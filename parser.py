from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from scanner import Token


@dataclass
class SyntaxErrorRecord:
    fragment: str
    line: int
    col: int
    message: str

    def location_ru(self) -> str:
        return f"строка {self.line}, позиция {self.col}"

    def location_en(self) -> str:
        return f"line {self.line}, position {self.col}"


@dataclass
class ParseResult:
    ok: bool
    errors: List[SyntaxErrorRecord] = field(default_factory=list)


class Parser:
    REL_OPS = {'>', '<', '>=', '<=', '==', '!='}
    ASSIGN_OPS = {'=', '+=', '-=', '*=', '/='}

    def __init__(self, tokens: List["Token"], lang: str = "ru"):
        self.tokens: List["Token"] = self._filter_tokens(tokens)
        self.i = 0
        self.errors: List[SyntaxErrorRecord] = []
        self.lang = lang if lang in ("ru", "en") else "ru"
        self._depth = 0

    def _m(self, ru: str, en: str) -> str:
        return en if self.lang == "en" else ru

    @staticmethod
    def _filter_tokens(tokens: List["Token"]) -> List["Token"]:
        out = []
        for t in tokens:
            if t.token_type == 'DELIMITER' and t.value in ('(пробел)', '\\t'):
                continue
            out.append(t)
        return out

    def _current(self) -> Optional["Token"]:
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def _advance(self) -> None:
        self.i += 1

    def _fragment(self, t: Optional["Token"]) -> str:
        if not t:
            return "EOF"
        raw = getattr(t, "raw_lexeme", t.value)
        return raw if len(raw) <= 32 else raw[:29] + "..."

    def _collect_repeated_fragment(self, token_type: str, value: str) -> str:
        j = self.i
        parts = []
        while j < len(self.tokens):
            t = self.tokens[j]
            if t.token_type != token_type or t.value != value:
                break
            parts.append(self._fragment(t))
            j += 1
        return "".join(parts) if parts else value

    def _current_grouped_fragment(self) -> str:
        t = self._current()
        if not t:
            return "EOF"
        if t.token_type == "DELIMITER":
            return self._collect_repeated_fragment("DELIMITER", t.value)
        return self._fragment(t)

    def _add_error(self, fragment: str, line: int, col: int, message: str):
        self.errors.append(SyntaxErrorRecord(fragment=fragment, line=line, col=col, message=message))

    def _line_has_token(self, start_index: int, token_type: str, value: Optional[str] = None) -> bool:
        j = start_index
        while j < len(self.tokens):
            t = self.tokens[j]
            if t.token_type == "DELIMITER" and t.value == "\\n":
                return False
            if t.token_type == token_type and (value is None or t.value == value):
                return True
            j += 1
        return False

    def _sync_to_line_end(self, consume_newline: bool = False):
        while self._current() is not None and not self._is_newline():
            self._advance()
        if consume_newline and self._is_newline():
            self._advance()

    def _sync_to_stmt_end(self):
        while self._current() is not None:
            t = self._current()
            if t.token_type == "DELIMITER" and t.value in (";", "\\n"):
                return
            self._advance()

    def _consume_stmt_end(self):
        if self._match_delimiter(";"):
            return
        if self._is_newline():
            self._advance()

    def _consume_trailing_tokens_after_colon(self, context_name: str):
        t = self._current()
        if t is None or self._is_newline():
            return
        self._add_error(
            self._fragment(t),
            t.line,
            t.start,
            self._m(
                f"Неожиданные символы после ':' в {context_name}",
                f"Unexpected tokens after ':' in {context_name}"
            )
        )
        self._sync_to_line_end()

    def _skip_newlines(self):
        while self._is_newline():
            self._advance()

    def _is_newline(self) -> bool:
        t = self._current()
        return t is not None and t.token_type == "DELIMITER" and t.value == "\\n"

    def _is_identifier(self) -> bool:
        t = self._current()
        return t is not None and t.token_type == "IDENTIFIER"

    def _match_keyword(self, word: str) -> bool:
        t = self._current()
        if t and t.token_type == "KEYWORD" and t.value == word:
            self._advance()
            return True
        return False

    def _match_delimiter(self, ch: str) -> bool:
        t = self._current()
        if t and t.token_type == "DELIMITER" and t.value == ch:
            self._advance()
            return True
        return False

    def _match_assignment_operator(self) -> bool:
        t = self._current()
        if t and t.token_type == "OPERATOR" and t.value in self.ASSIGN_OPS:
            self._advance()
            return True
        return False

    def _sync_to(self, *sync_values: str):
        vals = set(sync_values)
        while self._current() is not None:
            t = self._current()
            if (t.token_type == 'KEYWORD' and t.value in vals) or \
               (t.token_type == 'DELIMITER' and t.value in vals):
                return
            self._advance()

    # ====================== ГЛАВНЫЙ МЕТОД ======================
    def parse(self) -> ParseResult:
        self.errors = []
        self.i = 0
        self._depth = 0

        if not self.tokens:
            self._add_error("EOF", 1, 1, self._m("Пустой ввод", "Empty input"))
            return ParseResult(ok=False, errors=self.errors)

        self._skip_newlines()

        started_with_if = self._match_keyword("if")

        if not started_with_if:
            t = self._current()
            start_index = self.i
            self._add_error(
                self._fragment(t),
                t.line if t else 1,
                t.start if t else 1,
                self._m("Ожидалось ключевое слово 'if' в начале конструкции", 
                        "Expected keyword 'if' at the beginning")
            )
            if t and t.token_type == "DELIMITER" and t.value == ";":
                return ParseResult(ok=False, errors=list(self.errors))
            # Восстановление: если сможем найти начало условия вида
            # <ID> <relop> <ID> ':' — прыгаем туда, чтобы не плодить ошибки.
            recovered = self._recover_to_if_condition_start()
            if not recovered:
                # Иначе пытаемся хотя бы сдвинуться к первому идентификатору,
                # чтобы поймать ошибку в условии (например пропущен relOp).
                skipped_error = None
                for k in range(start_index + 1, len(self.tokens)):
                    tok = self.tokens[k]
                    if tok.token_type == "DELIMITER" and tok.value == "\\n":
                        break
                    if tok.token_type == "ERROR":
                        skipped_error = tok
                        break
                self.i = start_index + 1
                while self._current() is not None and self._current().token_type != "IDENTIFIER":
                    self._advance()
                cur = self._current()
                if (
                    skipped_error is not None
                    and cur is not None
                    and cur.token_type == "IDENTIFIER"
                    and cur.value == "f"
                    and self._line_has_error_before_relop(self.i + 1)
                ):
                    self._add_error(
                        self._fragment(skipped_error),
                        skipped_error.line,
                        skipped_error.start,
                        skipped_error.value
                    )
            else:
                # При восстановлении в начало условия часть ERROR-токенов
                # оказывается "позади" текущей позиции. Для случаев вроде
                # `i @a > b` вернем эту ошибку в итоговый список, но не будем
                # дублировать ее для `i@f`, где шум появляется внутри самого
                # слова `if`.
                err_index = None
                for k in range(start_index + 1, self.i + 1):
                    if k >= len(self.tokens):
                        break
                    if self.tokens[k].token_type == "ERROR":
                        err_index = k
                        break
                if err_index is not None:
                    next_tok = self.tokens[err_index + 1] if err_index + 1 < len(self.tokens) else None
                    # `i@f ...` — считаем `@` частью опечатки и не добавляем отдельной ошибкой.
                    should_restore = not (next_tok and next_tok.token_type == "IDENTIFIER" and next_tok.value == "f")
                    if not should_restore and next_tok is not None:
                        should_restore = self._line_has_error_before_relop(err_index + 2)
                    if should_restore:
                        err_tok = self.tokens[err_index]
                        self._add_error(
                            self._fragment(err_tok),
                            err_tok.line,
                            err_tok.start,
                            err_tok.value
                        )
        
        self._parse_if_body()

        return ParseResult(ok=len(self.errors) == 0, errors=list(self.errors))

    def _recover_to_if_condition_start(self) -> bool:
        """
        Пытаемся выставить `self.i` так, чтобы текущее положение соответствовало началу условия if:
        <IDENTIFIER> <REL_OP> <IDENTIFIER> ':'.
        """
        if not self.tokens:
            return False

        start = max(0, self.i)
        start_line = self.tokens[start].line if start < len(self.tokens) else 1
        for k in range(start + 1, len(self.tokens) - 2):
            t = self.tokens[k]
            if t.line != start_line:
                break
            if t.token_type != "OPERATOR" or t.value not in self.REL_OPS:
                continue
            left = self.tokens[k - 1]
            right = self.tokens[k + 1]
            if left.token_type == "IDENTIFIER" and right.token_type == "IDENTIFIER":
                self.i = k - 1
                return True
        return False

    def _parse_if_body(self):
        self._depth += 1
        if self._depth > 100:
            self._depth -= 1
            return

        self._parse_cond()

        # Отдельно помечаем лишние закрывающие скобки перед ':'.
        if self._current() and self._current().token_type == "DELIMITER" and self._current().value == ")":
            t = self._current()
            self._add_error(
                self._collect_repeated_fragment("DELIMITER", ")"),
                t.line,
                t.start,
                self._m("Лишняя закрывающая скобка ')'", "Unexpected closing parenthesis ')'")
            )
            # Съедаем все подряд идущие `)`, чтобы не получить вторую
            # искусственную ошибку "Ожидалось ':'" на этом же месте.
            while self._current() and self._current().token_type == "DELIMITER" and self._current().value == ")":
                self._advance()

        # === ИСПРАВЛЕНИЕ: надёжная проверка ':' ===
        has_colon = self._match_delimiter(":")

        if not has_colon:
            self._skip_newlines()
            if not self._match_delimiter(":"):
                t = self._current()
                self._add_error(
                    self._current_grouped_fragment(),
                    t.line if t else 1,
                    t.start if t else 1,
                    self._m("Ожидалось ':' после условия if", "Expected ':' after if condition")
                )
                if t is not None and self._line_has_token(self.i, "DELIMITER", ":"):
                    self._sync_to(":", "\\n")
                    if self._match_delimiter(":"):
                        has_colon = True
            else:
                has_colon = True
        if has_colon:
            self._consume_trailing_tokens_after_colon("if")

        self._skip_newlines()
        self._parse_suite()           # then

        self._skip_newlines()

        if self._match_keyword("else"):
            has_else_colon = False
            if not self._match_delimiter(":"):
                t = self._current()
                if self._skip_error_suffix_before_colon():
                    has_else_colon = True
                    self._consume_trailing_tokens_after_colon("else")
                    self._skip_newlines()
                    self._parse_suite()
                    self._depth -= 1
                    return
                self._add_error(
                    self._current_grouped_fragment(),
                    t.line if t else 1,
                    t.start if t else 1,
                    self._m("Ожидалось ':' после else", "Expected ':' after else")
                )
                if t is not None and self._line_has_token(self.i, "DELIMITER", ":"):
                    self._sync_to(":", "\\n")
                    if self._match_delimiter(":"):
                        has_else_colon = True
            else:
                has_else_colon = True

            if has_else_colon:
                self._consume_trailing_tokens_after_colon("else")
            self._skip_newlines()
            self._parse_suite()
        else:
            t = self._current()
            self._add_error(
                self._fragment(t),
                t.line if t else 1,
                t.start if t else 1,
                self._m("Ожидалось ключевое слово 'else'", "Expected keyword 'else'")
            )
            if (
                t is not None
                and t.token_type == "IDENTIFIER"
                and t.value.startswith("el")
                and not self._line_has_token(self.i, "DELIMITER", ":")
            ):
                self._add_error(
                    self._fragment(t),
                    t.line,
                    t.start,
                    self._m("Ожидалось ':' после else", "Expected ':' after else")
                )
            # Восстановление: если вместо `else:` написали `els:`/`el$se:` и т.п.,
            # то всё равно разберем else-блок и соберем ошибки внутри.
            if self._recover_to_colon_on_same_line():
                self._consume_trailing_tokens_after_colon("else")
                self._skip_newlines()
                self._parse_suite()

        self._depth -= 1

    def _parse_suite(self):
        self._depth += 1
        if self._depth > 100:
            self._depth -= 1
            return

        while self._current() is not None:
            self._skip_newlines()
            t = self._current()
            if t is None or t.value in ('else', 'if'):
                break

            # Если строка then-блока начинается с "el..." и дальше по этой строке есть ':',
            # считаем, что это опечатка в `else:` (например `el$se:` или `el;se:`),
            # и останавливаем suite, чтобы внешний уровень добавил только 1 ошибку "else".
            if t.token_type == "IDENTIFIER" and t.value.startswith("el"):
                found_colon = False
                j = self.i
                while j < len(self.tokens):
                    tj = self.tokens[j]
                    if tj.token_type == "DELIMITER" and tj.value == "\\n":
                        break
                    if tj.token_type == "DELIMITER" and tj.value == ":":
                        found_colon = True
                        break
                    j += 1
                if found_colon:
                    break

            # `els:` (опечатка вместо `else:`) — не пытаться разбирать как присваивание.
            # Иначе появится лишняя ошибка про оператор присваивания.
            next_t = self.tokens[self.i + 1] if self.i + 1 < len(self.tokens) else None
            if (
                t is not None
                and t.token_type == "IDENTIFIER"
                and t.value == "els"
            ):
                break

            self._parse_assign()
            self._skip_newlines()

            # Защита от зацикливания
            if self._current() is t:
                self._advance()
                continue

        self._depth -= 1

    def _parse_assign(self):
        if not self._is_identifier():
            return

        line = self._current().line
        col = self._current().start
        self._advance()

        # Специальный случай вроде `max @= a;`:
        # считаем это одной ошибкой оператора присваивания и не плодим каскад.
        if self._current() and self._current().token_type == "ERROR":
            t = self._current()
            self._add_error(
                self._fragment(t),
                t.line,
                t.start,
                self._m("Ожидался оператор присваивания", "Expected assignment operator")
            )
            self._sync_to_stmt_end()
            self._consume_stmt_end()
            return

        if self._current() and self._current().token_type == "OPERATOR":
            if self._current().value not in self.ASSIGN_OPS:
                t = self._current()
                self._add_error(
                    self._fragment(t),
                    line,
                    col,
                    self._m("Ожидался оператор присваивания", "Expected assignment operator")
                )
                self._advance()  # съедаем неправильный оператор (например ==)
            else:
                self._advance()
        else:
            t = self._current()
            self._add_error(
                self._fragment(t),
                line,
                col,
                self._m("Ожидался оператор присваивания", "Expected assignment operator")
            )
            if not self._line_has_token(self.i, "DELIMITER", ";"):
                self._add_error(
                    self._fragment(t),
                    line,
                    col,
                    self._m("Ожидалась ';' после присваивания", "Expected ';' after assignment")
                )
            self._sync_to_stmt_end()
            self._consume_stmt_end()
            return

        # правая часть
        if not self._is_identifier():
            t = self._current()
            self._add_error(
                self._fragment(t),
                line,
                col,
                self._m("Ожидался идентификатор после =", "Expected identifier after =")
            )
            return

        self._advance()

        # точка с запятой
        if not self._match_delimiter(";"):
            t = self._current()
            self._add_error(
                self._fragment(t),
                line,
                col,
                self._m("Ожидалась ';' после присваивания", "Expected ';' after assignment")
            )

    def _looks_like_suite_start(self, token: Optional["Token"]) -> bool:
        if token is None:
            return True
        if token.token_type == "IDENTIFIER":
            return True
        if token.token_type == "KEYWORD" and token.value in {"if", "else"}:
            return True
        return False

    def _skip_error_suffix_before_colon(self) -> bool:
        t = self._current()
        if t is None or t.token_type != "ERROR":
            return False
        if len(self._fragment(t)) <= 1:
            return False

        j = self.i
        while j < len(self.tokens):
            tj = self.tokens[j]
            if tj.token_type == "DELIMITER" and tj.value == "\\n":
                return False
            if tj.token_type == "DELIMITER" and tj.value == ":":
                self.i = j + 1
                return True
            if tj.token_type != "ERROR":
                return False
            j += 1
        return False

    def _line_has_error_after(self, start_index: int, min_raw_len: int = 1) -> bool:
        j = start_index
        while j < len(self.tokens):
            t = self.tokens[j]
            if t.token_type == "DELIMITER" and t.value == "\\n":
                return False
            if t.token_type == "ERROR" and len(self._fragment(t)) >= min_raw_len:
                return True
            j += 1
        return False

    def _line_has_error_before_relop(self, start_index: int) -> bool:
        j = start_index
        while j < len(self.tokens):
            t = self.tokens[j]
            if t.token_type == "DELIMITER" and t.value == "\\n":
                return False
            if t.token_type == "OPERATOR" and t.value in self.REL_OPS:
                return False
            if t.token_type == "ERROR":
                return True
            j += 1
        return False

    def _recover_to_colon_on_same_line(self) -> bool:
        """
        Если текущая позиция на строке `else`-заголовка (или его опечатки) и на этой же строке
        есть ':', то переходим на символ после ':' и возвращаем True.
        """
        t = self._current()
        if t is None:
            return False
        start_line = t.line
        j = self.i
        while j < len(self.tokens):
            tj = self.tokens[j]
            if tj.line != start_line or (tj.token_type == "DELIMITER" and tj.value == "\\n"):
                return False
            if tj.token_type == "DELIMITER" and tj.value == ":":
                self.i = j + 1
                return True
            j += 1
        return False


    # ====================== УСЛОВИЕ ======================
    def _parse_cond(self):
        self._parse_logical_term()
        while self._match_keyword("or"):
            self._parse_logical_term()

    def _parse_logical_term(self):
        self._parse_logical_factor()
        while self._match_keyword("and"):
            self._parse_logical_factor()

    def _parse_logical_factor(self):
        if self._match_keyword("not"):
            self._parse_primary_cond()
        else:
            self._parse_primary_cond()

    def _parse_primary_cond(self):
        if self._match_delimiter("("):
            self._parse_cond()
            if not self._match_delimiter(")"):
                t = self._current()
                self._add_error(self._fragment(t), t.line if t else 1, t.start if t else 1,
                                self._m("Ожидалась ')'", "Expected closing parenthesis ')'"))
                self._sync_to(")", ":", "else", "\\n")
        else:
            self._parse_compare()

    def _parse_compare(self):
        t = self._current()
        if t is not None and t.token_type in ("ERROR", "OPERATOR"):
            self._add_error(
                self._fragment(t),
                t.line,
                t.start,
                self._m("Ожидался идентификатор", "Expected identifier")
            )
            self._advance()

        if not self._is_identifier():
            return
        self._advance()

        # Должен быть оператор сравнения (>, <, >=, ...)
        t = self._current()
        if not t:
            return
        if t.token_type != "OPERATOR":
            self._add_error(
                self._fragment(t),
                t.line,
                t.start,
                self._m("Ожидался оператор сравнения", "Expected comparison operator")
            )
            # Пропустим до ближайшего ')' или ':' конца условия, чтобы не получить лишнюю цепочку ошибок.
            self._sync_to(")", ":", "\\n")
            return

        if t.value not in self.REL_OPS:
            self._add_error(
                self._fragment(t),
                t.line,
                t.start,
                self._m("Ожидался оператор сравнения", "Expected comparison operator")
            )
            self._sync_to(")", ":", "\\n")
            return

        self._advance()  # consume relop

        if not self._is_identifier():
            t2 = self._current()
            if t2:
                self._add_error(
                    self._fragment(t2),
                    t2.line,
                    t2.start,
                    self._m("Ожидался идентификатор", "Expected identifier")
                )
            self._sync_to(")", ":", "\\n")
            return

        self._advance()  # consume right operand