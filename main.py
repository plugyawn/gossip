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

class RuntimeEnvironment():
    def __init__(self):
        self.environment = {}

    def eval(self, program: AST, environment = None) -> Value:
        if environment:
            self.environment = environment
        if not self.environment:
            self.environment = {}
        match program:
            case NumLiteral(value):
                return value
            case Variable(name):
                if name in self.environment:
                    return self.environment[name]
                raise InvalidProgram()
            case Let(Variable(name), e1, e2):
                v1 = self.eval(e1)
                return self.eval(e2, self.environment | { name: v1 })
            case BinOp("+", left, right):
                environment = self.environment
                left = self.eval(left, environment)
                right = self.eval(right, environment)
                assert type(left) == type(right) == Fraction
                return left + right
            case BinOp("-", left, right):
                left = self.eval(left, environment)
                right = self.eval(right, environment)
                assert type(left) == type(right) == Fraction
                return left - right
            case BinOp("*", left, right):
                left = self.eval(left, environment)
                right = self.eval(right, environment)
                assert type(left) == type(right) == Fraction
                return left * right
            case BinOp("/", left, right):
                left = self.eval(left, environment)
                right = self.eval(right, environment)
                assert type(left) == type(right) == Fraction
                return left / right
            case BinOp("==", left, right):
                return self.eval(left) == self.eval(right)
            case BinOp("!=", left, right):
                return self.eval(left) != self.eval(right)
            case BinOp("<", left, right):
                assert type(self.eval(left)) == type(self.eval(right))
                return self.eval(left) < self.eval(right)
            case BinOp(">", left, right):
                assert type(self.eval(left)) == type(self.eval(right))
                return self.eval(left) > self.eval(right)
            case BinOp("<=", left, right):
                assert type(self.eval(left)) == type(self.eval(right))
                return self.eval(left) <= self.eval(right)
            case BinOp(">=", left, right):
                assert type(self.eval(left)) == type(self.eval(right))
                return self.eval(left) >= self.eval(right)
            case BinOp("&&", left, right):
                assert type(self.eval(left) == type(self.eval(right)) == bool)
                return self.eval(left) and self.eval(right)
            case BinOp("||", left, right):
                assert type(self.eval(left) == type(self.eval(right)) == bool)
                return self.eval(left) or self.eval(right)
            
            case UnOp("-", right):
                return 0 - self.eval(right)

            case If(cond, e1, e2):
                assert type(self.eval(cond)) == bool
                if self.eval(cond) == True:
                    return self.eval(e1)
                else:
                    return self.eval(e2)
        raise InvalidProgram(f"Runtime environment does not support program: {program}.")

def test_eval():
    runtime = RuntimeEnvironment()
    e1 = NumLiteral(2)
    e2 = NumLiteral(7)
    e3 = NumLiteral(9)
    e4 = NumLiteral(5)
    e5 = BinOp("+", e2, e3)
    e6 = BinOp("/", e5, e4)
    e7 = BinOp("*", e1, e6)
    assert runtime.eval(e7) == Fraction(32, 5)

    e8 = UnOp("-", e7)
    assert runtime.eval(e8) == Fraction(-32, 5)

def test_let_eval():
    runtime = RuntimeEnvironment()
    a  = Variable("a")
    e1 = NumLiteral(5)
    e2 = BinOp("+", a, a)
    e  = Let(a, e1, BinOp("+", a, Let(a, e2, e2)))
    assert runtime.eval(e) == 25
    e  = Let(a, e1, BinOp("+", Let(a, e2, e2), a))
    assert runtime.eval(e) == 25
    e3 = NumLiteral(6)
    e  = BinOp("+", Let(a, e1, e2), Let(a, e3, e2))
    assert runtime.eval(e) == 22

    a = NumLiteral(5)
    b = NumLiteral(6)
    c = NumLiteral(1)

    e = BinOp("==", a, BinOp("-", b, c))
    assert runtime.eval(e) == True

    e = BinOp("!=", a, BinOp("-", b, c))
    assert runtime.eval(e) == False

    e = If(BinOp("==", a, BinOp("-", b, c)), NumLiteral(1), NumLiteral(2))
    assert runtime.eval(e) == Fraction(1)


# main
if __name__ == "__main__":
    test_let_eval()