grammar IfElseSubset;

options { language=Python3; }

program
    : ifStmt NL* EOF
    ;

ifStmt
    : IF cond COLON suite ELSE COLON suite
    ;

cond
    : expr relOp expr
    ;

relOp
    : GT | LT | GE | LE | EQ | NE
    ;

expr
    : term ( (PLUS | MINUS) term )*
    ;

term
    : factor ( (STAR | DIV | MOD | IDIV) factor )*
    ;

factor
    : INT
    | ID
    | LPAREN expr RPAREN
    ;

suite
    : NL* stmt NL*
    ;

stmt
    : ID ASSIGN expr SEMI
    ;

IF      : 'if' ;
ELSE    : 'else' ;

GE      : '>=' ;
LE      : '<=' ;
EQ      : '==' ;
NE      : '!=' ;
IDIV    : '//' ;

GT      : '>' ;
LT      : '<' ;

ASSIGN  : '=' ;
PLUS    : '+' ;
MINUS   : '-' ;
STAR    : '*' ;
DIV     : '/' ;
MOD     : '%' ;

SEMI    : ';' ;
COLON   : ':' ;
LPAREN  : '(' ;
RPAREN  : ')' ;

INT     : [0-9]+ ;

ID      : [a-zA-Z_] [a-zA-Z0-9_]* ;

NL      : '\r'? '\n' ;

WS      : [ \t]+ -> skip ;

COMMENT : '#' ~[\r\n]* -> skip ;
