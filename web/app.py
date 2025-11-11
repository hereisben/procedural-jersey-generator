# web/app.py
from flask import Flask, request, jsonify
from pathlib import Path
import sys

# Allow import src.*
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.lexer.tokenizer import Lexer
from src.parser.parser import Parser
from src.semantic.checks import validate_jersey, SemanticError
from src.interpreter.svg import render_svg, RenderOptions

app = Flask(__name__)

def compile_and_render(jersey_text: str) -> str:
    toks = Lexer(jersey_text).tokens()
    ast = Parser(toks).parse()
    spec = validate_jersey(ast)
    svg = render_svg(spec, RenderOptions(show_debug=False))
    return svg

@app.post("/api/render")
def api_render():
    data = request.get_json(silent=True) or {}
    jersey_text = data.get("source", "")
    if not jersey_text.strip():
        return jsonify({"ok": False, "error": "Empty input"}), 400
    try:
        svg = compile_and_render(jersey_text)
        return jsonify({"ok": True, "svg": svg})
    except SemanticError as e:
        return jsonify({"ok": False, "error": f"Semantic error: {e}"}), 400
    except SyntaxError as e:
        return jsonify({"ok": False, "error": f"Syntax error: {e}"}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": f"Internal error: {e}"}), 500

@app.get("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
