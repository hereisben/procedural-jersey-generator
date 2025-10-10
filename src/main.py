import sys
from .lexer.tokenizer import Lexer
from .grammar import print_grammar

USAGE = """Usage:
  python -m src.main <file.jersey>    # tokenize and print tokens
  python -m src.main --show-grammar   # print EBNF grammar
"""

def main():
    if len(sys.argv) != 2:
        print(USAGE)
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "--show-grammar":
        print_grammar()
        return

    path = arg
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()

    print(f"\n=== Tokenizing {path} ===\n")
    for tok in Lexer(src).tokens():
        print(tok)

    out_path = path + ".tokens.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        for tok in Lexer(src).tokens():
            f.write(f"{tok.line}:{tok.col}\t{tok.type}\t{tok.lexeme}\n")

    print(f"\n✅ Token list written to {out_path}")

if __name__ == "__main__":
    main()
