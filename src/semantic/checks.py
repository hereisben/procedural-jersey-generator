# src/semantic/checks.py
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple, Union
from ..ast.nodes import (
    JerseyNode, TeamNode, ColorNode, NumberNode, PlayerNode,
    SponsorNode, FontNode, PatternNode, Stmt
)

class SemanticError(Exception):
    pass

@dataclass
class JerseySpec:
    team: Optional[str] = None
    primary: Optional[str] = None
    secondary: Optional[str] = None
    tertiary: Optional[str] = None
    patterncolor: Optional[str] = None
    number: Optional[int] = None
    player: Optional[str] = None
    sponsor: Optional[str] = None
    font: Optional[str] = None
    pattern: Optional[Tuple[str, List[Union[int, str]]]] = None  # (ident, args)

def _hex6(c: str) -> str:
    c = c.upper()
    if len(c) == 4:  # #RGB → #RRGGBB
        return f"#{c[1]*2}{c[2]*2}{c[3]*2}"
    return c

def validate_jersey(ast: JerseyNode) -> JerseySpec:
    seen: Dict[str, int] = {}
    spec = JerseySpec()

    for s in ast.stmts:
        if isinstance(s, TeamNode):
            _check_dup("team", seen)
            if not s.name.strip():
                raise SemanticError("team: name must be non-empty")
            spec.team = s.name.strip()

        elif isinstance(s, ColorNode):
            # allow: primary | secondary | tertiary | patterncolor
            key = s.kind
            if key not in ("primary", "secondary", "tertiary", "patterncolor"):
                raise SemanticError(f"Unknown color kind: {key}")
            _check_dup(key, seen)
            setattr(spec, key, _hex6(s.value))

        elif isinstance(s, NumberNode):
            _check_dup("number", seen)
            if s.value < 0 or s.value > 99:
                raise SemanticError("number: must be between 0 and 99")
            spec.number = s.value

        elif isinstance(s, PlayerNode):
            _check_dup("player", seen)
            spec.player = s.name.strip()

        elif isinstance(s, SponsorNode):
            _check_dup("sponsor", seen)
            spec.sponsor = s.name.strip()

        elif isinstance(s, FontNode):
            _check_dup("font", seen)
            spec.font = s.name.strip()

        elif isinstance(s, PatternNode):
            _check_dup("pattern", seen)
            ident = s.ident.strip()
            if not ident:
                raise SemanticError("pattern: ident must be non-empty")
            spec.pattern = (ident, s.args[:])

        else:
            raise SemanticError(f"Unknown statement: {type(s).__name__}")

    # required
    missing = [k for k in ("primary", "secondary", "tertiary") if getattr(spec, k) is None]
    if missing:
        raise SemanticError(f"Missing required field(s): {', '.join(missing)}")

    # defaults
    spec.team   = spec.team or "Unnamed FC"
    spec.player = spec.player or "PLAYER"
    spec.font   = spec.font or "Arial"
    spec.number = spec.number if spec.number is not None else 10

    return spec

def _check_dup(key: str, seen: Dict[str, int]):
    if key in seen:
        raise SemanticError(f"Duplicate declaration for '{key}'")
    seen[key] = 1
