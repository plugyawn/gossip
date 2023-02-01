from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from core import RuntimeEnvironment
from utils.datatypes import AST, NumLiteral, BinOp, Variable, Let, Value, If, BoolLiteral, UnOp, ASTSequence, NumType, BoolType, ForLoop, Assign, While, DoWhile, Declare
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

# def test_let_eval():
#     """
#     Tests the eval method of the runtime environment with the Let paradigm.
#     """
#     checker = StaticTypeChecker()
#     runtime = RuntimeEnvironment()
#     a  = Variable("a")
#     e1 = NumLiteral(5)
#     e4 = NumLiteral(10)
#     e7 = NumLiteral(4)
#     e2 = BinOp("+", a, a)
#     e  = Let(a, e1, BinOp("+", a, Let(a, e2, e2)))
#     assert runtime.eval(e) == 25
#     e  = Let(a, e1, BinOp("+", Let(a, e2, e2), a))
#     assert runtime.eval(e) == 25
#     e3 = NumLiteral(6)
#     e  = BinOp("+", Let(a, e1, e2), Let(a, e3, e2))
#     assert runtime.eval(e) == 22
#     e10 = Let(a,e4,e2)
#     e8 = BinOp("*",a,e7)
#     e9 = BinOp("==",e10,e8)
#     e = Let(a, e1, e9)
#     assert runtime.eval(e) == True
    

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


# def test_for_loop():
#     runtime = RuntimeEnvironment()
#     a = NumLiteral(0)
#     b = NumLiteral(1)
#     c = NumLiteral(2)
#     d = NumLiteral(3)
#     e = NumLiteral(4)
#     f = NumLiteral(5) 
#     g = [a,b,c,d,e,f]
#     h  = Variable("h")
#     e2 = BinOp("+", h, h)
#     lo = ForLoop(h,g,e2)
#     assert runtime.eval(lo) == 10


# def test_stream_eval():
#     runtime = RuntimeEnvironment()

#     string = """
#     let b = 6 end
#     let a = 5 end
#     if a == b then a+2 else a+1 end
#     """
#     L = Lexer.from_stream(Stream.from_string(string))
#     runtime = RuntimeEnvironment()
#     S = Parser.from_lexer(L)
#     for s in S:
#         runtime.eval(s)


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

    inital_declare_value = NumLiteral(0)

    v = Variable("v")
    w = Variable("w")

    c_dec = Declare(v,inital_declare_value)
    c = Assign(v,BinOp("+",a,b))

    d_dec = Declare(w,inital_declare_value)
    d = Assign(w,BinOp("*",v,v))

    e = Assign(w,BinOp("/",w,f))

    s = ASTSequence([c_dec,c,d_dec,d,e])

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

    
    stmt_init_j = Declare(j,start)
    stmt_init_x = Declare(x,start)
    cond = BinOp("<=",j,end)
    
    stmt0 = Declare(i,start)
    stmt1 = Assign(i,BinOp("*",j,double_it))
    stmt2 = Assign(x,BinOp("+",x,i))
    stmt3 = Assign(j,BinOp("+",j,increment))

    loop_statements = ASTSequence([stmt0,stmt1,stmt2,stmt3])
    loop = While(cond,loop_statements)

    s = ASTSequence([stmt_init_j,stmt_init_x,loop])

    assert(r.eval(s)==9)

    ## test looks like

    # int j=0
    # int x=0

    # while(j<=8):
    #     int i = 0
    #     i = 2*j
    #     x = x+i
    #     j=j+1


def test_while_initial_cond_false():
    r = RuntimeEnvironment()

    j = Variable("j")
    i = Variable("i")
    x = Variable("x")
    

    double_it = NumLiteral(2)
    start = NumLiteral(0)
    increment = NumLiteral(1)
    end = NumLiteral(8)

    
    stmt_init_j = Declare(j,start)
    stmt_init_x = Declare(x,start)
    cond = BinOp(">=",j,end)

    stmt0 = Declare(i,start)    
    stmt1 = Assign(i,BinOp("*",j,double_it))
    stmt2 = Assign(x,BinOp("+",x,i))
    stmt3 = Assign(j,BinOp("+",j,increment))

    loop_statements = ASTSequence([stmt0,stmt1,stmt2,stmt3])
    loop = While(cond,loop_statements)

    s = ASTSequence([stmt_init_j,stmt_init_x,loop])

    assert(r.eval(s)==None)  


# #for an initially true condition, while and do-while work identically
def test_do_while_initial_cond_true():
    r = RuntimeEnvironment()

    j = Variable("j")
    i = Variable("i")
    x = Variable("x")
    

    double_it = NumLiteral(2)
    start = NumLiteral(0)
    increment = NumLiteral(1)
    end = NumLiteral(8)

    
    stmt_init_j = Declare(j,start)
    stmt_init_x = Declare(x,start)
    cond = BinOp("<=",j,end)

    stmt0 = Declare(i,start)    
    stmt1 = Assign(i,BinOp("*",j,double_it))
    stmt2 = Assign(x,BinOp("+",x,i))
    stmt3 = Assign(j,BinOp("+",j,increment))

    loop_statements = ASTSequence([stmt0,stmt1,stmt2,stmt3])
    loop = DoWhile(loop_statements,cond)

    s = ASTSequence([stmt_init_j,stmt_init_x,loop])

    assert(r.eval(s)==9) 


# #for an initially false conditon, while doesn't work and do-while executes once

def test_do_while_initial_cond_false():
    r = RuntimeEnvironment()

    j = Variable("j")
    i = Variable("i")
    x = Variable("x")
    

    double_it = NumLiteral(2)
    start = NumLiteral(0)
    increment = NumLiteral(1)
    end = NumLiteral(8)

    
    stmt_init_j = Declare(j,start)
    stmt_init_x = Declare(x,start)
    ##change is here
    cond = BinOp(">=",j,end)
    
    stmt0 = Declare(i,start)
    stmt1 = Assign(i,BinOp("*",j,double_it))
    stmt2 = Assign(x,BinOp("+",x,i))
    stmt3 = Assign(j,BinOp("+",j,increment))

    loop_statements = ASTSequence([stmt0,stmt1,stmt2,stmt3])
    loop = DoWhile(loop_statements,cond)

    s = ASTSequence([stmt_init_j,stmt_init_x,loop])

    assert(r.eval(s)==1)


def test_nested_assignment_scope_loops():

    # int c = 0
    # int i = 0

    # while(i<10):
    #     int j = 0

    #     while(j<10):
    #         int i=0

    #         while(i<5):
    #             c=c+1
    #             i=i+1
            
    #         j=j+1
        
    #     i=i+1
    
    # c should be 500

    r = RuntimeEnvironment()

    c = Variable("c")
    i = Variable("i")
    j = Variable("j")

    start = NumLiteral(0)
    end = NumLiteral(10)
    increment = NumLiteral(1)
    five =  NumLiteral(5)


    declare_c = Declare(c,start)
    declare_i = Declare(i,start)

    innermost_loop_cond = BinOp("<",i,five)
    stmt_innermost_1 = Assign(c,BinOp("+",c,increment))
    stmt_innermost_2 = Assign(i,BinOp("+",i,increment))

    innermost_loop = While(innermost_loop_cond,ASTSequence([stmt_innermost_1,stmt_innermost_2]))
    


    #################


    second_loop_cond = BinOp("<",j,end)

    second_loop_stmt1 = Declare(i,start)
    second_loop_stmt2 = innermost_loop
    second_loop_stmt3 = Assign(j,BinOp("+",j,increment))

    second_loop = While(second_loop_cond,ASTSequence([second_loop_stmt1,second_loop_stmt2,second_loop_stmt3]))


    ###############

    outermost_loop_cond = BinOp("<",i,end)

    outermost_loop_stmt1 = Declare(j,start)
    outermost_loop_stmt2 = second_loop
    outermost_loop_stmt3 = Assign(i,BinOp("+",i,increment))

    outermost_loop = While(outermost_loop_cond,ASTSequence([outermost_loop_stmt1,outermost_loop_stmt2,outermost_loop_stmt3]))


    prgrm = ASTSequence([declare_c,declare_i,outermost_loop])

    assert(r.eval(prgrm)==10)


# main
if __name__ == "__main__":
    test_eval()
    #test_let_eval()
    test_bool_eval()
    test_sequence_eval()
    #test_for_loop()
    #test_stream_eval()
    
    #added loop tests and sequence tests
    test_greater_than()
    test_sequence_and_assign()
    test_while()
    test_while_initial_cond_false()
    test_do_while_initial_cond_true()
    test_do_while_initial_cond_false()
    test_nested_assignment_scope_loops()
