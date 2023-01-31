from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from core import RuntimeEnvironment
from utils.datatypes import AST, NumLiteral, BinOp, Variable, Let, Value, If, BoolLiteral, UnOp, ASTSequence, NumType, BoolType, Assign, While, DoWhile
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
    """
    Tests the eval method of the runtime environment with the Let paradigm.
    """
    checker = StaticTypeChecker()
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

def test_greater_than():
    r = RuntimeEnvironment()
    a = NumLiteral(5)
    b = NumLiteral(6)
    c = BinOp(">=",b,a)

    assert(r.eval(c)==True)

def test_sequence_and_assign():
    r = RuntimeEnvironment()
    a = NumLiteral(10)
    b = NumLiteral(6)
    f = NumLiteral(2)

    v = Variable("v")
    w = Variable("w")
    c = Assign(v,BinOp("+",a,b))
    d = Assign(w,BinOp("*",v,v))
    e = Assign(w,BinOp("/",w,f))

    s = ASTSequence([c,d,e])

    assert(r.eval(s)==128)

def test_while():
    r = RuntimeEnvironment()

    j = Variable("j")
    i = Variable("i")
    x = Variable("x")
    

    double_it = NumLiteral(2)
    start = NumLiteral(0)
    increment = NumLiteral(1)
    end = NumLiteral(8)

    
    stmt_init_j = Assign(j,start)
    stmt_init_x = Assign(x,start)
    cond = BinOp("<=",j,end)
    
    stmt1 = Assign(i,BinOp("*",j,double_it))
    stmt2 = Assign(x,BinOp("+",x,i))
    stmt3 = Assign(j,BinOp("+",j,increment))

    loop_statements = ASTSequence([stmt1,stmt2,stmt3])
    loop = While(cond,loop_statements)

    s = ASTSequence([stmt_init_j,stmt_init_x,loop])

    assert(r.eval(s)==9)

def test_while_initial_cond_false():
    r = RuntimeEnvironment()

    j = Variable("j")
    i = Variable("i")
    x = Variable("x")
    

    double_it = NumLiteral(2)
    start = NumLiteral(0)
    increment = NumLiteral(1)
    end = NumLiteral(8)

    
    stmt_init_j = Assign(j,start)
    stmt_init_x = Assign(x,start)
    cond = BinOp(">=",j,end)
    
    stmt1 = Assign(i,BinOp("*",j,double_it))
    stmt2 = Assign(x,BinOp("+",x,i))
    stmt3 = Assign(j,BinOp("+",j,increment))

    loop_statements = ASTSequence([stmt1,stmt2,stmt3])
    loop = While(cond,loop_statements)

    s = ASTSequence([stmt_init_j,stmt_init_x,loop])

    assert(r.eval(s)==None)  


#for an initially true condition, while and do-while work identically
def test_do_while_initial_cond_true():
    r = RuntimeEnvironment()

    j = Variable("j")
    i = Variable("i")
    x = Variable("x")
    

    double_it = NumLiteral(2)
    start = NumLiteral(0)
    increment = NumLiteral(1)
    end = NumLiteral(8)

    
    stmt_init_j = Assign(j,start)
    stmt_init_x = Assign(x,start)
    cond = BinOp("<=",j,end)
    
    stmt1 = Assign(i,BinOp("*",j,double_it))
    stmt2 = Assign(x,BinOp("+",x,i))
    stmt3 = Assign(j,BinOp("+",j,increment))

    loop_statements = ASTSequence([stmt1,stmt2,stmt3])
    loop = DoWhile(loop_statements,cond)

    s = ASTSequence([stmt_init_j,stmt_init_x,loop])

    assert(r.eval(s)==9) 


#for an initially false conditon, while doesn't work and do-while executes once

def test_do_while_initial_cond_false():
    r = RuntimeEnvironment()

    j = Variable("j")
    i = Variable("i")
    x = Variable("x")
    

    double_it = NumLiteral(2)
    start = NumLiteral(0)
    increment = NumLiteral(1)
    end = NumLiteral(8)

    
    stmt_init_j = Assign(j,start)
    stmt_init_x = Assign(x,start)
    ##change is here
    cond = BinOp(">=",j,end)
    
    stmt1 = Assign(i,BinOp("*",j,double_it))
    stmt2 = Assign(x,BinOp("+",x,i))
    stmt3 = Assign(j,BinOp("+",j,increment))

    loop_statements = ASTSequence([stmt1,stmt2,stmt3])
    loop = DoWhile(loop_statements,cond)

    s = ASTSequence([stmt_init_j,stmt_init_x,loop])

    assert(r.eval(s)==1)

    
   

    ##Test
    # x=0
    # j=0
    # while(j<=5):
    #     i=2*j
    #     x=x+i
    #     j=j+1


    

# main
if __name__ == "__main__":
    test_eval()
    test_let_eval()
    test_bool_eval()
    test_sequence_eval()
    test_greater_than()
    test_sequence_and_assign()
    test_while()
    test_do_while_initial_cond_true()


