from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping

@dataclass
class NumLiteral:
    value: Fraction
    def __init__(self, *args):
        self.value = Fraction(*args)

@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'

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

@dataclass
class BoolLiteral:
    value: bool

@dataclass
class ASTSequence:
    seq: list['AST'] | list


@dataclass
class While:
    cond: 'AST'
    seq: list['AST']
    env: dict

AST = ASTSequence | NumLiteral | BinOp | UnOp | Variable | Let | BoolLiteral | If | While

Value = Fraction

class InvalidProgram(Exception):
    pass
