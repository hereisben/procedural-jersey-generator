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
from src.interpreter.json_to_dsl import jersey_json_to_dsl

app = Flask(__name__)

def compile_and_render(jersey_text: str) -> str:
    toks = Lexer(jersey_text).tokens()
    ast = Parser(toks).parse()
    spec = validate_jersey(ast)
    svg = render_svg(spec, RenderOptions(show_debug=False))
    return svg

def compile_dsl_to_svg(dsl_code: str) -> str:
    return compile_and_render(dsl_code)

def fake_ai_suggest_jersey(message: str, image_path: str | None = None) -> dict:
    """
    Dummy AI: nhận message + image_path, trả về JSON jersey suggestion
    theo spec của project.
    Sau này chỉ cần thay thân hàm này bằng call OpenAI / model thật.
    """
    # Tạm thời ignore message + image_path,
    # hard-code Juventus away kit như bạn đang làm.
    return {
        "team": "Juventus",
        "player": "VLAHOVIC",
        "number": 9,
        "sponsor": "Jeep",
        "font": "Sport Scholars Outline",
        "primary": "#fefefe",
        "secondary": "#000000",
        "tertiary": "#d4a856",
        "pattern": {
            "type": "stripes",
            "args": [9, 18],
        },
        "patternColor": "#000000",
        "source": {
            "fromText": bool(message),
            "fromImage": bool(image_path),
            "imageAnalysisConfidence": 0.78,
        },
        "approximationNote": (
            "Approximation of the Juventus 23/24 away kit using flat stripes and simple colors."
        ),
    }



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

@app.route("/api/ai/chat-jersey", methods=["POST"])
def ai_chat_jersey():
    data = request.get_json(force=True, silent=True) or {}

    prompt = (data.get("prompt") or "").strip()
    current_dsl = data.get("currentDsl") or ""

    if not prompt:
        return jsonify(ok=False, error="Missing prompt"), 400

    ai_json = fake_ai_suggest_jersey(message=prompt, image_path=None)

    dsl_code = jersey_json_to_dsl(ai_json)

    try:
        svg_xml = compile_dsl_to_svg(dsl_code)
    except Exception as e:
        return jsonify(
            ok=False,
            error="Failed to compile DSL to SVG",
            details=str(e),
            dsl=dsl_code,
        ), 400

    return jsonify(
        ok=True,
        spec=ai_json,  
        dsl=dsl_code,
        svg=svg_xml,
        approximationNote=ai_json.get("approximationNote", ""),
    )




if __name__ == "__main__":
    app.run(debug=True, port=5000)
