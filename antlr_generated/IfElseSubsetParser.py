# Generated from grammar/IfElseSubset.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,24,84,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,1,0,1,0,5,0,21,8,0,10,0,12,0,24,9,0,1,0,1,0,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,3,1,3,1,4,1,
        4,1,4,5,4,46,8,4,10,4,12,4,49,9,4,1,5,1,5,1,5,5,5,54,8,5,10,5,12,
        5,57,9,5,1,6,1,6,1,6,1,6,1,6,1,6,3,6,65,8,6,1,7,5,7,68,8,7,10,7,
        12,7,71,9,7,1,7,1,7,5,7,75,8,7,10,7,12,7,78,9,7,1,8,1,8,1,8,1,8,
        1,8,0,0,9,0,2,4,6,8,10,12,14,16,0,3,2,0,3,6,8,9,1,0,11,12,2,0,7,
        7,13,15,81,0,18,1,0,0,0,2,27,1,0,0,0,4,36,1,0,0,0,6,40,1,0,0,0,8,
        42,1,0,0,0,10,50,1,0,0,0,12,64,1,0,0,0,14,69,1,0,0,0,16,79,1,0,0,
        0,18,22,3,2,1,0,19,21,5,22,0,0,20,19,1,0,0,0,21,24,1,0,0,0,22,20,
        1,0,0,0,22,23,1,0,0,0,23,25,1,0,0,0,24,22,1,0,0,0,25,26,5,0,0,1,
        26,1,1,0,0,0,27,28,5,1,0,0,28,29,3,4,2,0,29,30,5,17,0,0,30,31,3,
        14,7,0,31,32,5,2,0,0,32,33,5,17,0,0,33,34,3,14,7,0,34,35,5,16,0,
        0,35,3,1,0,0,0,36,37,3,8,4,0,37,38,3,6,3,0,38,39,3,8,4,0,39,5,1,
        0,0,0,40,41,7,0,0,0,41,7,1,0,0,0,42,47,3,10,5,0,43,44,7,1,0,0,44,
        46,3,10,5,0,45,43,1,0,0,0,46,49,1,0,0,0,47,45,1,0,0,0,47,48,1,0,
        0,0,48,9,1,0,0,0,49,47,1,0,0,0,50,55,3,12,6,0,51,52,7,2,0,0,52,54,
        3,12,6,0,53,51,1,0,0,0,54,57,1,0,0,0,55,53,1,0,0,0,55,56,1,0,0,0,
        56,11,1,0,0,0,57,55,1,0,0,0,58,65,5,20,0,0,59,65,5,21,0,0,60,61,
        5,18,0,0,61,62,3,8,4,0,62,63,5,19,0,0,63,65,1,0,0,0,64,58,1,0,0,
        0,64,59,1,0,0,0,64,60,1,0,0,0,65,13,1,0,0,0,66,68,5,22,0,0,67,66,
        1,0,0,0,68,71,1,0,0,0,69,67,1,0,0,0,69,70,1,0,0,0,70,72,1,0,0,0,
        71,69,1,0,0,0,72,76,3,16,8,0,73,75,5,22,0,0,74,73,1,0,0,0,75,78,
        1,0,0,0,76,74,1,0,0,0,76,77,1,0,0,0,77,15,1,0,0,0,78,76,1,0,0,0,
        79,80,5,21,0,0,80,81,5,10,0,0,81,82,3,8,4,0,82,17,1,0,0,0,6,22,47,
        55,64,69,76
    ]

class IfElseSubsetParser ( Parser ):

    grammarFileName = "IfElseSubset.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'else'", "'>='", "'<='", "'=='", 
                     "'!='", "'//'", "'>'", "'<'", "'='", "'+'", "'-'", 
                     "'*'", "'/'", "'%'", "';'", "':'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "IF", "ELSE", "GE", "LE", "EQ", "NE", 
                      "IDIV", "GT", "LT", "ASSIGN", "PLUS", "MINUS", "STAR", 
                      "DIV", "MOD", "SEMI", "COLON", "LPAREN", "RPAREN", 
                      "INT", "ID", "NL", "WS", "COMMENT" ]

    RULE_program = 0
    RULE_ifStmt = 1
    RULE_cond = 2
    RULE_relOp = 3
    RULE_expr = 4
    RULE_term = 5
    RULE_factor = 6
    RULE_suite = 7
    RULE_stmt = 8

    ruleNames =  [ "program", "ifStmt", "cond", "relOp", "expr", "term", 
                   "factor", "suite", "stmt" ]

    EOF = Token.EOF
    IF=1
    ELSE=2
    GE=3
    LE=4
    EQ=5
    NE=6
    IDIV=7
    GT=8
    LT=9
    ASSIGN=10
    PLUS=11
    MINUS=12
    STAR=13
    DIV=14
    MOD=15
    SEMI=16
    COLON=17
    LPAREN=18
    RPAREN=19
    INT=20
    ID=21
    NL=22
    WS=23
    COMMENT=24

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ifStmt(self):
            return self.getTypedRuleContext(IfElseSubsetParser.IfStmtContext,0)


        def EOF(self):
            return self.getToken(IfElseSubsetParser.EOF, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(IfElseSubsetParser.NL)
            else:
                return self.getToken(IfElseSubsetParser.NL, i)

        def getRuleIndex(self):
            return IfElseSubsetParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = IfElseSubsetParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 18
            self.ifStmt()
            self.state = 22
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==22:
                self.state = 19
                self.match(IfElseSubsetParser.NL)
                self.state = 24
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 25
            self.match(IfElseSubsetParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(IfElseSubsetParser.IF, 0)

        def cond(self):
            return self.getTypedRuleContext(IfElseSubsetParser.CondContext,0)


        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(IfElseSubsetParser.COLON)
            else:
                return self.getToken(IfElseSubsetParser.COLON, i)

        def suite(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IfElseSubsetParser.SuiteContext)
            else:
                return self.getTypedRuleContext(IfElseSubsetParser.SuiteContext,i)


        def ELSE(self):
            return self.getToken(IfElseSubsetParser.ELSE, 0)

        def SEMI(self):
            return self.getToken(IfElseSubsetParser.SEMI, 0)

        def getRuleIndex(self):
            return IfElseSubsetParser.RULE_ifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = IfElseSubsetParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_ifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.match(IfElseSubsetParser.IF)
            self.state = 28
            self.cond()
            self.state = 29
            self.match(IfElseSubsetParser.COLON)
            self.state = 30
            self.suite()
            self.state = 31
            self.match(IfElseSubsetParser.ELSE)
            self.state = 32
            self.match(IfElseSubsetParser.COLON)
            self.state = 33
            self.suite()
            self.state = 34
            self.match(IfElseSubsetParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CondContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IfElseSubsetParser.ExprContext)
            else:
                return self.getTypedRuleContext(IfElseSubsetParser.ExprContext,i)


        def relOp(self):
            return self.getTypedRuleContext(IfElseSubsetParser.RelOpContext,0)


        def getRuleIndex(self):
            return IfElseSubsetParser.RULE_cond

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCond" ):
                return visitor.visitCond(self)
            else:
                return visitor.visitChildren(self)




    def cond(self):

        localctx = IfElseSubsetParser.CondContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_cond)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.expr()
            self.state = 37
            self.relOp()
            self.state = 38
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GT(self):
            return self.getToken(IfElseSubsetParser.GT, 0)

        def LT(self):
            return self.getToken(IfElseSubsetParser.LT, 0)

        def GE(self):
            return self.getToken(IfElseSubsetParser.GE, 0)

        def LE(self):
            return self.getToken(IfElseSubsetParser.LE, 0)

        def EQ(self):
            return self.getToken(IfElseSubsetParser.EQ, 0)

        def NE(self):
            return self.getToken(IfElseSubsetParser.NE, 0)

        def getRuleIndex(self):
            return IfElseSubsetParser.RULE_relOp

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelOp" ):
                return visitor.visitRelOp(self)
            else:
                return visitor.visitChildren(self)




    def relOp(self):

        localctx = IfElseSubsetParser.RelOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_relOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 888) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IfElseSubsetParser.TermContext)
            else:
                return self.getTypedRuleContext(IfElseSubsetParser.TermContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(IfElseSubsetParser.PLUS)
            else:
                return self.getToken(IfElseSubsetParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(IfElseSubsetParser.MINUS)
            else:
                return self.getToken(IfElseSubsetParser.MINUS, i)

        def getRuleIndex(self):
            return IfElseSubsetParser.RULE_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = IfElseSubsetParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.term()
            self.state = 47
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11 or _la==12:
                self.state = 43
                _la = self._input.LA(1)
                if not(_la==11 or _la==12):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 44
                self.term()
                self.state = 49
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IfElseSubsetParser.FactorContext)
            else:
                return self.getTypedRuleContext(IfElseSubsetParser.FactorContext,i)


        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(IfElseSubsetParser.STAR)
            else:
                return self.getToken(IfElseSubsetParser.STAR, i)

        def DIV(self, i:int=None):
            if i is None:
                return self.getTokens(IfElseSubsetParser.DIV)
            else:
                return self.getToken(IfElseSubsetParser.DIV, i)

        def MOD(self, i:int=None):
            if i is None:
                return self.getTokens(IfElseSubsetParser.MOD)
            else:
                return self.getToken(IfElseSubsetParser.MOD, i)

        def IDIV(self, i:int=None):
            if i is None:
                return self.getTokens(IfElseSubsetParser.IDIV)
            else:
                return self.getToken(IfElseSubsetParser.IDIV, i)

        def getRuleIndex(self):
            return IfElseSubsetParser.RULE_term

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = IfElseSubsetParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.factor()
            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 57472) != 0):
                self.state = 51
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 57472) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 52
                self.factor()
                self.state = 57
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(IfElseSubsetParser.INT, 0)

        def ID(self):
            return self.getToken(IfElseSubsetParser.ID, 0)

        def LPAREN(self):
            return self.getToken(IfElseSubsetParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(IfElseSubsetParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(IfElseSubsetParser.RPAREN, 0)

        def getRuleIndex(self):
            return IfElseSubsetParser.RULE_factor

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFactor" ):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)




    def factor(self):

        localctx = IfElseSubsetParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_factor)
        try:
            self.state = 64
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20]:
                self.enterOuterAlt(localctx, 1)
                self.state = 58
                self.match(IfElseSubsetParser.INT)
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.match(IfElseSubsetParser.ID)
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 3)
                self.state = 60
                self.match(IfElseSubsetParser.LPAREN)
                self.state = 61
                self.expr()
                self.state = 62
                self.match(IfElseSubsetParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SuiteContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self):
            return self.getTypedRuleContext(IfElseSubsetParser.StmtContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(IfElseSubsetParser.NL)
            else:
                return self.getToken(IfElseSubsetParser.NL, i)

        def getRuleIndex(self):
            return IfElseSubsetParser.RULE_suite

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSuite" ):
                return visitor.visitSuite(self)
            else:
                return visitor.visitChildren(self)




    def suite(self):

        localctx = IfElseSubsetParser.SuiteContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_suite)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==22:
                self.state = 66
                self.match(IfElseSubsetParser.NL)
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 72
            self.stmt()
            self.state = 76
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==22:
                self.state = 73
                self.match(IfElseSubsetParser.NL)
                self.state = 78
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(IfElseSubsetParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(IfElseSubsetParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(IfElseSubsetParser.ExprContext,0)


        def getRuleIndex(self):
            return IfElseSubsetParser.RULE_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = IfElseSubsetParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(IfElseSubsetParser.ID)
            self.state = 80
            self.match(IfElseSubsetParser.ASSIGN)
            self.state = 81
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





