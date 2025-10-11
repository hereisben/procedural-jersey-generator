from dataclasses import dataclass
import re
from typing import List

KEYWORDS = {
    "jersey": "JERSEY",
    "team": "TEAM",
    "primary": "PRIMARY",
    "secondary": "SECONDARY",
    "pattern": "PATTERN",
    "number": "NUMBER",
    "player": "PLAYER",
    "sponsor": "SPONSOR",
    "font": "FONT",
}

SYMBOLS = {
    '{': 'LBRACE', '}': 'RBRACE', '(': 'LPAREN', ')': 'RPAREN',
    ';': 'SEMI', ':': 'COLON', ',': 'COMMA'
}

COLOR_RE = re.compile(r"#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?\b")
INT_RE   = re.compile(r"[0-9]+\b")
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\b")
STR_RE   = re.compile(r'"(?:\\.|[^"\\\n])*"')

LINE_COMMENT_RE  = re.compile(r"//.*?(?=\n|$)")
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
WHITESPACE_RE = re.compile(r"[ \t\r\n]+")

@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, src: str):
        self.src = src
        self.pos = 0
        self.line = 1
        self.col = 1

    def _advance(self, n: int):
        segment = self.src[self.pos:self.pos+n]
        line_breaks = segment.count('\n')
        if line_breaks:
            self.line += line_breaks
            last_nl_idx = segment.rfind('\n')
            self.col = len(segment) - last_nl_idx
        else:
            self.col += n
        self.pos += n

    def _match(self, pattern: re.Pattern):
        m = pattern.match(self.src, self.pos)
        return m.group(0) if m else None

    def tokens(self) -> List[Token]:
        toks: List[Token] = []
        n = len(self.src)
        while self.pos < n:
            # whitespace
            m = self._match(WHITESPACE_RE)
            if m:
                self._advance(len(m))
                continue
            # comments
            m = self._match(LINE_COMMENT_RE)
            if m:
                self._advance(len(m))
                continue
            m = self._match(BLOCK_COMMENT_RE)
            if m:
                self._advance(len(m))
                continue

            if self.pos >= n:
                break

            start_line, start_col = self.line, self.col
            ch = self.src[self.pos]

            # symbols
            if ch in SYMBOLS:
                toks.append(Token(SYMBOLS[ch], ch, start_line, start_col))
                self._advance(1)
                continue

            # string
            m = self._match(STR_RE)
            if m:
                toks.append(Token('STRING', m, start_line, start_col))
                self._advance(len(m))
                continue

            # color
            m = self._match(COLOR_RE)
            if m:
                toks.append(Token('COLOR', m, start_line, start_col))
                self._advance(len(m))
                continue

            # int
            m = self._match(INT_RE)
            if m:
                toks.append(Token('INT', m, start_line, start_col))
                self._advance(len(m))
                continue

            # ident / keyword
            m = self._match(IDENT_RE)
            if m:
                typ = KEYWORDS.get(m, 'IDENT')
                toks.append(Token(typ, m, start_line, start_col))
                self._advance(len(m))
                continue

            bad = self.src[self.pos]
            raise LexerError(f"Unexpected character '{bad}' at {start_line}:{start_col}")

        toks.append(Token('EOF', '', self.line, self.col))
        return toks
