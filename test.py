from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from core import RuntimeEnvironment
from utils.datatypes import (
    AST,
    NumLiteral,
    BinOp,
    Variable,
    Let,
    Value,
    If,
    Print,
    BoolLiteral,
    UnOp,
    ASTSequence,
    NumType,
    BoolType,
    ForLoop,
    Assign,
    While,
    DoWhile,
    Declare,
    StringLiteral,
    ListObject,
    StringSlice,
    ListCons,
    ListOp,
    funct_def, 
    funct_call, 
    funct_ret,
    ListIndex,
)
from utils.typechecker import StaticTypeChecker
from utils.errors import *


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
    e5 = BinOp("+", e2, e3)  # 16
    e6 = BinOp("/", e5, e4)  # 3.2
    e7 = BinOp("*", e1, e6)  # 6.4
    assert checker.check(e7).type == NumType()
    e5 = BinOp("+", e2, e3)  # 16
    e6 = BinOp("/", e5, e4)  # 3.2
    e7 = BinOp("*", e1, e6)  # 6.4
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


def test_for_loop():
    runtime = RuntimeEnvironment()
    a = NumLiteral(0)
    b = NumLiteral(1)
    c = NumLiteral(2)
    d = NumLiteral(3)
    e = NumLiteral(4)
    f = NumLiteral(5)
    g = ASTSequence([a,b,c,d,e,f])
    h  = Variable("h")
    e2 = BinOp("+", h, h)
    lo = ForLoop(h,g,e2)
    assert runtime.eval(lo) == 10


def test_stream_eval():
    runtime = RuntimeEnvironment()

    string = """
    let b = 6 end
    let a = 5 end
    if a == b then a+2 else a+1 end
    """
    L = Lexer.from_stream(Stream.from_string(string))
    runtime = RuntimeEnvironment()
    S = Parser.from_lexer(L)
    for s in S:
        runtime.eval(s)


def test_greater_than():
    r = RuntimeEnvironment()
    a = NumLiteral(5)
    b = NumLiteral(6)
    c = BinOp(">=", b, a)

    assert r.eval(c) == True


def test_sequence_and_assign():
    r = RuntimeEnvironment()
    a = NumLiteral(10)
    b = NumLiteral(6)
    f = NumLiteral(2)

    inital_declare_value = NumLiteral(0)

    v = Variable("v")
    w = Variable("w")

    c_dec = Declare(v, inital_declare_value)
    c = Assign(v, BinOp("+", a, b))

    d_dec = Declare(w, inital_declare_value)
    d = Assign(w, BinOp("*", v, v))

    e = Assign(w, BinOp("/", w, f))

    s = ASTSequence([c_dec, c, d_dec, d, e])

    assert r.eval(s) == 128


def test_while():
    r = RuntimeEnvironment()

    j = Variable("j")
    i = Variable("i")
    x = Variable("x")

    double_it = NumLiteral(2)
    start = NumLiteral(0)
    increment = NumLiteral(1)
    end = NumLiteral(8)

    stmt_init_j = Declare(j, start)
    stmt_init_x = Declare(x, start)
    cond = BinOp("<=", j, end)

    stmt0 = Declare(i, start)
    stmt1 = Assign(i, BinOp("*", j, double_it))
    stmt2 = Assign(x, BinOp("+", x, i))
    stmt3 = Assign(j, BinOp("+", j, increment))

    loop_statements = ASTSequence([stmt0, stmt1, stmt2, stmt3])
    loop = While(cond, loop_statements)

    s = ASTSequence([stmt_init_j, stmt_init_x, loop])

    assert r.eval(s) == 9

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

    stmt_init_j = Declare(j, start)
    stmt_init_x = Declare(x, start)
    cond = BinOp(">=", j, end)

    stmt0 = Declare(i, start)
    stmt1 = Assign(i, BinOp("*", j, double_it))
    stmt2 = Assign(x, BinOp("+", x, i))
    stmt3 = Assign(j, BinOp("+", j, increment))

    loop_statements = ASTSequence([stmt0, stmt1, stmt2, stmt3])
    loop = While(cond, loop_statements)

    s = ASTSequence([stmt_init_j, stmt_init_x, loop])

    assert r.eval(s) == None


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

    stmt_init_j = Declare(j, start)
    stmt_init_x = Declare(x, start)
    cond = BinOp("<=", j, end)

    stmt0 = Declare(i, start)
    stmt1 = Assign(i, BinOp("*", j, double_it))
    stmt2 = Assign(x, BinOp("+", x, i))
    stmt3 = Assign(j, BinOp("+", j, increment))

    loop_statements = ASTSequence([stmt0, stmt1, stmt2, stmt3])
    loop = DoWhile(loop_statements, cond)

    s = ASTSequence([stmt_init_j, stmt_init_x, loop])

    assert r.eval(s) == 9


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

    stmt_init_j = Declare(j, start)
    stmt_init_x = Declare(x, start)
    ##change is here
    cond = BinOp(">=", j, end)

    stmt0 = Declare(i, start)
    stmt1 = Assign(i, BinOp("*", j, double_it))
    stmt2 = Assign(x, BinOp("+", x, i))
    stmt3 = Assign(j, BinOp("+", j, increment))

    loop_statements = ASTSequence([stmt0, stmt1, stmt2, stmt3])
    loop = DoWhile(loop_statements, cond)

    s = ASTSequence([stmt_init_j, stmt_init_x, loop])

    assert r.eval(s) == 1


def test_nested_assignment_scope_loops():

    # int c = 0
    # int i = 0

    # while(i<10):
    #     int j = 0

    #     while(j<10):
    #         int i=5

    #         while(i>0):
    #             c=c+1
    #             i=i-1

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
    five = NumLiteral(5)

    declare_c = Declare(c, start)
    declare_i = Declare(i, start)

    innermost_loop_cond = BinOp(">", i, start)
    stmt_innermost_1 = Assign(c, BinOp("+", c, increment))
    stmt_innermost_2 = Assign(i, BinOp("-", i, increment))

    innermost_loop = While(
        innermost_loop_cond, ASTSequence([stmt_innermost_1, stmt_innermost_2])
    )

    second_loop_cond = BinOp("<", j, end)

    second_loop_stmt1 = Declare(i, five)
    second_loop_stmt2 = innermost_loop
    second_loop_stmt3 = Assign(j, BinOp("+", j, increment))

    second_loop = While(
        second_loop_cond,
        ASTSequence([second_loop_stmt1, second_loop_stmt2, second_loop_stmt3]),
    )

    outermost_loop_cond = BinOp("<", i, end)

    outermost_loop_stmt1 = Declare(j, start)
    outermost_loop_stmt2 = second_loop
    outermost_loop_stmt3 = Assign(i, BinOp("+", i, increment))

    outermost_loop = While(
        outermost_loop_cond,
        ASTSequence([outermost_loop_stmt1, outermost_loop_stmt2, outermost_loop_stmt3]),
    )

    prgrm = ASTSequence([declare_c, declare_i, outermost_loop])

    assert r.eval(prgrm) == 10


# strings test


def test_strings_assignment():
    r = RuntimeEnvironment()

    x = Variable("x")
    val = StringLiteral("Jack")
    val2 = StringLiteral("Bauer")

    declare_x = Declare(x, val)
    assign_x = Assign(x, val2)

    block = ASTSequence([declare_x, assign_x])

    assert r.eval(block) == "Bauer"


def test_strings_concat():
    r = RuntimeEnvironment()

    x = Variable("x")
    y = Variable("y")
    val = StringLiteral("Jack")
    val2 = StringLiteral("Bauer")

    declare_x = Declare(x, val)
    declare_y = Declare(y, val2)

    concat = BinOp("+", x, y)
    assign_x = Assign(x, concat)

    block = ASTSequence([declare_x, declare_y, assign_x, x])

    assert r.eval(block) == "JackBauer"


def strings_concat_error():
    r = RuntimeEnvironment()

    x = Variable("x")
    y = Variable("y")
    val = StringLiteral("Jack")
    val2 = NumLiteral(10)

    declare_x = Declare(x, val)
    declare_y = Declare(y, val2)

    concat = BinOp("+", x, y)
    assign_x = Assign(x, concat)

    block = ASTSequence([declare_x, declare_y, assign_x, x])

    assert r.eval(block) == InvalidConcatenationError


def test_strings_slicing():
    r = RuntimeEnvironment()

    x = Variable("x")
    val = StringLiteral("JackBauer")
    y = Variable("y")

    declare_x = Declare(x, val)
    strt = NumLiteral(0)
    end = NumLiteral(4)
    sliced = StringSlice(x, strt, end)
    declare_y = Declare(y, sliced)

    block = ASTSequence([declare_x, declare_y, y])
    assert r.eval(block) == "Jack"


def test_list_assgn_and_variability():
    r = RuntimeEnvironment()

    x = Variable("x")
    val = ListObject(
        [NumLiteral(1), NumLiteral(2), NumLiteral(3), NumLiteral(4), NumLiteral(5)],
        Fraction,
    )
    y = Variable("y")

    declare_x = Declare(x, val)
    declare_y = Declare(y, x)

    block = ASTSequence([declare_x, declare_y, y])

    assert r.eval(block) == [1, 2, 3, 4, 5]


def test_list_cons():
    r = RuntimeEnvironment()

    x = Variable("x")
    val = ListObject(
        [NumLiteral(1), NumLiteral(2), NumLiteral(3), NumLiteral(4), NumLiteral(5)],
        Fraction,
    )
    y = Variable("y")

    declare_x = Declare(x, val)
    declare_y = Declare(y, x)

    z = Variable("z")
    w = Variable("w")
    declare_z = Declare(z, NumLiteral(4))
    declare_w = Declare(w, NumLiteral(5))

    add_to_y = ListCons(BinOp("+", z, w), y)

    block = ASTSequence([declare_x, declare_y, declare_w, declare_z, add_to_y, y])

    assert r.eval(block) == [9, 1, 2, 3, 4, 5]


def list_type_wont_change_error():
    r = RuntimeEnvironment()

    x = Variable("x")
    val = ListObject(
        [NumLiteral(1), NumLiteral(2), NumLiteral(3), NumLiteral(4), NumLiteral(5)],
        Fraction,
    )
    y = Variable("y")

    declare_x = Declare(x, val)
    declare_y = Declare(y, x)

    z = Variable("z")

    declare_z = Declare(z, StringLiteral("JackBauer"))
    add_to_y = ListCons(z, y)

    block = ASTSequence([declare_x, declare_y, declare_z, add_to_y, y])

    assert r.eval(block) == ["JackBauer", 1, 2, 3, 4, 5]


def mut_var_wont_change_type():
    r = RuntimeEnvironment()
    x = Variable("x")

    declare_x = Declare(x, NumLiteral(5))
    assign_x = Assign(x, StringLiteral("JackBauer"))

    block = ASTSequence([declare_x, assign_x])

    # assertion will fail as Fraction type variable "x" can't be set to a string now.
    assert r.eval(block) == "JackBauer"


def test_list_head():
    r = RuntimeEnvironment()

    x = Variable("x")
    val = ListObject(
        [NumLiteral(1), NumLiteral(2), NumLiteral(3), NumLiteral(4), NumLiteral(5)],
        Fraction,
    )
    y = Variable("y")

    declare_x = Declare(x, val)
    declare_y = Declare(y, x)

    z = Variable("z")
    w = Variable("w")
    declare_z = Declare(z, NumLiteral(4))
    declare_w = Declare(w, NumLiteral(5))

    add_to_y = ListCons(BinOp("+", z, w), y)
    get_y_head = ListOp("head", y)

    block = ASTSequence(
        [declare_x, declare_y, declare_w, declare_z, add_to_y, get_y_head]
    )

    assert r.eval(block) == 9


def test_list_tail():
    r = RuntimeEnvironment()

    x = Variable("x")
    val = ListObject(
        [NumLiteral(1), NumLiteral(2), NumLiteral(3), NumLiteral(4), NumLiteral(5)],
        Fraction,
    )
    y = Variable("y")

    declare_x = Declare(x, val)
    declare_y = Declare(y, x)

    z = Variable("z")
    w = Variable("w")
    declare_z = Declare(z, NumLiteral(4))
    declare_w = Declare(w, NumLiteral(5))

    add_to_y = ListCons(BinOp("+", z, w), y)
    get_y_tail = ListOp("tail", y)

    block = ASTSequence(
        [declare_x, declare_y, declare_w, declare_z, add_to_y, get_y_tail]
    )

    assert r.eval(block) == [1, 2, 3, 4, 5]


def test_list_isempty():
    r = RuntimeEnvironment()

    x = Variable("x")
    val = ListObject(
        [NumLiteral(1), NumLiteral(2), NumLiteral(3), NumLiteral(4), NumLiteral(5)],
        Fraction,
    )
    y = Variable("y")

    declare_x = Declare(x, val)
    declare_y = Declare(y, x)

    z = Variable("z")
    w = Variable("w")
    declare_z = Declare(z, NumLiteral(4))
    declare_w = Declare(w, NumLiteral(5))

    add_to_y = ListCons(BinOp("+", z, w), y)
    get_y_isempty = ListOp("is-empty?", y)

    block = ASTSequence(
        [declare_x, declare_y, declare_w, declare_z, add_to_y, get_y_isempty]
    )

    assert r.eval(block) == False


def test_list_isempty_true():
    r = RuntimeEnvironment()

    x = Variable("x")
    val = ListObject([], Fraction)
    y = Variable("y")

    declare_x = Declare(x, val)
    declare_y = Declare(y, x)
    get_y_isempty = ListOp("is-empty?", y)

    block = ASTSequence([declare_x, declare_y, get_y_isempty])

    assert r.eval(block) == True

# testing for function

def test_for_func():
    r = RuntimeEnvironment()
    a = NumLiteral(9)
    t  = Variable("a")
    li = [t]
    li_ = [a]
    f = Print(t)
    f_2 = funct_ret(a)
    f_3 = ASTSequence([f,f_2])
    go = funct_def(Variable("hi"), li, f_3)
    go_ = funct_call(Variable("hi"), li_)  
    r.eval(go)
    assert(r.eval(go_)==9)

# test for reccursive functions
def test_rec_funct():
    r = RuntimeEnvironment()
    a = NumLiteral(7)
    a2 = NumLiteral(1)
    t  = Variable("a")
    li = [t]
    li_ = [a]
    cond = BinOp("<=",t ,a2)
    e1 = funct_ret(a2)
    
    e2_1 = Assign(t,BinOp("-",t,a2))
    e4 = funct_call(Variable("hi"), li)
    e2_2 = funct_ret(BinOp("*",BinOp("+",t,a2),e4))
    e2 = ASTSequence([e2_1, e2_2])
    f = If(cond, e1, e2)
    go = funct_def(Variable("hi"), li, f)
    go_ = funct_call(Variable("hi"), li_)
    r.eval(go)
    assert(r.eval(go_)==5040)
    
# main
if __name__ == "__main__":
    test_eval()
    test_bool_eval()
    test_sequence_eval()
    test_greater_than()
    test_for_loop()
    test_sequence_and_assign()
    test_while()
    test_while_initial_cond_false()
    test_do_while_initial_cond_true()
    test_do_while_initial_cond_false()
    test_nested_assignment_scope_loops()

    test_strings_assignment()
    test_strings_concat()
    test_strings_slicing()

    test_list_assgn_and_variability()
    test_list_cons()
    test_list_head()
    test_list_tail()
    test_list_isempty()
    test_list_isempty_true()
    test_for_func()
    test_rec_funct()

    # ERROR TESTS

    # 1
    # strings_concat_error()  #will display error for concatenating number with string
    # - won't be detected by pytest, will be detected when running test.py

    # 2
    # list_type_wont_change_error() #will display error for inserting an element of different type in a list
    # - won't be detected by pytest, will be detected when running test.py

    # 3
    # mut_var_wont_change_type()  #will display error for trying to assign a string value to a variable
    # initially declared as a number.
