from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping, Optional, List


@dataclass
class NumType:
    pass

@dataclass
class BoolType:
    pass

@dataclass
class StringType:
    pass

@dataclass
class ListType:
    pass

@dataclass
class Funct_obj:
    pass 

SimType = NumType | BoolType | StringType|ListType| Funct_obj

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
class StringLiteral:
    value: str
    type: Optional[StringType] = StringType()
    


@dataclass
class ListObject:
    elements: list()
    element_type: int | float | str | list
    type: Optional[ListType] = ListType()


@dataclass
class ListCons:
    to_add: 'AST'
    base_list: 'AST'
    #If I have an empty 


@dataclass
class ListOp:
    op: str
    base_list: 'AST'
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
class StringSlice:
    var: Variable
    start: NumType()
    end: NumType()

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
class Range:
    start: 'AST'
    end: 'AST'
    type: Optional[SimType] = None
@dataclass
class ASTSequence:
    seq: list['AST'] | list
    type: Optional[SimType] = None
    length = lambda self: len(self.seq)

@dataclass
class ForLoop:
    var: 'AST'
    val_list: list['AST']
    stat: 'AST' 

@dataclass
class Print:
    value: 'AST'
        
@dataclass
class Declare:
    var:'AST'
    value: 'AST'

@dataclass
class Assign:
    var: 'AST'
    expression: 'AST'

@dataclass
class While:
    cond: 'AST'
    seq: 'AST'
    

@dataclass
class DoWhile:
    seq: 'AST'
    cond: 'AST'

@dataclass
class funct_def:
    name: str
    var_list : list['AST']
    body : 'AST'

@dataclass
class funct_ret:
    ret_val: 'AST'

@dataclass
class funct_call:
    name: 'AST'
    arg_val: list['AST']

AST = ASTSequence | NumLiteral | BinOp | UnOp | Variable | Let | BoolLiteral | If | ForLoop | Declare | Assign | While | DoWhile | funct_def | funct_call | funct_ret | Print | StringLiteral | ListObject | StringSlice | ListCons | ListOp


Value = Fraction | bool | str | list  

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
class StringToken:
    s: str


@dataclass
class ListToken:
    l: list

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
@dataclass
class Symbols:
    symbol: str



