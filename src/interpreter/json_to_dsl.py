# src/interpreter/json_to_dsl.py

from typing import Dict, Any, List


def jersey_json_to_dsl(data: Dict[str, Any]) -> str:
    """
    Convert AI suggestion JSON into a jersey DSL string.
    """

    # 1. Read pattern
    pattern = data.get("pattern", {}) or {}
    pattern_type = pattern.get("type", "plain")
    pattern_args: List[Any] = pattern.get("args", []) or []
    args_str = ", ".join(str(a) for a in pattern_args)

    lines: List[str] = []
    lines.append("jersey {")

    # 2. Mandatory
    lines.append(f'  team: "{data["team"]}";')
    lines.append(f'  primary: {data["primary"]};')
    lines.append(f'  secondary: {data["secondary"]};')
    lines.append(f'  tertiary: {data["tertiary"]};')
    lines.append(f'  player_size: {data["player_size"]};')
    lines.append(f'  number_size: {data["number_size"]};')
    lines.append(f'  team_size: {data["team_size"]};')
    lines.append(f'  sponsor_size: {data["sponsor_size"]};')

    # 3. Pattern (skip if plain)
    if pattern_type != "plain":
        if args_str:
            lines.append(f"  pattern: {pattern_type}({args_str});")
        else:
            lines.append(f"  pattern: {pattern_type}();")

    # 4. Optional fields
    pattern_color = data.get("patternColor")
    if pattern_color:
        lines.append(f"  pattern_color: {pattern_color};")

    number = data.get("number")
    if number is not None:
        lines.append(f"  number: {int(number)};")

    player = data.get("player")
    if player:
        lines.append(f'  player: "{player}";')

    sponsor = data.get("sponsor")
    if sponsor:
        lines.append(f'  sponsor: "{sponsor}";')

    font = data.get("font")
    if font:
        lines.append(f'  font: "{font}";')

    lines.append("}")
    return "\n".join(lines)
