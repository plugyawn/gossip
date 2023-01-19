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

AST = NumLiteral | BinOp | UnOp | Variable | Let | BoolLiteral | If

Value = Fraction

class InvalidProgram(Exception):
    pass

def eval(program: AST, environment: Mapping[str, Value] = None) -> Value:
    if environment is None:
        environment = {}
    match program:
        case NumLiteral(value):
            return value
        case Variable(name):
            if name in environment:
                return environment[name]
            raise InvalidProgram()
        case Let(Variable(name), e1, e2):
            v1 = eval(e1, environment)
            return eval(e2, environment | { name: v1 })
        case BinOp("+", left, right):
            assert type(eval(left, environment)) == type(eval(right, environment)) == Fraction
            return eval(left, environment) + eval(right, environment)
        case BinOp("-", left, right):
            assert type(eval(left, environment)) == type(eval(right, environment)) == Fraction
            return eval(left, environment) - eval(right, environment)
        case BinOp("*", left, right):
            assert type(eval(left, environment)) == type(eval(right, environment)) == Fraction
            return eval(left, environment) * eval(right, environment)
        case BinOp("/", left, right):
            assert type(eval(left, environment)) == type(eval(right, environment)) == Fraction
            return eval(left, environment) / eval(right, environment)
        case BinOp("==", left, right):
            return eval(left, environment) == eval(right, environment)
        case BinOp("!=", left, right):
            return eval(left, environment) != eval(right, environment)
        case BinOp("<", left, right):
            assert type(eval(left, environment)) == type(eval(right, environment))
            return eval(left, environment) < eval(right, environment)
        case BinOp(">", left, right):
            assert type(eval(left, environment)) == type(eval(right, environment))
            return eval(left, environment) > eval(right, environment)
        case BinOp("<=", left, right):
            assert type(eval(left, environment)) == type(eval(right, environment))
            return eval(left, environment) <= eval(right, environment)
        case BinOp(">=", left, right):
            assert type(eval(left, environment)) == type(eval(right, environment))
            return eval(left, environment) >= eval(right, environment)

        case BinOp("&&", left, right):
            assert type(eval(left, environment) == type(eval(right, environment)) == bool)
            return eval(left, environment) and eval(right, environment)
        case BinOp("||", left, right):
            assert type(eval(left, environment) == type(eval(right, environment)) == bool)
            return eval(left, environment) or eval(right, environment)
        
        case UnOp("-", right):
            return 0 - eval(right, environment)

        case If(cond, e1, e2):
            assert type(eval(cond, environment)) == bool
            if eval(cond, environment) == True:
                return eval(e1, environment)
            else:
                return eval(e2, environment)

    raise InvalidProgram()

def test_eval():
    e1 = NumLiteral(2)
    e2 = NumLiteral(7)
    e3 = NumLiteral(9)
    e4 = NumLiteral(5)
    e5 = BinOp("+", e2, e3)
    e6 = BinOp("/", e5, e4)
    e7 = BinOp("*", e1, e6)
    assert eval(e7) == Fraction(32, 5)

    e8 = UnOp("-", e7)
    assert eval(e8) == Fraction(-32, 5)

def test_let_eval():
    a  = Variable("a")
    e1 = NumLiteral(5)
    e2 = BinOp("+", a, a)
    e  = Let(a, e1, e2)
    assert eval(e) == 10
    e  = Let(a, e1, Let(a, e2, e2))
    assert eval(e) == 20
    e  = Let(a, e1, BinOp("+", a, Let(a, e2, e2)))
    assert eval(e) == 25
    e  = Let(a, e1, BinOp("+", Let(a, e2, e2), a))
    assert eval(e) == 25
    e3 = NumLiteral(6)
    e  = BinOp("+", Let(a, e1, e2), Let(a, e3, e2))
    assert eval(e) == 22

    a = NumLiteral(5)
    b = NumLiteral(6)
    c = NumLiteral(1)

    e = BinOp("==", a, BinOp("-", b, c))
    assert eval(e) == True

    e = BinOp("!=", a, BinOp("-", b, c))
    assert eval(e) == False

    e = If(BinOp("==", a, BinOp("-", b, c)), NumLiteral(1), NumLiteral(2))
    assert eval(e) == Fraction(1)