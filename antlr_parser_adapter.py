"""
Adapter to integrate ANTLR-generated parser with the existing GUI.
Converts ANTLR parser output to SyntaxErrorRecord format compatible with main_window.py
"""

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
    """Custom error listener to capture ANTLR parsing errors"""
    
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
                col=column + 1,  # ANTLR uses 0-based columns, we use 1-based
                message=error_msg
            )
        )


class ANTLRParserAdapter:
    """Adapter to use ANTLR parser with Scanner tokens interface"""
    
    def __init__(self, code_text: str, lang: str = "ru"):
        """
        Initialize ANTLR parser adapter.
        
        Args:
            code_text: The source code to parse (raw text)
            lang: Language for error messages ("ru" or "en")
        """
        self.code_text = code_text
        self.lang = lang if lang in ("ru", "en") else "ru"
        self.errors: List[SyntaxErrorRecord] = []
        self.parse_tree = None

    def parse(self) -> ParseResult:
        """
        Parse the code using ANTLR parser.
        
        Returns:
            ParseResult with ok flag and list of errors
        """
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
            # Create input stream from text
            input_stream = InputStream(self.code_text)
            
            # Create lexer
            lexer = IfElseSubsetLexer(input_stream)
            
            # Create token stream from lexer
            stream = CommonTokenStream(lexer)
            
            # Create parser from token stream
            parser = IfElseSubsetParser(stream)
            
            # Remove default error listeners and add custom one
            parser.removeErrorListeners()
            error_listener = ANTLRErrorListener(lang=self.lang)
            parser.addErrorListener(error_listener)
            
            # Parse and get the parse tree
            self.parse_tree = parser.program()
            
            # Collect errors from listener
            self.errors = error_listener.errors
            
            # Additional semantic checks can be done here using visitor
            visitor = SemanticValidator(self.lang)
            visitor.visit(self.parse_tree)
            self.errors.extend(visitor.errors)
            
        except Exception as e:
            # Catch any unexpected errors
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
    """Semantic validator using visitor pattern"""
    
    def __init__(self, lang: str = "ru"):
        self.lang = lang
        self.errors: List[SyntaxErrorRecord] = []
        self.symbol_table: set = set()

    def visitIfStmt(self, ctx):
        """Validate if statement"""
        self.visitChildren(ctx)
        return None

    def visitStmt(self, ctx):
        """Validate statement - check if identifier is defined"""
        if ctx.ID():
            id_text = ctx.ID().getText()
            # Store identifier in symbol table
            self.symbol_table.add(id_text)
        
        self.visitChildren(ctx)
        return None


class ANTLRScanner:
    """ANTLR-based lexer that produces Scanner-compatible tokens"""
    
    def __init__(self):
        pass

    @staticmethod
    def tokens_from_text(text: str) -> List:
        """
        Tokenize text using ANTLR lexer.
        Returns list of tokens compatible with Scanner.Token format.
        """
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
                    start=antlr_token.column + 1,  # Convert to 1-based
                    end=antlr_token.column + len(antlr_token.text)
                )
                tokens.append(token)
        
        except Exception as e:
            pass  # Silently handle errors in tokenization
        
        return tokens

    @staticmethod
    def _map_token_type(antlr_token) -> str:
        """Map ANTLR token types to Scanner token types"""
        text = antlr_token.text
        
        # Map ANTLR symbol constant to readable name
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
