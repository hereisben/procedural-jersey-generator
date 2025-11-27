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
    args_str = ", ".join(str(a) for a in pattern_args)

    lines: List[str] = []
    lines.append("jersey {")

    # Colors, pattern
    lines.append(f'  primary: {data["primary"]};')
    lines.append(f'  secondary: {data["secondary"]};')
    lines.append(f'  tertiary: {data["tertiary"]};')
    pattern_color = data.get("pattern_color") or data.get("secondary") or data.get("primary") or "#000000"
    if pattern_color:
        lines.append(f"  pattern_color: {pattern_color};")
    if pattern_type in ("stripes", "hoops", "sash"):
        if args_str:
            lines.append(f"  pattern: {pattern_type}({args_str});")
        else:
            lines.append(f"  pattern: {pattern_type}();")

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
