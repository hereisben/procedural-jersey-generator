
import argparse
from pathlib import Path

from .lexer.tokenizer import Lexer
from .grammar import print_grammar
from .parser.parser import Parser
from .ast.nodes import JerseyNode

def _lex(text: str):
    try:
        lx = Lexer(text)
        if hasattr(lx, "tokens"):
            toks = list(lx.tokens())
            if toks:
                return toks
    except TypeError:
        pass

    # Fallback: no-arg constructor + tokenize(text)
    lx = Lexer()
    if hasattr(lx, "tokenize"):
        return lx.tokenize(text)

    raise RuntimeError("Lexer interface not recognized. Expected .tokens() or .tokenize(text).")

def dump_tokens(tokens, out_path: Path | None):
    for t in tokens:
        lexeme = getattr(t, "lexeme", getattr(t, "value", ""))
        line = getattr(t, "line", "?")
        col  = getattr(t, "col", "?")
        print(f"{line}:{col}\t{t.type}\t{lexeme}")
    if out_path:
        with out_path.open("w", encoding="utf-8") as f:
            for t in tokens:
                lexeme = getattr(t, "lexeme", getattr(t, "value", ""))
                line = getattr(t, "line", "?")
                col  = getattr(t, "col", "?")
                f.write(f"{line}:{col}\t{t.type}\t{lexeme}\n")
        print(f"\n✅ Token list written to {out_path}")

def parse_file(text: str) -> JerseyNode:
    tokens = _lex(text)
    parser = Parser(tokens)
    return parser.parse()

def main():
    ap = argparse.ArgumentParser(
        prog="python -m src.main",
        description="Jersey DSL CLI: show grammar, tokenize, and parse to AST",
    )
    ap.add_argument("file", nargs="?", help=".jersey file to process")
    ap.add_argument("--show-grammar", action="store_true", help="print EBNF grammar and exit")
    ap.add_argument("--tokens", action="store_true", help="print tokens to stdout")
    ap.add_argument("--write-tokens", action="store_true", help="also write <file>.tokens.txt")
    ap.add_argument("--show-ast", action="store_true", help="parse and pretty-print AST")

    args = ap.parse_args()

    if args.show_grammar and not args.file:
        print_grammar()
        return

    if not args.file:
        ap.print_usage()
        print("\nExamples:")
        print("  python -m src.main --show-grammar")
        print("  python -m src.main examples/basic.jersey --tokens")
        print("  python -m src.main examples/basic.jersey --show-ast --write-tokens")
        return

    path = Path(args.file)
    text = path.read_text(encoding="utf-8")

    tokens = None
    if args.tokens or args.write_tokens or args.show_ast:
        tokens = _lex(text)

    if args.tokens or args.write_tokens:
        out_path = path.with_suffix(path.suffix + ".tokens.txt") if args.write_tokens else None
        dump_tokens(tokens, out_path)

    if args.show_ast:
        jersey_ast: JerseyNode = Parser(tokens).parse()
        from pprint import pprint
        pprint(jersey_ast)

    if args.show_grammar:
        print("\n=== EBNF Grammar ===\n")
        print_grammar()

if __name__ == "__main__":
    main()
