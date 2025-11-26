
from dataclasses import dataclass
from typing import List, Optional
from ..ast.nodes import (
    JerseyNode, TeamNode, ColorNode, NumberNode, PlayerNode,
    SponsorNode, FontNode, PlayerSizeNode, NumberSizeNode, TeamSizeNode, SponsorSizeNode, PatternNode
)

@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int

class ParserError(SyntaxError):
    pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.i = 0

    # --- cursor helpers
    def _peek(self) -> Optional[Token]:
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def _match(self, *types: str) -> Optional[Token]:
        tok = self._peek()
        if tok and tok.type in types:
            self.i += 1
            return tok
        return None

    def _expect(self, typ: str, msg: str) -> Token:
        tok = self._match(typ)
        if not tok:
            got = self._peek()
            where = f" at line {got.line}, col {got.col}" if got else ""
            raise ParserError(f"Expected {typ} {msg}, got {got.type if got else 'EOF'}{where}")
        return tok

    # ------------- entry point -------------
    def parse(self) -> JerseyNode:
        node = self._parse_jersey()
        extra = self._peek()
        if extra and extra.type != "EOF":
            raise ParserError(f"Extra tokens after jersey block at line {extra.line}, col {extra.col}")
        return node

    # program := jersey_block
    def _parse_jersey(self) -> JerseyNode:
        self._expect("JERSEY", "to start jersey block")
        self._expect("LBRACE", "after 'jersey'")
        stmts = self._parse_stmt_list()
        self._expect("RBRACE", "to close jersey block")
        return JerseyNode(stmts=stmts)

    # stmt_list := { stmt }
    def _parse_stmt_list(self) -> List[object]:
        stmts = []
        while True:
            tok = self._peek()
            if not tok or tok.type in ("RBRACE", "EOF"):
                break
            stmts.append(self._parse_stmt())
        return stmts

    # stmt alternatives
    def _parse_stmt(self):
        tok = self._peek()
        if not tok:
            raise ParserError("Unexpected EOF inside jersey block")

        if tok.type == "TEAM":
            return self._parse_team()
        if tok.type == "PRIMARY":
            return self._parse_color(kind="primary")
        if tok.type == "SECONDARY":
            return self._parse_color(kind="secondary")
        if tok.type == "TERTIARY":
            return self._parse_color(kind="tertiary")
        if tok.type == "NUMBER":
            return self._parse_number()
        if tok.type == "PLAYER":
            return self._parse_player()
        if tok.type == "SPONSOR":
            return self._parse_sponsor()
        if tok.type == "FONT":
            return self._parse_font()
        if tok.type == "PLAYERSIZE":
            return self._parse_player_size()
        if tok.type == "NUMBERSIZE":
            return self._parse_number_size()
        if tok.type == "TEAMSIZE":
            return self._parse_team_size()
        if tok.type == "SPONSORSIZE":
            return self._parse_sponsor_size()
        if tok.type == "PATTERN":
            return self._parse_pattern()
        if tok.type == "PATTERNCOLOR":
            return self._parse_color(kind="pattern_color")

        raise ParserError(f"Unexpected token {tok.type} at line {tok.line}, col {tok.col}")

    # team: "Spartan FC";
    def _parse_team(self):
        self._expect("TEAM", "")
        self._expect("COLON", "after 'team'")
        s = self._expect("STRING", "for team name").value
        self._expect("SEMI", "after team string")
        return TeamNode(name=self._unquote(s))

    # primary/secondary: #RRGGBB;
    def _parse_color(self, kind: str):
        if kind == "primary":
            self._expect("PRIMARY", "")
        elif kind == "secondary":
            self._expect("SECONDARY", "")
        elif kind == "tertiary":
            self._expect("TERTIARY", "")
        elif kind == "pattern_color":
            self._expect("PATTERNCOLOR", "")
        else:
            raise ParserError(f"Unknown color kind: {kind}")
        self._expect("COLON", f"after '{kind}'")
        val_tok = self._expect("COLOR", f"for {kind} color")
        self._expect("SEMI", f"after {kind} color")
        return ColorNode(kind=kind, value=val_tok.value)

    # number: 23;
    def _parse_number(self):
        self._expect("NUMBER", "")
        self._expect("COLON", "after 'number'")
        n = int(self._expect("INT", "for jersey number").value)
        self._expect("SEMI", "after number")
        return NumberNode(value=n)

    # player: "BEN";
    def _parse_player(self):
        self._expect("PLAYER", "")
        self._expect("COLON", "after 'player'")
        s = self._expect("STRING", "for player name").value
        self._expect("SEMI", "after player")
        return PlayerNode(name=self._unquote(s))

    # sponsor: "SJSU";
    def _parse_sponsor(self):
        self._expect("SPONSOR", "")
        self._expect("COLON", "after 'sponsor'")
        s = self._expect("STRING", "for sponsor").value
        self._expect("SEMI", "after sponsor")
        return SponsorNode(name=self._unquote(s))

    # font: IDENT | "Some Font";
    def _parse_font(self):
        self._expect("FONT", "")
        self._expect("COLON", "after 'font'")
        tok = self._match("IDENT", "STRING")
        if not tok:
            got = self._peek()
            raise ParserError(f"Expected font name at line {got.line}, col {got.col}")
        self._expect("SEMI", "after font")
        name = self._unquote(tok.value) if tok.type == "STRING" else tok.value
        return FontNode(name=name)
    
    # fontsize: INT
    def _parse_player_size(self):
        self._expect("PLAYERSIZE", "")
        self._expect("COLON", "after 'player_size'")
        n = int(self._match("INT", "for player_size").value)
        self._expect("SEMI", "after player_size")
        return PlayerSizeNode(value=n)
    
    def _parse_number_size(self):
        self._expect("NUMBERSIZE", "")
        self._expect("COLON", "after 'number_size'")
        n = int(self._match("INT", "for number_size").value)
        self._expect("SEMI", "after number_size")
        return NumberSizeNode(value=n)
    
    def _parse_team_size(self):
        self._expect("TEAMSIZE", "")
        self._expect("COLON", "after 'team_size'")
        n = int(self._match("INT", "for team_size").value)
        self._expect("SEMI", "after team_size")
        return TeamSizeNode(value=n)
    
    def _parse_sponsor_size(self):
        self._expect("SPONSORSIZE", "")
        self._expect("COLON", "after 'sponsor_size'")
        n = int(self._match("INT", "for sponsor_size").value)
        self._expect("SEMI", "after sponsor_size")
        return SponsorSizeNode(value=n)

    # pattern: stripes(7,14);
    def _parse_pattern(self):
        self._expect("PATTERN", "")
        self._expect("COLON", "after 'pattern'")
        ident = self._expect("IDENT", "for pattern ident").value
        args = []
        if self._match("LPAREN"):
            # arg_list? -> (arg {"," arg})?
            if self._peek() and self._peek().type not in ("RPAREN",):
                args.append(self._parse_arg())
                while self._match("COMMA"):
                    args.append(self._parse_arg())
            self._expect("RPAREN", "to close pattern args")
        self._expect("SEMI", "after pattern")
        return PatternNode(ident=ident, args=args)

    def _parse_arg(self):
        tok = self._match("INT", "COLOR", "STRING", "IDENT")
        if not tok:
            got = self._peek()
            raise ParserError(f"Expected argument at line {got.line}, col {got.col}")
        if tok.type == "INT":
            return int(tok.value)
        return self._unquote(tok.value) if tok.type == "STRING" else tok.value

    @staticmethod
    def _unquote(s: str) -> str:
        if len(s) >= 2 and s[0] == s[-1] == '"':
            return bytes(s[1:-1], "utf-8").decode("unicode_escape")
        return s
