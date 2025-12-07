from dataclasses import dataclass, field
from typing import List, Optional, Union

# AST Nodes for Jersey DSL
@dataclass
class TeamNode:
    name: str
    x: int
    y: int
    size: int

@dataclass
class ColorNode:
    kind: str  # 'primary' | 'secondary' | 'tertiary' | 'pattern_color'
    value: str # "#RRGGBB" or "#RGB"

@dataclass
class NumberNode:
    value: int
    x: int
    y: int
    size: int

@dataclass
class PlayerNode:
    name: str
    x: int
    y: int
    size: int

@dataclass
class SponsorNode:
    name: str
    x: int
    y: int
    size: int

@dataclass
class FontNode:
    name: str

Arg = Union[int, str]  # int for INT, str for COLOR/STRING/IDENT

@dataclass
class PatternNode:
    ident: str
    args: List[Arg] = field(default_factory=list)

# Define a union type for all possible statement nodes
Stmt = Union[
    TeamNode, ColorNode, NumberNode, PlayerNode, SponsorNode, FontNode, PatternNode
]

@dataclass
class JerseyNode:
    stmts: List[Stmt]
