from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from core import RuntimeEnvironment
from utils.datatypes import AST, NumLiteral, BinOp, Variable, Let, Value, If, BoolLiteral, UnOp, ASTSequence, NumType, BoolType
from utils.typechecker import StaticTypeChecker


def test_eval():
    """
    Tests the eval method of the runtime environment.
    """
    checker = StaticTypeChecker()
    runtime = RuntimeEnvironment()
    e1 = NumLiteral(2)
    e2 = NumLiteral(7)
    e3 = NumLiteral(9)
    e4 = NumLiteral(5)
    e5 = BinOp("+", e2, e3) # 16
    e6 = BinOp("/", e5, e4) # 3.2
    e7 = BinOp("*", e1, e6) # 6.4
    assert checker.check(e7).type == NumType()
    e5 = BinOp("+", e2, e3) # 16
    e6 = BinOp("/", e5, e4) # 3.2
    e7 = BinOp("*", e1, e6) # 6.4
    assert checker.check(e7).type == NumType()
    assert runtime.eval(e7) == Fraction(32, 5)

    e8 = UnOp("-", e7)
    assert checker.check(e8).type == NumType()
    assert checker.check(e8).type == NumType()
    assert runtime.eval(e8) == Fraction(-32, 5)

def test_let_eval():
    
    runtime = RuntimeEnvironment()
    a  = Variable("a")
    e1 = NumLiteral(5)
    e4 = NumLiteral(10)
    e7 = NumLiteral(7)
    e2 = BinOp("+", a, a)
    e  = Let(a, e1, BinOp("+", a, Let(a, e2, e2)))
    assert runtime.eval(e) == 25
    e  = Let(a, e1, BinOp("+", Let(a, e2, e2), a))
    assert runtime.eval(e) == 25
    e3 = NumLiteral(6)
    e  = BinOp("+", Let(a, e1, e2), Let(a, e3, e2))
    assert runtime.eval(e) == 22
    e10 = Let(a,e4,e2)
    e8 = BinOp("*",a,e7)
    e9 = BinOp("==",e10,e8)
    e = Let(a, e1, e9)
    assert runtime.eval(e) == True
    

def test_bool_eval():
    """
    Tests the eval method of the runtime environment with boolean expressions.
    """
    checker = StaticTypeChecker()
    runtime = RuntimeEnvironment()
    a = NumLiteral(5)
    b = NumLiteral(6)
    c = NumLiteral(1)

    e = BinOp("==", a, BinOp("-", b, c))
    assert checker.check(e).type == BoolType()
    assert runtime.eval(e) == True

    e = BinOp("!=", a, BinOp("-", b, c))
    assert checker.check(e).type == BoolType()
    assert runtime.eval(e) == False

    e = If(BinOp("==", a, BinOp("-", b, c)), NumLiteral(1), NumLiteral(2))

    assert runtime.eval(e) == Fraction(1)

def test_sequence_eval():
    runtime = RuntimeEnvironment()
    a = NumLiteral(5)
    b = NumLiteral(6)
    c = NumLiteral(1)

    v = Variable("v")
    w = Let(v, a, a)
    x = Let(v, BinOp("+", v, v), a)

    p = Let(v, b, b)
    q = Let(v, BinOp("-", v, v), b) 


    f = ASTSequence([w, x, v])
    g = ASTSequence([p, q, v])


    g = If(BinOp("==", a, BinOp("-", b, c)), f, g)



# main
if __name__ == "__main__":
    test_eval()
    test_let_eval()
    test_bool_eval()
    test_sequence_eval()
