# src/interpreter/svg.py
from dataclasses import dataclass
from ..semantic.checks import JerseySpec

SVG_HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
W, H = 484, 342

FRONT_BODY_PATH = (
    "M 131.85528,19.171174 C 139.53629,16.610837 141.64632,-0.014767775 "
    "147.46173,1.2097492 C 174.36045,6.8736572 208.82829,25.734133 "
    "209.64854,40.433995 C 210.84774,61.925053 221.56575,85.146766 "
    "229.73554,106.39756 C 213.34939,115.1027 198.73219,122.92337 "
    "182.34604,131.62851 C 178.50553,127.78801 162.38641,87.17138 "
    "163.82452,81.107 C 165.38956,74.507362 167.71215,160.04893 "
    "182.34604,185.39557 C 185.93828,191.61751 162.50286,209.2067 "
    "115.11776,209.2067 C 67.290507,209.2067 44.297267,191.61751 "
    "47.889507,185.39557 C 62.523394,160.04893 57.592845,72.373857 "
    "58.411018,79.107 C 60.849126,99.17138 51.730009,127.78801 "
    "47.889505,131.62851 C 31.503353,122.92337 16.886153,115.1027 "
    "0.500001,106.39756 C 8.669794,85.146766 19.387801,61.925053 "
    "20.586999,40.433995 C 21.40725,25.734133 60.455348,5.7285924 "
    "87.354067,0.064684449 C 93.169478,-1.1598326 93.799064,17.48998 "
    "101.48007,20.050317 C 116.30881,21.012341 111.4688,23.404506 "
    "131.85528,19.171174 z"
)

FRONT_DECOR_PATH = (
    "M 68.230168,202.7133 L 66.74401,202.04554 L 65.889571,204.66438 L 62.971263,216.84432 L 64.304094,227.24503 L 67.830638,235.92452 L 66.347275,225.34068 L 66.46241,217.06712 L 68.333908,208.36933 L 70.319926,202.92026 L 70.186062,203.97615 L 68.230168,202.7133 z "
    "M 162.64098,202.50595 L 164.12713,201.83819 L 164.98157,204.45703 L 167.89988,216.63697 L 166.56705,227.03768 L 163.04051,235.71717 L 164.52387,225.13333 L 164.40873,216.85977 L 162.53724,208.16198 L 160.55122,202.71291 L 160.68508,203.7688 L 162.64098,202.50595 z "
)

FRONT_SHORTS_PATH = (
    "M 115.11777,291.33484 L 125.23094,341.6678 L 184.52146,326.73853 "
    "L 170.01874,177.44586 L 60.216797,177.44586 L 45.71408,326.73853 "
    "L 105.0046,341.6678 L 115.11777,291.33484 z"
)

FRONT_TRIM_TOP_PATH = (
    "M 105.99,338.96782 L 45.54,324.04282 L 45.24,327.11782 "
    "L 105.19,342.09282 L 105.49,341.66782 z"
)

FRONT_TRIM_BOTTOM_PATH = (
    "M 124.14066,338.66782 L 184.49,323.91782 L 184.79,327.091782 "
    "L 124.90,342.16782 L 124.14066,338.66782 z"
)

BACK_BODY_PATH = (
    "M 381.73751,20.73214 C 389.41852,18.1718 391.52855,1.5462 "
    "397.34396,2.77071 C 424.24268,8.43462 458.71052,27.2951 "
    "459.53077,41.99496 C 460.72997,63.48602 471.44798,86.70773 "
    "479.61777,107.95853 C 463.23162,116.66366 448.61442,124.48434 "
    "432.22827,133.18948 C 428.38776,129.34897 412.26864,88.73235 "
    "413.70675,82.66797 C 415.27179,76.06833 417.59438,161.60989 "
    "432.22827,186.95654 C 435.82051,193.17847 412.38509,210.76767 "
    "364.99999,210.76767 C 317.17274,210.76767 294.1795,193.17847 "
    "297.77174,186.95654 C 312.40562,161.60989 307.47507,73.93482 "
    "308.29325,80.66797 C 310.73136,100.73235 301.61224,129.34897 "
    "297.77173,133.18948 C 281.38558,124.48434 266.76838,116.66366 "
    "250.38223,107.95853 C 258.55202,86.70773 269.27003,63.48602 "
    "270.46923,41.99496 C 271.28948,27.2951 310.33758,7.28956 "
    "337.2363,1.62565 C 343.05171,0.40113 343.68129,19.05095 "
    "351.3623,21.61128 C 363.83749,28.117466 372.8259,26.994907 "
    "381.73751,20.73214 z"
)

BACK_SHORTS_PATH = (
    "M 365,291.94583 L 375.11317,342.27879 L 434.40369,327.34952 "
    "L 419.90097,178.05685 L 310.09903,178.05685 L 295.59631,327.34952 "
    "L 354.88683,342.27879 L 365,291.94583 z"
)

BACK_TRIM_TOP_PATH = (
    "M 355,338.79282 L 296.25,324.04282 L 295.5,327.04282 "
    "L 354.5,341.79282 L 355,338.79282 z"
)

BACK_TRIM_BOTTOM_PATH = (
    "M 374.75,338.66782 L 433.5,323.91782 L 434.25,326.91782 "
    "L 375.25,341.66782 L 374.75,338.66782 z"
)

FRONT_COLLAR_PATH = (
    "M 86.75,0.1678158 L 91.5,13.1678158 L 98,21.417816 "
    "L 108.25,25.667816 L 115.5,25.417816 L 129,24.917816 "
    "L 138.5,20.667816 L 145.6,9.878158 L 147.0,0.8158 "
    "L 142.75,0.9178158 L 138.25,10.917816 L 133.05,18.167816 "
    "L 123.5,19.667816 L 115.5,20.667816 L 103.25,19.667816 "
    "L 99.5,17.167816 L 93,4.6678158 L 90.5,0.9678158 "
    "L 89.75,0.1678158 z"
)

BACK_COLLAR_PATH = (
    "M 337.625,5.542816 L 339.375,9.542816 L 344.875,20.792816 "
    "L 353.125,26.042816 L 375.375,27.792816 L 385.875,24.292816 "
    "L 390.375,20.042816 L 396.875,5.792816 L 396.375,2.292816 "
    "L 394.125,2.292816 L 388.125,13.292816 L 383.525,19.542816 "
    "L 374.375,22.042816 L 366.375,23.042816 L 353.125,21.042816 "
    "L 349.375,19.542816 L 342.875,6.042816 L 341.375,1.542816 "
    "L 337.625,1.342816 z"
)

LOGO_PATH = (
    "m230.58 2.4199l-68.84 0.0039-68.847 0.002-18.594 18.308-18.594 18.307 0.055 42.57 0.054 42.569 18.166 17.96 18.168 17.95h64.902 64.9l8.25 7.95 8.26 7.94v28.5 28.49l-8.18 8.19-8.18 8.18h-21.79-21.78v19.34 19.34h29.86 29.86l18.8-18.52 18.81-18.53v-46.44-46.45l-17.44-17.27-17.43-17.27h-67.67-67.67l-7.972-7.96-7.973-7.96-0.019-26.358-0.018-26.354 7.137-6.896 7.135-6.897 58.83-0.01 58.83-0.009 5.88 5.824 5.88 5.824v12.451 12.45h20.18 20.19v-37.612-37.613l-16.15-0.0001h-16.15v5.4121 5.414l-5.42-5.414-5.43-5.4121zm-116.65 76.074v15.088 15.088h12.75 12.75v4.25 4.25h16.57 16.58v-4.68-4.67h13.81 13.82v-14.664-14.662h-43.14-43.14zm25.5 87.976v71.93 71.92l-7.97 7.98-7.96 7.97h-34.646-34.647l-6.264-6.27-6.263-6.28v-13.49-13.49h-19.551-19.549l0.0001 35.49v35.49h17.213 17.211v-6.48-6.47l6.486 6.47 6.487 6.48 44.408-0.02 44.405-0.02 16.9-16.72 16.89-16.73v-78.88-78.88h-16.58-16.57zm-87.125 43.35v39.52 39.53h18.275 18.275v-5.2-5.2l4.788 4.78 4.787 4.77h17.31 17.31v-19.34-19.34h-15.76-15.76l-5.915-5.59-5.91-5.59v-14.17-14.17h-18.701-18.699z"
)

@dataclass
class RenderOptions:
    show_debug: bool = False

def render_svg(spec: JerseySpec, opts: RenderOptions | None = None) -> str:
    opts = opts or RenderOptions()
    prim = spec.primary or "#0033AA"
    sec  = spec.secondary or "#FFCC00"
    ter = spec.tertiary or spec.patterncolor or "#000000"

    # --- jersey geometry (reusable) ---
    front_body   = FRONT_BODY_PATH
    front_shorts = FRONT_SHORTS_PATH
    back_body    = BACK_BODY_PATH
    back_shorts  = BACK_SHORTS_PATH
    front_decors = FRONT_DECOR_PATH
    logo = LOGO_PATH

    # --- clipped pattern layer (mask to jersey shape) ---
    defs = f'''
      <defs>
        <clipPath id="frontJerseyClip">
        <path d="{front_body}"/>
        </clipPath>
        <clipPath id="backJerseyClip">
        <path d="{back_body}"/>
        </clipPath>

        <clipPath id="frontShortsClip">
        <path d="{front_shorts}"/>
        </clipPath>
        <clipPath id="backShortsClip">
        <path d="{back_shorts}"/>
        </clipPath>
    </defs>
    '''

    front_shorts_fill = f'<path d="{front_shorts}" fill="{sec}"/>\n'
    back_shorts_fill  = f'<path d="{back_shorts}"  fill="{sec}"/>\n'

    front_jersey_fill = f'<path d="{front_body}"  fill="{prim}"/>\n'
    back_jersey_fill  = f'<path d="{back_body}"   fill="{prim}"/>\n'

    front_short_decor = f'<path d="{front_decors}" fill="{prim}"/>\n'
    logo_decor = f'<path d="{logo}" transform="scale(0.07) translate(1900, 700)" fill="#ffffff"/>\n'

    patcol = spec.patterncolor or "#FFFFFF"

    front_jersey_pattern = (
        f'<g clip-path="url(#frontJerseyClip)">\n'
        f'{_pattern_layer(spec, prim, patcol)}\n'
        f'</g>\n'
    )
    back_jersey_pattern = (
        f'<g clip-path="url(#backJerseyClip)">\n'
        f'{_pattern_layer(spec, prim, patcol)}\n'
        f'</g>\n'
    )

    front_shorts_pattern = ""
    back_shorts_pattern = ""

    trims = (
        f'<path d="{FRONT_TRIM_TOP_PATH}"    fill="{ter}"/>\n'
        f'<path d="{FRONT_TRIM_BOTTOM_PATH}" fill="{ter}"/>\n'
        f'<path d="{BACK_TRIM_TOP_PATH}"     fill="{ter}"/>\n'
        f'<path d="{BACK_TRIM_BOTTOM_PATH}"  fill="{ter}"/>\n'
    )

    # Outlines
    shorts_outlines = (
        f'<path d="{front_shorts}" fill="none" stroke="#111" stroke-width="2.0"/>\n'
        f'<path d="{back_shorts}"  fill="none" stroke="#111" stroke-width="2.0"/>\n'
    )

    jersey_outlines = (
        f'<path d="{front_body}"   fill="none" stroke="#111" stroke-width="2.0"/>\n'
        f'<path d="{back_body}"    fill="none" stroke="#111" stroke-width="2.0"/>\n'
        f'<path d="{FRONT_TRIM_TOP_PATH}"    fill="none" stroke="#111" stroke-width="1.5"/>\n'
        f'<path d="{FRONT_TRIM_BOTTOM_PATH}" fill="none" stroke="#111" stroke-width="1.5"/>\n'
        f'<path d="{BACK_TRIM_TOP_PATH}"     fill="none" stroke="#111" stroke-width="1.5"/>\n'
        f'<path d="{BACK_TRIM_BOTTOM_PATH}"  fill="none" stroke="#111" stroke-width="1.5"/>\n'
        f'<path d="{FRONT_COLLAR_PATH}"      fill="white" stroke="{sec}" stroke-width="1.5"/>\n'
        f'<path d="{BACK_COLLAR_PATH}"       fill="white" stroke="{sec}" stroke-width="1.5"/>\n'
    )

    # --- text layers ---
    front_cx = 115
    back_cx  = 365

    front_sponsor = _svg_text(
        spec.sponsor,
        x=front_cx,
        y=125,
        size=35,
        anchor="middle",
        weight="bold",
        fill=ter,
        font=spec.font,
    ) if spec.sponsor else ""

    front_number = _svg_text(
        str(spec.number),
        x=145,
        y=70,
        size=22,
        anchor="middle",
        weight="bold",
        fill=ter,
        font=spec.font,
    )

    # Back (right): sponsor + player + number + team
    back_sponsor = _svg_text(
        spec.sponsor,
        x=back_cx,
        y=45,
        size=10,
        anchor="middle",
        weight="bold",
        fill=ter,
        font=spec.font,
    ) if spec.sponsor else ""

    back_player = _svg_text(
        spec.player,
        x=back_cx,
        y=85,
        size=26,
        anchor="middle",
        weight="bold",
        fill=ter,
        font=spec.font,
        letter_spacing="2",
    )

    back_number = _svg_text(
        str(spec.number),
        x=back_cx,
        y=155,
        size=80,
        anchor="middle",
        weight="bold",
        fill=ter,
        font=spec.font,
    )

    back_team = _svg_text(
        spec.team,
        x=back_cx,
        y=190,
        size=20,
        anchor="middle",
        weight="bold",
        fill=ter,
        font=spec.font,
    )

    debug = (
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="magenta" stroke-dasharray="4,4"/>'
        if (opts and opts.show_debug) else ""
    )

    meta = (
    '<metadata>'
    'Author: Ben Nguyen | Procedural Jersey Generator '
    '© 2025 Ben Nguyen'
    '</metadata>'
    )

    credit = _svg_text("© 2025 Ben Nguyen", x=W/2, y=590, size=14,
                   anchor="middle", weight="normal", fill="#eee", font=spec.font or "Arial")

    return (
        f"{SVG_HEADER}\n"
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
        f'  {meta}\n'
        f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>\n'
        f'  {defs}\n'
        f'  {debug}\n'
        f'  <g id="jersey">\n'
        f'    {front_shorts_fill}\n'
        f'    {front_short_decor}\n'
        f'    {back_shorts_fill}\n'
        f'    {shorts_outlines}\n'
        f'    {front_jersey_fill}\n'
        f'    {back_jersey_fill}\n'
        f'    {front_jersey_pattern}\n'
        f'    {back_jersey_pattern}\n'
        f'    {trims}\n'
        f'    {jersey_outlines}\n'
        f'    <g clip-path="url(#frontJerseyClip)">\n'
        f'      {front_sponsor}\n'
        f'      {logo_decor}\n'
        f'    </g>\n'
        f'    <g clip-path="url(#backJerseyClip)">\n'
        f'      {back_sponsor}\n'
        f'      {back_player}\n'
        f'      {back_number}\n'
        f'      {back_team}\n'
        f'    </g>\n'
        f'    {credit}\n'
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
        return _vertical_stripes(count * 2, thickness, sec)

    if ident == "hoops":
        count = int(args[0]) if len(args) >= 1 else 6
        thickness = int(args[1]) if len(args) >= 2 else 20
        return _horizontal_hoops(count, thickness, sec)

    if ident == "sash":
        angle = int(args[0]) if len(args) >= 1 else 30
        width = int(args[1]) if len(args) >= 2 else 80
        return _sash(angle, width, sec)

    return ""  # unknown pattern: ignore

# Full-canvas stripes/hoops; clipPath hides overflow beyond jersey
def _vertical_stripes(count: int, thickness: int, color: str) -> str:
    left, right, top, bottom = 0, W, 0, H
    span = right - left
    gap = span / max(count, 1)
    rects = []
    for i in range(count):
        x = left + i * gap + (gap - thickness) / 2
        rects.append(f'<rect x="{x:.1f}" y="{top}" width="{thickness}" height="{bottom-top}" fill="{color}" opacity="1"/>')
    return "\n".join(rects)

def _horizontal_hoops(count: int, thickness: int, color: str) -> str:
    left, right, top, bottom = 0, W, 0, H
    span = bottom - top
    gap = span / max(count, 1)
    rects = []
    for i in range(count):
        y = top + i * gap + (gap - thickness) / 2
        rects.append(f'<rect x="{left}" y="{y:.1f}" width="{right-left}" height="{thickness}" fill="{color}" opacity="1"/>')
    return "\n".join(rects)

def _sash(angle: int, width: int, color: str) -> str:
    cx, cy = W/2, H/2 + 40
    return (
        f'<g transform="translate({cx},{cy}) rotate({-abs(angle)}) translate({-cx}, {-cy})">'
        f'  <rect x="180" y="-100" width="{width}" height="{H}" fill="{color}" opacity="1"/>'
        f'</g>'
    )
