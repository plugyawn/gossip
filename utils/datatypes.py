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

"""
The following are used in the evaluation step.
"""
@dataclass
class NumLiteral:
    value: Fraction
    type = NumType()
    def __init__(self, *args):
        self.value = Fraction(*args)

@dataclass
class BoolLiteral:
    value: bool
    type = BoolType()

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
    type = NumType()

@dataclass
class Variable:
    name: str
    type: Optional[SimType] = None

@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST' = None

@dataclass
class Assign:
    var: Variable
    e1: 'AST'

@dataclass
class If:
    cond: 'AST'
    e1: 'AST'
    e2: 'AST'
    type: Optional[SimType] = None

@dataclass
class ASTSequence:
    seq: list['AST'] | list
    type: Optional[SimType] = None

AST = ASTSequence | NumLiteral | BinOp | UnOp | Variable | Let | BoolLiteral | If | list['AST']

Value = Fraction

"""
The following are used in the lexer.
"""
@dataclass
class Num:
    n: int | float
    floating: bool = False

@dataclass
class Bool:
    b: bool

@dataclass
class Keyword:
    word: str

@dataclass
class Identifier:
    word: str

@dataclass
class Operator:
    op: str

@dataclass
class Buffer:
    buf: str
