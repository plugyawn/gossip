from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from core import RuntimeEnvironment
from utils.datatypes import *


# def test_eval():
#     """
#     Tests the eval method of the runtime environment.
#     """
#     runtime = RuntimeEnvironment()
#     e1 = NumLiteral(2)
#     e2 = NumLiteral(7)
#     e3 = NumLiteral(9)
#     e4 = NumLiteral(5)
#     e5 = BinOp("+", e2, e3)
#     e6 = BinOp("/", e5, e4)
#     e7 = BinOp("*", e1, e6)
#     assert runtime.eval(e7) == Fraction(32, 5)

#     e8 = UnOp("-", e7)
#     assert runtime.eval(e8) == Fraction(-32, 5)

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

def test_let_eval():
    """
    Tests the eval method of the runtime environment with the Let paradigm.
    """
    runtime = RuntimeEnvironment()
    a  = Variable("a")
    e1 = NumLiteral(5)
    e2 = NumLiteral(10)
    e3 = NumLiteral(4)

    m = Let(a,e1,BinOp("==",Let(a,e2,BinOp("+",a,a)),BinOp("*",a,e3)))
    print(runtime.eval(m))


    # e2 = BinOp("+", a, a)
    # e  = Let(a, e1, BinOp("+", a, Let(a, e2, e2)))
    # assert runtime.eval(e) == 25
    # e  = Let(a, e1, BinOp("+", Let(a, e2, e2), a))
    # assert runtime.eval(e) == 25
    # e3 = NumLiteral(6)
    # e  = BinOp("+", Let(a, e1, e2), Let(a, e3, e2))
    # assert runtime.eval(e) == 22

# def test_bool_eval():
#     """
#     Tests the eval method of the runtime environment with boolean expressions.
#     """
#     runtime = RuntimeEnvironment()
#     a = NumLiteral(5)
#     b = NumLiteral(6)
#     c = NumLiteral(1)

#     e = BinOp("==", a, BinOp("-", b, c))
#     assert runtime.eval(e) == True

#     e = BinOp("!=", a, BinOp("-", b, c))
#     assert runtime.eval(e) == False

#     e = If(BinOp("==", a, BinOp("-", b, c)), NumLiteral(1), NumLiteral(2))

#     assert runtime.eval(e) == Fraction(1)

# def test_sequence_eval():
#     runtime = RuntimeEnvironment()
#     a = NumLiteral(5)
#     b = NumLiteral(6)
#     c = NumLiteral(1)

#     v = Variable("v")
#     w = Let(v, a, a)
#     x = Let(v, BinOp("+", v, v), a)

#     p = Let(v, b, b)
#     q = Let(v, BinOp("-", v, v), b) 


#     f = ASTSequence([w, x, v])
#     g = ASTSequence([p, q, v])


#     g = If(BinOp("==", a, BinOp("-", b, c)), f, g)


# def test_while():
#     runtime = RuntimeEnvironment()
#     upper = NumLiteral(3)
#     lower = NumLiteral(0)

#     increment = NumLiteral(1)

#     x = Variable("x")
#     y = Variable("y")    

#     cond = Let(y,lower,BinOp("<=",y,upper))

#     stmt1 = Let(x,BinOp("+",x,x),lower)
#     stmt2 = Let(x,BinOp("*",x,x),lower)
#     stmt3 = Let(y,BinOp("+",y,increment),lower)

#     sequence = [stmt1,stmt2,stmt3]

#     e = While(cond,sequence)
#     # print(runtime.eval(e))

#     ##Test
#     # x=0
#     # y=0
#     # while(y<=3):
#     #     x=x+x
#     #     x=x*x
#     #     y=y+1


#     # a = runtime.eval(e)
#     # print(a)



# # test_sequence_eval()
# # main
# if __name__ == "__main__":
#     test_eval()
#     test_let_eval()
#     test_bool_eval()
#     test_sequence_eval()
#     test_while()

test_let_eval()