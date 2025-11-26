GRAMMAR_EBNF = r'''
Program        ::= "jersey" LBRACE DeclList RBRACE ;
DeclList       ::= { Decl } ;
Decl           ::= TeamDecl | ColorDecl | PatternDecl | NumberDecl | PlayerDecl | SponsorDecl | FontDecl ;

TeamDecl       ::= "team"     ":" STRING ";" ;
ColorDecl      ::= ("primary" | "secondary" | "tertiary") ":" COLOR ";" ;
PatternDecl    ::= "pattern"  ":" PatternExpr ";" ;
NumberDecl     ::= "number"   ":" INT ";" ;
PlayerDecl     ::= "player"   ":" STRING ";" ;
SponsorDecl    ::= "sponsor"  ":" STRING ";" ;
FontDecl       ::= "font"     ":" STRING ";" ;
PlayerSizeDecl   ::= "player_size" ":" INT ";" ;
NumberSizeDecl   ::= "number_size" ":" INT ";" ;
TeamSizeDecl   ::= "team_size" ":" INT ";" ;
SponsorSizeDecl   ::= "sponsor_size" ":" INT ";" ;

PatternExpr    ::= Ident "(" ArgList? ")" ;
ArgList        ::= Arg { "," Arg } ;
Arg            ::= INT | COLOR | STRING ;

Ident          ::= IDENT ;
COLOR          ::= "#" HEXDIGIT{3} | "#" HEXDIGIT{6} ;
INT            ::= DIGIT{1,9} ;
STRING         ::= '"' { ANY_BUT_QUOTE_OR_NEWLINE | Escaped } '"' ;
Escaped        ::= '\"' | '\n' | '\t' | '\\' ;

LBRACE         ::= '{' ;  RBRACE ::= '}' ;
LPAREN         ::= '(' ;  RPAREN ::= ')' ;
SEMI           ::= ';' ;  COLON ::= ':' ;  COMMA ::= ',' ;

WS             ::= ( ' ' | '\t' | '\r' | '\n' ) { WS } ;
LineComment    ::= '//' { any } ( '\n' | EOF ) ;
BlockComment   ::= '/*' { any } '*/' ;
'''.strip()


def print_grammar():
    print("\n=== Jersey DSL EBNF ===\n")
    print(GRAMMAR_EBNF)
