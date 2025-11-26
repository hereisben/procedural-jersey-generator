from dataclasses import dataclass, field
from os import name
from turtle import st
from typing import List, Optional, Union, Any

@dataclass
class TeamNode:
    name: str

@dataclass
class ColorNode:
    kind: str  # 'primary' | 'secondary' | 'tertiary' | 'pattern_color'
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

@dataclass
class PlayerSizeNode:
    value: int

@dataclass
class TeamSizeNode:
    value: int

@dataclass
class NumberSizeNode:
    value: int

@dataclass
class SponsorSizeNode:
    value: int


Arg = Union[int, str]  # int for INT, str for COLOR/STRING/IDENT

@dataclass
class PatternNode:
    ident: str
    args: List[Arg] = field(default_factory=list)

Stmt = Union[
    TeamNode, ColorNode, NumberNode, PlayerNode, SponsorNode, FontNode, PlayerSizeNode, NumberSizeNode, TeamSizeNode, SponsorNode, PatternNode
]

@dataclass
class JerseyNode:
    stmts: List[Stmt]
