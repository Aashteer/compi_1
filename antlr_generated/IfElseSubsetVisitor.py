# Generated from grammar/IfElseSubset.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .IfElseSubsetParser import IfElseSubsetParser
else:
    from IfElseSubsetParser import IfElseSubsetParser

# This class defines a complete generic visitor for a parse tree produced by IfElseSubsetParser.

class IfElseSubsetVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by IfElseSubsetParser#program.
    def visitProgram(self, ctx:IfElseSubsetParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IfElseSubsetParser#ifStmt.
    def visitIfStmt(self, ctx:IfElseSubsetParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IfElseSubsetParser#cond.
    def visitCond(self, ctx:IfElseSubsetParser.CondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IfElseSubsetParser#relOp.
    def visitRelOp(self, ctx:IfElseSubsetParser.RelOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IfElseSubsetParser#expr.
    def visitExpr(self, ctx:IfElseSubsetParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IfElseSubsetParser#term.
    def visitTerm(self, ctx:IfElseSubsetParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IfElseSubsetParser#factor.
    def visitFactor(self, ctx:IfElseSubsetParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IfElseSubsetParser#suite.
    def visitSuite(self, ctx:IfElseSubsetParser.SuiteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IfElseSubsetParser#stmt.
    def visitStmt(self, ctx:IfElseSubsetParser.StmtContext):
        return self.visitChildren(ctx)



del IfElseSubsetParser