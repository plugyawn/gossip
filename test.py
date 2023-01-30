from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from core import RuntimeEnvironment
from utils.datatypes import *


def test_eval():
    """
    Tests the eval method of the runtime environment.
    """
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
    """
    Tests the eval method of the runtime environment with the Let paradigm.
    """
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

def test_bool_eval():
    """
    Tests the eval method of the runtime environment with boolean expressions.
    """
    runtime = RuntimeEnvironment()
    a = NumLiteral(5)
    b = NumLiteral(6)
    c = NumLiteral(1)

    e = BinOp("==", a, BinOp("-", b, c))
    assert runtime.eval(e) == True

    e = BinOp("!=", a, BinOp("-", b, c))
    assert runtime.eval(e) == False

    e = If(BinOp("==", a, BinOp("-", b, c)), NumLiteral(1), NumLiteral(2))
    assert runtime.eval(e) == Fraction(1)

def test_for_loop():
    runtime = RuntimeEnvironment()
    a = NumLiteral(0)
    b = NumLiteral(1)
    c = NumLiteral(2)
    d = NumLiteral(3)
    e = NumLiteral(4)
    f = NumLiteral(5) 
    g = [a,b,c,d,e,f]
    h  = Variable("h")
    e2 = BinOp("+", h, h)
    lo = ForLoop(h,g,e2)
    assert runtime.eval(lo) == 10
    
# main
if __name__ == "__main__":
    test_eval()
    test_let_eval()
    test_bool_eval()
    test_for_loop()
