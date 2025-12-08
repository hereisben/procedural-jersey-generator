# 🧵 Procedural Jersey Generator

### _A Domain-Specific Language (DSL) & Compiler for Procedural Soccer Kit Design_

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/hereisben/procedural-jersey-generator)

⚽ **Procedural Jersey Generator** is a miniature compiler that turns a small domain-specific language (DSL) into fully rendered SVG soccer jerseys.  
Built for **CS 152 — Programming Languages**, San José State University.

---

## 👨‍💻 Author

**Ben Nguyen**  
CS 152 – Fall 2025  
San José State University

---

## 📖 Overview

This project implements a full compiler pipeline:

```

Lexer → Parser → AST → Semantic Checker → Interpreter → SVG Renderer

```

Users write jersey designs in a custom declarative DSL.  
The compiler parses, validates, and renders a complete jersey as SVG.

Example DSL:

```txt
jersey {
        primary: #E5A823;
        secondary: #0055A2;
        tertiary: #ffffff;
        pattern_color: #0055A2;
        font: "Sport Scholars Outline";
        team: "Spartan FC", (365, 190), 18;
        player: "BEN", (365, 85), 26;
        number: 23, (365, 155), 75;
        sponsor: "SJSU", (115, 125), 35;
        pattern: stripes(7,22);
      }
```

---

## 🌐 Web Playground

The project includes a full interactive IDE:

- Real-time SVG rendering
- Two-way binding between DSL editor and form UI
- Pattern configuration menus
- Sticky layout for long pages
- AI jersey generation

Run:

```bash
python web/app.py
```

Visit:

```
http://localhost:5000
```

---

## 🤖 AI Design Assistant

The system contains an AI-powered jersey generator:

1. User writes a natural language prompt
2. Backend produces strict JSON
3. `json_to_dsl.py` converts JSON → DSL
4. Compiler renders the jersey

Example prompt:

> “Create a Juventus away kit with gold trim and waves.”

AI returns a complete, valid, compiler-safe design:

- Colors
- Text placements
- Pattern + args
- Font
- Coordinates + sizes

---

## 🎨 Supported Patterns

### Geometric

```txt
stripes(count, thickness)
hoops(count, thickness)
sash(angle, width)
checker(cell_w, cell_h)
half_split("vertical" | "horizontal", ratio)
gradient("up" | "down" | "center", intensity)
```

### Organic / Artistic

```txt
brush(thickness, roughness)
waves(amplitude, wavelength)
camo(cell_size, variance)
```

All patterns are clipped to jersey geometry and validated semantically.

---

## 🎨 Color Model

```txt
primary: #RRGGBB;
secondary: #RRGGBB;
tertiary: #RRGGBB;
pattern_color: #RRGGBB;
```

Semantic checks ensure:

- All colors are provided
- HEX normalization
- Optional contrast rules

---

## 🔡 Text Placement System

Each text element includes coordinates + size:

```txt
team:    "NAME", (x, y), size;
player:  "NAME", (x, y), size;
number:  N, (x, y), size;
sponsor: "NAME", (x, y), size;
```

Renderer uses an embedded WOFF2 font (`SportScholars-Outline.woff2`)
so exported SVGs look identical everywhere.

---

## 🧱 Compiler Architecture

### Lexer

Regex tokenizer for keywords, identifiers, punctuation, HEX colors, numbers, strings.

### Parser

Recursive-descent → typed AST (`ast/nodes.py`).

### Semantic Checker

- Required field validation
- Duplicate detection
- Pattern argument ranges
- Text placement validation
- Color normalization
- Builds a `JerseySpec`

### Interpreter / SVG Renderer

- Jersey geometry (front/back)
- Clip paths
- All patterns (geometric + organic)
- Embedded fonts
- Metadata insertion
- Deterministic randomness for digital camo

---

## 🔁 JSON → DSL Converter

Strict conversion ensures:

- Correct field ordering
- Semicolons
- Normalized names (e.g., `pattern_color`)
- Valid arguments
- AI-safe layout

Example:

```json
{
  "team": { "name": "Spartan FC", "x": 260, "y": 80, "size": 22 },
  "pattern": { "type": "waves", "args": [50, 140] }
}
```

→

```txt
team: "Spartan FC", (260, 80), 22;
pattern: waves(50, 140);
```

---

## 📁 Project File Tree

```
procedural-jersey-generator/
├── docs/
│   └── grammar.ebnf
├── examples/
├── src/
│   ├── ast/
│   │   ├── __init__.py
│   │   └── nodes.py
│   ├── interpreter/
│   │   ├── __init__.py
│   │   ├── json_to_dsl.py
│   │   └── svg.py
│   ├── lexer/
│   │   ├── __init__.py
│   │   └── tokenizer.py
│   ├── parser/
│   │   ├── __init__.py
│   │   └── parser.py
│   ├── semantic/
│   │   ├── __init__.py
│   │   └── checks.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── manual_json_to_dsl.py
│   ├── __init__.py
│   ├── grammar.py
│   └── main.py
├── web/
│   ├── static/
│   │   ├── fonts/
│   │   │   ├── SportScholars-Outline.woff
│   │   │   └── SportScholars-Outline.woff2
│   │   └── index.html
│   └── app.py
├── LICENSE
├── README.md
├── requirements.txt
└── wsgi.py
```

---

## 🚀 CLI Usage

Render tokens:

```bash
python -m src.main examples/basic.jersey --tokens
```

Render SVG:

```bash
python -m src.main examples/basic.jersey --render-svg --out examples/basic.svg
```

Save tokens to a file:

```bash
python -m src.main examples/basic.jersey --tokens > examples/basic.jersey.tokens.txt
```

Render all examples:

```bash
for f in examples/*.jersey; do
  python -m src.main "$f" --render-svg --out "${f%.jersey}.svg"
done
```

---

## 📜 License

Released under the repository’s `LICENSE` file.

Exported SVGs include embedded metadata:

```
© 2025 Ben Nguyen — Procedural Jersey Generator
```
