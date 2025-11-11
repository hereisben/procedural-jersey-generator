from dataclasses import dataclass, field
from typing import List, Optional, Union, Any

@dataclass
class TeamNode:
    name: str

@dataclass
class ColorNode:
    kind: str  # 'primary' | 'secondary' | 'patterncolor'
    value: str # "#RRGGBB" or "#RGB"

@dataclass
class NumberNode:
    value: int

@dataclass
class PlayerNode:
    name: str

@dataclass
class SponsorNode:
    name: str

@dataclass
class FontNode:
    name: str

Arg = Union[int, str]  # int for INT, str for COLOR/STRING/IDENT

@dataclass
class PatternNode:
    ident: str
    args: List[Arg] = field(default_factory=list)

Stmt = Union[
    TeamNode, ColorNode, NumberNode, PlayerNode, SponsorNode, FontNode, PatternNode
]

@dataclass
class JerseyNode:
    stmts: List[Stmt]
