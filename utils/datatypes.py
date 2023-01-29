from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping, Optional

@dataclass
class NumType:
    pass

@dataclass
class BoolType:
    pass

SimType = NumType | BoolType

@dataclass
class NumLiteral:
    value: Fraction
    type: SimType = NumType()

@dataclass
class BoolLiteral:
    value: bool
    type: SimType = BoolType()

@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'
    type: Optional[SimType] = None

@dataclass
class UnOp:
    operator: str
    right: 'AST'

@dataclass
class Variable:
    name: str

@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

@dataclass
class If:
    cond: 'AST'
    e1: 'AST'
    e2: 'AST'
    type: Optional[SimType] = None

@dataclass
class ASTSequence:
    seq: list['AST'] | list

AST = ASTSequence | NumLiteral | BinOp | UnOp | Variable | Let | BoolLiteral | If | list['AST']

Value = Fraction