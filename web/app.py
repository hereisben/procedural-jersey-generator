# web/app.py
from flask import Flask, request, jsonify
from pathlib import Path
import sys
import os
from groq import Groq
import json


# Allow import src.*
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.lexer.tokenizer import Lexer
from src.parser.parser import Parser
from src.semantic.checks import validate_jersey, SemanticError
from src.interpreter.svg import render_svg, RenderOptions
from src.interpreter.json_to_dsl import jersey_json_to_dsl
from dotenv import load_dotenv
load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
if not groq_client.api_key:
    raise RuntimeError("Missing GROQ_API_KEY in .env")

AI_SYSTEM_PROMPT = """
You are a soccer jersey design assistant.

Your ONLY job:
1. Read the user's natural language request for a jersey.
2. Return ONE JSON object that follows EXACTLY this schema:

{
    "team": string,          // required
    "player": string,        // required
    "number": integer,       // required
    "sponsor": string,       // required
    "font": string,          // required
    "primary": string,       // required, hex color like "#000000"
    "secondary": string,     // required, hex color like "#FFFFFF"
    "tertiary": string,      // required, hex accent color
    "pattern_color": string,  // required, hex color for pattern
    "player_size": integer,   // required, from 8 to 100, pick reasonable font size
    "number_size": integer,   // required, from 8 to 100, pick reasonable font size
    "team_size": integer,     // required, from 8 to 100, pick reasonable font size
    "sponsor_size": integer,   // required, from 8 to 100, pick reasonable font size
    "pattern": {
        "type": string,        // one of: "stripes", "hoops", "sash", "solid"
        "args": array          // numbers for pattern parameters, e.g. stripes(count, thickness) -> [9,18]
},

  "source": {
    "fromText": boolean,
    "fromImage": boolean,
    "imageAnalysisConfidence": number
  },

  "approximationNote": string
}

Rules:
- OUTPUT MUST BE VALID JSON, NO COMMENTS, NO EXTRA TEXT.
- Use double quotes for all keys and string values.
- All colors MUST be valid 7-character hex codes: "#RRGGBB".
- If the user doesn't specify team name, pick a reasonable name.
- If user doesn't specify sponsor, choose a short fake sponsor.
- If user doesn't specify font, use "Sport Scholars Outline".

Pattern rules:
- "stripes": args = [count, thickness]
- "hoops":   args = [count, thickness]
- "sash":    args = [angleDegrees, widthPixels]
- "solid":   args = []

PLAYER NAME RULES:
- If the user specifies a player, use that name.
- If user DOES NOT specify a player, set player = "PLAYER".
- Always return player in uppercase (e.g. "MESSI", "LEWANDOWSKI").

Return ONLY the JSON object, nothing else.
"""

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
        "pattern_color": "#000000",
        "player_size": 26,
        "number_size": 75,
        "team_size": 18,
        "sponsor_size": 35,
        "source": {
            "fromText": bool(message),
            "fromImage": bool(image_path),
            "imageAnalysisConfidence": 0.78,
        },
        "approximationNote": (
            "Approximation of the Juventus 23/24 away kit using flat stripes and simple colors."
        ),
    }

def real_ai_suggest_jersey(message: str) -> dict:
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": AI_SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
    )

    raw = completion.choices[0].message.content
    try:
        return json.loads(raw)
    except Exception as e:
        raise RuntimeError(f"Groq JSON parse failed: {e}\nRaw: {raw}")


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

    try:
        ai_json = real_ai_suggest_jersey(message=prompt)
    except Exception as e:
        # fallback
        # ai_json = fake_ai_suggest_jersey(message=prompt, image_path=None)
        return jsonify(ok=False, error=f"AI failed: {e}"), 500

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
