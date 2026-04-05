from __future__ import annotations

from io import StringIO
from typing import List, Optional, TYPE_CHECKING
from dataclasses import dataclass, field

from antlr4 import (
    InputStream,
    CommonTokenStream,
    RecognitionException,
    Parser as ANTLRParser
)
from antlr4.error.ErrorListener import ErrorListener

from antlr_generated.IfElseSubsetLexer import IfElseSubsetLexer
from antlr_generated.IfElseSubsetParser import IfElseSubsetParser
from antlr_generated.IfElseSubsetVisitor import IfElseSubsetVisitor

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


class ANTLRErrorListener(ErrorListener):
    
    def __init__(self, lang: str = "ru"):
        super().__init__()
        self.errors: List[SyntaxErrorRecord] = []
        self.lang = lang

    def syntaxError(self, recognizer, offendingToken, line, column, msg, e):
        fragment = offendingToken.text if offendingToken and offendingToken.text else "EOF"
        if len(fragment) > 32:
            fragment = fragment[:29] + "..."
        
        if self.lang == "ru":
            error_msg = f"Синтаксическая ошибка: {msg}"
        else:
            error_msg = f"Syntax error: {msg}"
        
        self.errors.append(
            SyntaxErrorRecord(
                fragment=fragment,
                line=line,
                col=column + 1,  
                message=error_msg
            )
        )


class ANTLRParserAdapter:
    
    def __init__(self, code_text: str, lang: str = "ru"):
        self.code_text = code_text
        self.lang = lang if lang in ("ru", "en") else "ru"
        self.errors: List[SyntaxErrorRecord] = []
        self.parse_tree = None

    def parse(self) -> ParseResult:
        self.errors = []
        
        if not self.code_text.strip():
            if self.lang == "ru":
                msg = "Пустой поток ввода"
            else:
                msg = "Empty input stream"
            self.errors.append(
                SyntaxErrorRecord(
                    fragment="EOF",
                    line=1,
                    col=1,
                    message=msg
                )
            )
            return ParseResult(ok=False, errors=list(self.errors))

        try:
            input_stream = InputStream(self.code_text)
            
            lexer = IfElseSubsetLexer(input_stream)
            
            stream = CommonTokenStream(lexer)
            
            parser = IfElseSubsetParser(stream)
            
            parser.removeErrorListeners()
            error_listener = ANTLRErrorListener(lang=self.lang)
            parser.addErrorListener(error_listener)
            
            self.parse_tree = parser.program()

            self.errors = error_listener.errors

            visitor = SemanticValidator(self.lang)
            visitor.visit(self.parse_tree)
            self.errors.extend(visitor.errors)
            
        except Exception as e:
            if self.lang == "ru":
                msg = f"Ошибка при разборе: {str(e)}"
            else:
                msg = f"Parsing error: {str(e)}"
            
            self.errors.append(
                SyntaxErrorRecord(
                    fragment="ERROR",
                    line=1,
                    col=1,
                    message=msg
                )
            )

        return ParseResult(ok=len(self.errors) == 0, errors=list(self.errors))


class SemanticValidator(IfElseSubsetVisitor):
    
    def __init__(self, lang: str = "ru"):
        self.lang = lang
        self.errors: List[SyntaxErrorRecord] = []
        self.symbol_table: set = set()

    def visitIfStmt(self, ctx):
        self.visitChildren(ctx)
        return None

    def visitStmt(self, ctx):
        if ctx.ID():
            id_text = ctx.ID().getText()
            self.symbol_table.add(id_text)
        
        self.visitChildren(ctx)
        return None


class ANTLRScanner:
    
    def __init__(self):
        pass

    @staticmethod
    def tokens_from_text(text: str) -> List:
        from scanner import Token
        
        tokens = []
        
        try:
            input_stream = InputStream(text)
            lexer = IfElseSubsetLexer(input_stream)
            
            for antlr_token in lexer.getAllTokens():
                token_type = ANTLRScanner._map_token_type(antlr_token)
                token = Token(
                    token_type=token_type,
                    value=antlr_token.text,
                    line=antlr_token.line,
                    start=antlr_token.column + 1,  
                    end=antlr_token.column + len(antlr_token.text)
                )
                tokens.append(token)
        
        except Exception as e:
            pass  
        
        return tokens

    @staticmethod
    def _map_token_type(antlr_token) -> str:
        text = antlr_token.text

        if text in ('if', 'else'):
            return 'KEYWORD'
        elif text in ('>', '<', '>=', '<=', '==', '!=', '=', '+', '-', '*', '/', '%', '//'):
            return 'OPERATOR'
        elif text in (':', ';', '(', ')', '{', '}', '[', ']', ',', '\n'):
            return 'DELIMITER'
        elif text.isdigit():
            return 'INTEGER'
        elif text.replace('_', '').isalnum() and (text[0].isalpha() or text[0] == '_'):
            return 'IDENTIFIER'
        else:
            return 'ERROR'
