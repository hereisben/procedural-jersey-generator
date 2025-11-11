# src/interpreter/svg.py
from typing import Tuple, List, Union
from dataclasses import dataclass
from ..semantic.checks import JerseySpec

SVG_HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
W, H = 600, 700

@dataclass
class RenderOptions:
    show_debug: bool = False

def render_svg(spec: JerseySpec, opts: RenderOptions | None = None) -> str:
    opts = opts or RenderOptions()
    prim = spec.primary or "#0033AA"
    sec  = spec.secondary or "#FFCC00"

    body = f'<path d="M150,120 L240,60 L360,60 L450,120 L520,230 L520,600 L80,600 L80,230 Z" fill="{prim}" stroke="#111" stroke-width="3"/>'
    sleeves = (
        f'<path d="M80,230 L40,260 L40,330 L80,330 Z" fill="{prim}" stroke="#111" stroke-width="3"/>'
        f'<path d="M520,230 L560,260 L560,330 L520,330 Z" fill="{prim}" stroke="#111" stroke-width="3"/>'
    )

    pattern = _pattern_layer(spec, prim, sec)

    team    = _svg_text(spec.team,   x=W/2, y=220, size=26,  anchor="middle", weight="bold", fill=sec, font=spec.font)
    sponsor = _svg_text(spec.sponsor, x=W/2, y=300, size=32,  anchor="middle", weight="bold", fill=sec, font=spec.font) if spec.sponsor else ""
    number  = _svg_text(str(spec.number), x=W/2, y=400, size=120, anchor="middle", weight="bold", fill=sec, font=spec.font)
    player  = _svg_text(spec.player, x=W/2, y=160, size=22,  anchor="middle", weight="bold", fill=sec, font=spec.font, letter_spacing="2")

    debug = f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="magenta" stroke-dasharray="4,4"/>' if (opts and opts.show_debug) else ""

    return (
        f"{SVG_HEADER}\n"
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
        f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>\n'
        f'  {debug}\n'
        f'  <g id="jersey">\n'
        f'    {sleeves}\n'
        f'    {body}\n'
        f'    {pattern}\n'
        f'    {player}\n'
        f'    {team}\n'
        f'    {sponsor}\n'
        f'    {number}\n'
        f'  </g>\n'
        f'</svg>\n'
    )

def _svg_text(txt: str, x: float, y: float, size: int, anchor: str, weight: str, fill: str, font: str, letter_spacing: str | None = None) -> str:
    if txt is None:
        return ""
    ls = f' letter-spacing="{letter_spacing}"' if letter_spacing else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-weight="{weight}" font-family="{_escape(font)}" font-size="{size}" fill="{fill}"{ls}>{_escape(txt)}</text>'

def _escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
         .replace("'", "&apos;")
    )

def _pattern_layer(spec: JerseySpec, prim: str, sec: str) -> str:
    if not spec.pattern:
        return ""
    ident, args = spec.pattern
    ident = ident.lower()

    if ident == "stripes":
        count = int(args[0]) if len(args) >= 1 else 6
        thickness = int(args[1]) if len(args) >= 2 else 20
        return _vertical_stripes(count, thickness, sec)

    if ident == "hoops":
        count = int(args[0]) if len(args) >= 1 else 6
        thickness = int(args[1]) if len(args) >= 2 else 20
        return _horizontal_hoops(count, thickness, sec)

    if ident == "sash":
        angle = int(args[0]) if len(args) >= 1 else 30
        width = int(args[1]) if len(args) >= 2 else 80
        return _sash(angle, width, sec)

    return ""  # unknown pattern: ignore

def _vertical_stripes(count: int, thickness: int, color: str) -> str:
    left, right, top, bottom = 100, 500, 120, 600
    span = right - left
    gap = span / max(count, 1)
    rects = []
    for i in range(count):
        x = left + i * gap + (gap - thickness) / 2
        rects.append(f'<rect x="{x:.1f}" y="{top}" width="{thickness}" height="{bottom-top}" fill="{color}" opacity="0.75"/>')
    return "\n".join(rects)

def _horizontal_hoops(count: int, thickness: int, color: str) -> str:
    left, right, top, bottom = 100, 500, 150, 580
    span = bottom - top
    gap = span / max(count, 1)
    rects = []
    for i in range(count):
        y = top + i * gap + (gap - thickness) / 2
        rects.append(f'<rect x="{left}" y="{y:.1f}" width="{right-left}" height="{thickness}" fill="{color}" opacity="0.75"/>')
    return "\n".join(rects)

def _sash(angle: int, width: int, color: str) -> str:
    cx, cy = W/2, H/2 + 40
    return (
        f'<g transform="translate({cx},{cy}) rotate({-abs(angle)}) translate({-cx}, {-cy})">'
        f'  <rect x="120" y="140" width="{width}" height="520" fill="{color}" opacity="0.75"/>'
        f'</g>'
    )
