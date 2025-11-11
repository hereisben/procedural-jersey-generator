import argparse
from pathlib import Path

from .lexer.tokenizer import Lexer
from .grammar import print_grammar
from .parser.parser import Parser
from .ast.nodes import JerseyNode
from .semantic.checks import validate_jersey, SemanticError
from .interpreter.svg import render_svg, RenderOptions


def _lex(text: str):
    lx = Lexer(text)
    toks = lx.tokens()
    return list(toks)

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
        description="Jersey DSL CLI: show grammar, tokenize, parse to AST, and render SVG",
    )
    ap.add_argument("file", nargs="?", help=".jersey file to process")
    ap.add_argument("--show-grammar", action="store_true", help="print EBNF grammar and exit")
    ap.add_argument("--tokens", action="store_true", help="print tokens to stdout")
    ap.add_argument("--write-tokens", action="store_true", help="also write <file>.tokens.txt (or --out)")
    ap.add_argument("--show-ast", action="store_true", help="parse and pretty-print AST")
    ap.add_argument("--render-svg", action="store_true", help="render jersey to SVG")
    ap.add_argument("--out", help="output path for artifacts (.tokens.txt or .svg)")

    args = ap.parse_args()

    # Case 1: Just show grammar and no file
    if args.show_grammar and not args.file:
        print_grammar()
        return

    # If no file is provided, show usage + examples
    if not args.file:
        ap.print_usage()
        print("\nExamples:")
        print("  python -m src.main --show-grammar")
        print("  python -m src.main examples/basic.jersey --tokens")
        print("  python -m src.main examples/striped.jersey --render-svg --out examples/striped.svg")
        return

    path = Path(args.file)
    text = path.read_text(encoding="utf-8")

    # Prepare tokens if any downstream step needs them
    needs_tokens = args.tokens or args.write_tokens or args.show_ast or args.render_svg
    tokens = _lex(text) if needs_tokens else None

    # Tokens output
    if args.tokens or args.write_tokens:
        # If --write-tokens and --out given, respect --out; else <file>.tokens.txt
        out_path = None
        if args.write_tokens:
            out_path = Path(args.out) if args.out else path.with_suffix(path.suffix + ".tokens.txt")
        dump_tokens(tokens, out_path)

    # Parse to AST if needed
    jersey_ast: JerseyNode | None = None
    if args.show_ast or args.render_svg:
        jersey_ast = Parser(tokens).parse()
        if args.show_ast:
            from pprint import pprint
            pprint(jersey_ast)

    # Render SVG if requested
    if args.render_svg:
        try:
            spec = validate_jersey(jersey_ast)
        except SemanticError as e:
            print(f"Semantic error: {e}")
            return
        svg = render_svg(spec, RenderOptions(show_debug=False))
        out_svg = Path(args.out) if args.out else path.with_suffix(".svg")
        out_svg.write_text(svg, encoding="utf-8")
        print(f"✅ SVG written to {out_svg}")

    # Optionally print grammar even when a file is provided
    if args.show_grammar:
        print("\n=== EBNF Grammar ===\n")
        print_grammar()

if __name__ == "__main__":
    main()
