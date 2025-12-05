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
class TextPlacement:
    text: str | int
    x: int
    y: int
    size: int

@dataclass
class JerseySpec:
    team: Optional[TextPlacement] = None
    primary: Optional[str] = None
    secondary: Optional[str] = None
    tertiary: Optional[str] = None
    pattern_color: Optional[str] = None
    number: Optional[TextPlacement] = None
    player: Optional[TextPlacement] = None
    sponsor: Optional[TextPlacement] = None
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
            spec.team = TextPlacement(text=s.name.strip(), x=s.x, y=s.y, size=s.size)

        elif isinstance(s, ColorNode):
            # allow: primary | secondary | tertiary | pattern_color
            key = s.kind
            if key not in ("primary", "secondary", "tertiary", "pattern_color"):
                raise SemanticError(f"Unknown color kind: {key}")
            _check_dup(key, seen)
            setattr(spec, key, _hex6(s.value))

        elif isinstance(s, NumberNode):
            _check_dup("number", seen)
            if s.value < 0 or s.value > 99:
                raise SemanticError("number: must be between 0 and 99")
            spec.number = TextPlacement(text=s.value, x=s.x, y=s.y, size=s.size)

        elif isinstance(s, PlayerNode):
            _check_dup("player", seen)
            spec.player = TextPlacement(text=s.name.strip(), x=s.x, y=s.y, size=s.size)

        elif isinstance(s, SponsorNode):
            _check_dup("sponsor", seen)
            spec.sponsor = TextPlacement(text=s.name.strip(), x=s.x, y=s.y, size=s.size)

        elif isinstance(s, FontNode):
            _check_dup("font", seen)
            spec.font = s.name.strip()


        elif isinstance(s, PatternNode):
            _check_dup("pattern", seen)
            ident = s.ident.strip()
            if not ident:
                raise SemanticError("pattern: ident must be non-empty")
            if (ident == "stripes" or ident == "hoops"):
                c = s.args[0]
                t = s.args[1]
                if ((c is not None and c < 1) or (c is not None and c > 50)):
                    raise SemanticError("stripes/hoops: count must be between 1 and 50")
                if ((t is not None and t < 2) or (t is not None and t > 120)):
                    raise SemanticError("stripes/hoops: thickness must be between 2 and 120")
            if (ident == "sash"):
                a = s.args[0]
                w = s.args[1]
                if ((a is not None and a < 0) or (a is not None and a > 85)):
                    raise SemanticError("sash: angle must be between 0 and 85")
                if ((w is not None and w < 10) or (w is not None and w > 200)):
                    raise SemanticError("sash: width must be between 10 and 200")
            if (ident == "checker"):
                w = s.args[0]
                h = s.args[1]
                if ((w is not None and w < 5) or (h is not None and h < 5)):
                    raise SemanticError("checker: width/height must greater than 5")
                if ((w is not None and w > 200) or (h is not None and h > 200)):
                    raise SemanticError("checker: width/height must less than 200")
            if (ident == "gradient"):
                i = s.args[1]
                if (i is not None and i < 10):
                    raise SemanticError("gradient: intensity must greater than 10")
                if (i is not None and i > 200):
                    raise SemanticError("gradient: intensity must less than 200")
            if (ident == "brush"):
                t = s.args[0]
                r = s.args[1]
                if ((t is not None and t < 1) or (t is not None and t > 200)):
                    raise SemanticError("brush: thickness must be between 1 and 200")
                if ((r is not None and r < 5) or (r is not None and r > 200)):
                    raise SemanticError("brush: roughness must be between 5 and 200")
            if (ident == "waves"):
                a = s.args[0]
                l = s.args[1]
                if ((a is not None and a < 2) or (a is not None and a > 200)):
                    raise SemanticError("waves: amplitude must be between 2 and 200")
                if ((l is not None and l < 1) or (l is not None and l > 100)):
                    raise SemanticError("waves: wavelength must be between 1 and 100")

            spec.pattern = (ident, s.args[:])

        else:
            raise SemanticError(f"Unknown statement: {type(s).__name__}")

    # required
    missing = [k for k in ("primary", "secondary", "tertiary") if getattr(spec, k) is None]
    if missing:
        raise SemanticError(f"Missing required field(s): {', '.join(missing)}")

    # defaults
    spec.team   = spec.team or TextPlacement(text="Unnamed FC", x=365, y=190, size=18)
    spec.player = spec.player or TextPlacement(text="PLAYER", x=365, y=85, size=17)
    spec.font   = spec.font or "Arial"
    spec.number = spec.number or TextPlacement(text=23, x=365, y=155, size=75)
    spec.sponsor = spec.sponsor or TextPlacement(text="SJSU", x=115, y=125, size=35)
    return spec

def _check_dup(key: str, seen: Dict[str, int]):
    if key in seen:
        raise SemanticError(f"Duplicate declaration for '{key}'")
    seen[key] = 1
