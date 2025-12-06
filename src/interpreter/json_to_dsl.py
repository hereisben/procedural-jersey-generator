# src/interpreter/json_to_dsl.py

from typing import Dict, Any, List


def jersey_json_to_dsl(data: Dict[str, Any]) -> str:
    """
    Convert AI suggestion JSON into a jersey DSL string.
    """

    # Read pattern
    pattern = data.get("pattern", {}) or {}
    pattern_type = pattern.get("type", "plain")
    pattern_args: List[Any] = pattern.get("args", []) or []

    lines: List[str] = []
    lines.append("jersey {")

    # Colors, pattern
    lines.append(f'  primary: {data["primary"]};')
    lines.append(f'  secondary: {data["secondary"]};')
    lines.append(f'  tertiary: {data["tertiary"]};')
    pattern_color = data.get("pattern_color") or data.get("secondary") or data.get("primary") or "#000000"
    if pattern_color:
        lines.append(f"  pattern_color: {pattern_color};")

    if pattern_type in ("stripes", "hoops"):
        if len(pattern_args) >= 2:
            count = int(pattern_args[0])
            thickness = int(pattern_args[1])
            lines.append(f"  pattern: {pattern_type}({count},{thickness});")

    elif pattern_type == "sash":
        if len(pattern_args) >= 2:
            angle = int(pattern_args[0])
            width = int(pattern_args[1])
            lines.append(f"  pattern: sash({angle},{width});")

    elif pattern_type == "checker":
        if len(pattern_args) >= 2:
            cell_w = int(pattern_args[0])
            cell_h = int(pattern_args[1])
            lines.append(f"  pattern: checker({cell_w},{cell_h});")

    elif pattern_type == "gradient":
        if len(pattern_args) >= 2:
            direction = str(pattern_args[0])
            intensity = int(pattern_args[1])
            lines.append(f'  pattern: gradient("{direction}",{intensity});')

    elif pattern_type == "brush":
        if len(pattern_args) >= 2:
            thickness = int(pattern_args[0])
            roughness = int(pattern_args[1])
            lines.append(f"  pattern: brush({thickness},{roughness});")

    elif pattern_type == "waves":
        if len(pattern_args) >= 2:
            amplitude = int(pattern_args[0])
            wavelength = int(pattern_args[1])
            lines.append(f"  pattern: waves({amplitude},{wavelength});")

    elif pattern_type == "camo":
        if len(pattern_args) >= 2:
            cell = int(pattern_args[0])
            variance = int(pattern_args[1])
            lines.append(f"  pattern: camo({cell},{variance});")

    elif pattern_type == "halftone_dots":
        if len(pattern_args) >= 2:
            dot_size = int(pattern_args[0])
            spacing = int(pattern_args[1])
            lines.append(f"  pattern: halftone_dots({dot_size},{spacing});")
    
    elif pattern_type == "topo":
        if len(pattern_args) >= 2:
            levels = int(pattern_args[0])
            base_gap = int(pattern_args[1])
            lines.append(f"  pattern: topo({levels},{base_gap});")

    elif pattern_type == "solid":
        pass
    

    #TEAM
    team = data.get("team", "UNNAMED FC")
    team_size = int(data.get("team_size", 18))
    lines.append(f'  team: "{team}", (365, 190), {team_size};')

    number = int(data.get("number", 23))
    number_size = int(data.get("number_size", 75))
    lines.append(f'  number: {number}, (365, 155), {number_size};')

    player = data.get("player", "PLAYER")
    player_size = int(data.get("player_size", 26))
    lines.append(f'  player: "{player}", (365, 85), {player_size};')

    sponsor = data.get("sponsor")
    sponsor_size = int(data.get("sponsor_size", 35))
    if sponsor:
        lines.append(f'  sponsor: "{sponsor}", (115, 125), {sponsor_size};')

    font = data.get("font")
    if font:
        lines.append(f'  font: "{font}";')

    lines.append("}")
    return "\n".join(lines)
