# Project Progress — Procedural Jersey Generator (Draft Notes)

## September 10, 2025

Today I wrote and turned in the full project proposal for the jersey DSL. I tried to explain the main idea, why I care about soccer kits, and how the pipeline will go from grammar + parsing to SVG jerseys. First time I really think about the language as `jersey { ... }` with short text lines that turn into visuals. It helped me see context-free grammar and parsing are not just theory, they can end up as real pictures. Still a bit hard to balance between keeping the grammar simple and making it expressive, and also writing about grammar in a way that doesn’t sound too dry.

## October 9, 2025

Today I mostly worked on structure and the lexer. I set up the project folders like a small compiler: `lexer/`, `parser/`, `semantic/`, `interpreter/`, and put the EBNF in `docs/grammar.ebnf`. Then I wrote `src/lexer/tokenizer.py` with regex patterns for keywords, symbols, colors, strings, numbers, plus `src/main.py` as a CLI so I can run on `.jersey` files and print tokens. I tested on `examples/basic.jersey` and the tokens looked right. I also learned more about how the order of regex rules matters, how to track line/column for future error messages, and I fought with Python imports when switching between `python -m src.main` and direct run.

## October 10, 2025

Today I cleaned up the lexer interface. I changed `Lexer.tokens()` to return a list of `Token` instead of a generator and added type hints so the code is easier to read and my IDE stops yelling. I simplified `_lex()` in `main.py` to use this new API and tested again with `python -m src.main examples/basic.jersey --tokens`. Learned a few type-hint issues, fixed some argparse warnings, and got a clearer sense of how the CLI will connect to lexer, parser, and AST later.

## November 11, 2025

Today was about semantics and starting the SVG renderer. I added semantic checks in `src/semantic/checks.py` to catch duplicate fields, missing fields, and normalize colors. I created a `JerseySpec` dataclass and a `SemanticError`. Then I wrote the first SVG renderer in `src/interpreter/svg.py` with stripes, hoops, sash, team/sponsor text, and debug outlines, and wired it into `src/main.py` with flags like `--render-svg`. Now the full chain runs and I can finally see a jersey SVG appear. Still some balancing between CLI flexibility and consistent color handling.

## November 12, 2025

Today I extended the DSL and put the compiler on the web. Added optional `patterncolor` to the language and updated lexer/parser/semantic + renderer to use a shared `clipPath` and better layering. Then I created a Flask backend (`web/app.py`) with `/api/render` and a small frontend in `web/static/index.html` with an editor, presets, and live preview. Now I can type DSL in the browser and see the jersey appear. Learned a lot about hooking a compiler backend to an API, and dealt with Flask static paths and JSON edge cases.

## November 13, 2025

Today I added SVG metadata and polished the UI. Put `<metadata>` and `<desc>` tags inside SVG for credit, added a footer in the playground, and redesigned the frontend into a 3-column layout. Added more presets and improved spacing and responsiveness. Mostly UI work but it makes the whole thing feel more “real”.

## November 14, 2025

Today I tried to make the playground feel smooth to use. Finished the interactions, added nicer default colors, reorganized the form layout, added sponsor input, and implemented two-way binding between the form and the DSL editor. Added debouncing so SVG updates don’t flash. Also fixed the white flash issue by reusing the same SVG node. Finally deployed the Flask app somewhere I can reach from a browser.

## November 21, 2025

Today I upgraded the color model and the jersey look. Added a third color `tertiary` into the DSL and made primary, secondary, tertiary required. Used tertiary as accent color for trims and all text. Cleaned up jersey body vs shorts, disabled patterns on shorts, tightened clipping, and added collar geometry. Updated the playground with new color pickers and updated the small parser/serializer in the frontend. This made the DSL feel more complete but also broke old files that didn’t have tertiary.

## November 22, 2025

Today I improved geometry/typography and added the first real AI flow. Refined jersey outlines and text sizes/weights. Embedded the font into SVG using base64 + inline `<style>`. Updated the playground to use the new font. Then wired an AI pipeline: natural language → JSON → DSL → SVG. Wrote `jersey_json_to_dsl()` and added an AI chat box in the UI. Fixed sash geometry and returned `spec`, `dsl`, `svg`, `approximationNote` together. Learned a lot about making AI output go through a strict compiler.

## November 25, 2025

Today I added text size fields into the DSL (`player_size`, `number_size`, `team_size`, `sponsor_size`) and propagated them through lexer → parser → AST → semantic → renderer. Cleaned up `pattern_color` naming. Fixed parser errors caused by missing semicolons in AI DSL output. Updated the AI endpoint to give clearer errors, updated bindings in the UI, and fixed static file paths. Finally confirmed the full pipeline: AI → JSON → DSL → compiler → SVG → browser.

## November 26, 2025

Today I made the AI pipeline more robust and added explicit text placement. Added backend fallback for `pattern_color`, strengthened the AI system prompt, fixed a front-end naming bug, and added coordinates + size to all text statements in the DSL. Updated parser/AST to use a `TextPlacement` dataclass, updated semantic checks, updated SVG renderer, and synced everything with the playground UI. Tightened the AI prompt to enforce JSON-only and added a contrast rule when patterns exist. The hardest part was updating the mini DSL parser and making sure AI output didn’t wrap JSON with explanations.

## December 4, 2025

Today I added two new patterns and improved usability. Implemented a `checker` pattern with cell width/height, added semantic checks, UI controls, AI support, and JSON→DSL support. Fixed the `clamp` helper for bad numbers. Added a `gradient` pattern with direction + intensity and implemented it in SVG with opacity layering. Updated the AI prompt and made the UI panels sticky so scrolling is easier.

## December 5, 2025

Today I added a batch of new patterns: `brush`, `waves`, `digital_camo`, and `halftone_dots`. Each one needed DSL entries, semantic ranges, SVG rendering, UI controls, and JSON→DSL + AI prompt updates. Learned that simple math (jitters, sine waves, grids, opacity) can create rich effects without images. Also constantly had to keep pattern naming, arg order, and schema aligned across all layers.

## December 6, 2025

Today I finished the pattern set and added final polish. Implemented `topo` (contour rings) and `half_split` (vertical/horizontal ratio). Tuned the geometry so it feels like a real jersey front/back. Added word-based text wrapping so long names break naturally. Added PNG export using SVG → canvas → PNG download. Mostly polishing: tuning distortion, making wrapping look clean, and ensuring PNG matches the SVG preview.
