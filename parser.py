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
            if t.token_type == 'ERROR':
                continue
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
        return t.value if len(t.value) <= 32 else t.value[:29] + "..."

    def _add_error(self, fragment: str, line: int, col: int, message: str):
        self.errors.append(SyntaxErrorRecord(fragment=fragment, line=line, col=col, message=message))

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
            self._add_error(
                self._fragment(t),
                t.line if t else 1,
                t.start if t else 1,
                self._m("Ожидалось ключевое слово 'if' в начале конструкции", 
                        "Expected keyword 'if' at the beginning")
            )
            return ParseResult(ok=False, errors=self.errors)  # 🔥 ВЫХОД
        
        self._parse_if_body()

        return ParseResult(ok=len(self.errors) == 0, errors=list(self.errors))

    def _parse_if_body(self):
        self._depth += 1
        if self._depth > 100:
            self._depth -= 1
            return

        self._parse_cond()

        # === ИСПРАВЛЕНИЕ: надёжная проверка ':' ===
        has_colon = self._match_delimiter(":")

        if not has_colon:
            self._skip_newlines()
            if not self._match_delimiter(":"):
                t = self._current()
                self._add_error(
                    self._fragment(t),
                    t.line if t else 1,
                    t.start if t else 1,
                    self._m("Ожидалось ':' после условия if", "Expected ':' after if condition")
                )
            else:
                has_colon = True
                

        self._skip_newlines()
        self._parse_suite()           # then

        self._skip_newlines()

        if self._match_keyword("else"):
            if not self._match_delimiter(":"):
                t = self._current()
                self._add_error(self._fragment(t), t.line if t else 1, t.start if t else 1,
                                self._m("Ожидалось ':' после else", "Expected ':' after else"))
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
                self._sync_to(")", ":", "else", "\n")
        else:
            self._parse_compare()

    def _parse_compare(self):
        if not self._is_identifier():
            return
        self._advance()

        if self._current() and self._current().token_type == "OPERATOR":
            if self._current().value not in self.REL_OPS:
                t = self._current()
                self._add_error(
                    self._fragment(t),
                    t.line,
                    t.start,
                    self._m("Ожидался оператор сравнения", "Expected comparison operator")
                )
                self._advance()  
            else:
                self._advance()
        else:
            return


        if self._is_identifier():
            self._advance()