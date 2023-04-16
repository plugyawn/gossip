from dataclasses import dataclass
from utils.datatypes import Value
from typing import Union, Mapping, List, Optional
from utils.errors import *
from utils.datatypes import *

@dataclass
class Label:
    target: int

class I:
    """The instructions for our stack VM."""
    @dataclass
    class PUSH:
        val: Value

    @dataclass
    class UMINUS:
        pass

    @dataclass
    class ADD:
        pass

    @dataclass
    class SUB:
        pass

    @dataclass
    class MUL:
        pass

    @dataclass
    class DIV:
        pass

    @dataclass
    class QUOT:
        pass

    @dataclass
    class REM:
        pass

    @dataclass
    class EXP:
        pass

    @dataclass
    class EQ:
        pass

    @dataclass
    class NEQ:
        pass

    @dataclass
    class LT:
        pass

    @dataclass
    class GT:
        pass

    @dataclass
    class LE:
        pass

    @dataclass
    class GE:
        pass

    @dataclass
    class JMP:
        label: Label

    @dataclass
    class JMP_IF_FALSE:
        label: Label

    @dataclass
    class JMP_IF_TRUE:
        label: Label

    @dataclass
    class NOT:
        pass

    @dataclass
    class DUP:
        pass

    @dataclass
    class POP:
        pass

    @dataclass
    class LOAD:
        name: str

    @dataclass
    class STORE:
        name: str

    @dataclass
    class PUSHFN:
        entry: Label

    @dataclass
    class CALL:
        pass

    @dataclass
    class RETURN:
        pass

    @dataclass
    class HALT:
        pass

    @dataclass
    class DECLARE:
        name: str
        # localID: int
        pass

    @dataclass
    class PUSH_FRAME:
        pass

    @dataclass
    class POP_FRAME:
        pass
    @dataclass
    class LOAD_SCOPE:
        name : str
    @dataclass
    class STORE_SCOPE:
        name : str
    
    @dataclass
    class PRINT:
        pass

Instruction = (
      I.PUSH
    | I.ADD
    | I.SUB
    | I.MUL
    | I.DIV
    | I.QUOT
    | I.REM
    | I.NOT
    | I.UMINUS
    | I.JMP
    | I.JMP_IF_FALSE
    | I.JMP_IF_TRUE
    | I.DUP
    | I.POP
    | I.HALT
    | I.EQ
    | I.NEQ
    | I.LT
    | I.GT
    | I.LE
    | I.GE
    | I.LOAD
    | I.STORE
    | I.PUSHFN
    | I.CALL
    | I.RETURN
    | I.DECLARE
    | I.PUSH_FRAME
    | I.POP_FRAME
    | I.STORE_SCOPE
    | I.LOAD_SCOPE
    | I.PRINT
)





@dataclass
class ByteCode:
    insns: List[Instruction]

    def __init__(self):
        self.insns = []

    def label(self):
        return Label(-1)

    def emit(self, instruction):
        self.insns.append(instruction)

    def emit_label(self, label):
        label.target = len(self.insns)
    
    def pop(self):
        self.insns.pop()



# def print_bytecode(code: ByteCode):
#     for i, insn in enumerate(code.insns):
#         match insn:
#             case I.JMP(Label(offset)) | I.JMP_IF_TRUE(Label(offset)) | I.JMP_IF_FALSE(Label(offset)):
#                 print(f"{i:=4} {insn.__class__.__name__:<15} {offset}")
#             case I.LOAD(localID) | I.STORE(localID):
#                 print(f"{i:=4} {insn.__class__.__name__:<15} {localID}")
#             case I.PUSH(value):
#                 print(f"{i:=4} {'PUSH':<15} {value}")
#             case I.PUSHFN(Label(offset)):
#                 print(f"{i:=4} {'PUSHFN':<15} {offset}")
#             case _:
#                 print(f"{i:=4} {insn.__class__.__name__:<15}")




#class to store a list of local variables of a function- only function calls
#create a new frame.
class Frame:
    retaddr: int
    # dynamicLink: 'Frame'

    def __init__(self, retaddr = -1, dynamicLink = None):
        MAX_LOCALS = 32
        self.locals = {}
        self.retaddr = retaddr
        # self.dynamicLink = dynamicLink





#converting the AST from the parser to the Bytecode list of instructions

def codegen(program: AST) -> ByteCode:
    code = ByteCode()
    code.emit(I.PUSH("stack bottom"))
    do_codegen(program, code)
    code.emit(I.HALT())
    return code




def do_codegen (program: AST, code: ByteCode) -> None:

    #helper function to avoid passing the "code" everytime
    def codegen_(program):
        do_codegen(program, code)

    simple_ops = {
        "+": I.ADD(),
        "-": I.SUB(),
        "*": I.MUL(),
        "/": I.DIV(),
        "quot": I.QUOT(),
        "rem": I.REM(),
        "<": I.LT(),
        ">": I.GT(),
        "<=": I.LE(),
        ">=": I.GE(),
        "==": I.EQ(),
        "!=": I.NEQ(),
        "not": I.NOT(),
        "**": I.EXP()
    }

    match program:
        case NumLiteral(value) | BoolLiteral(value) | StringLiteral(value):
            code.emit(I.PUSH(value))

        # case UnitLiteral():
        #     code.emit(I.PUSH(None))

        case BinOp(operator, left, right) if operator in simple_ops:
            codegen_(left)
            codegen_(right)
            code.emit(simple_ops[operator])

        case BinOp("&&", left, right):
            E = code.label()
            codegen_(left)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_FALSE(E))
            code.emit(I.POP())
            codegen_(right)
            code.emit_label(E)

        case BinOp("||", left, right):
            E = code.label()
            codegen_(left)
            code.emit(I.DUP())
            code.emit(I.JMP_IF_TRUE(E))
            code.emit(I.POP())
            codegen_(right)
            code.emit_label(E)


        case UnOp("-", right):
            codegen_(right)
            code.emit(I.UMINUS())


        case ASTSequence(seq):

            for ast in seq[:-1]:
                codegen_(ast)
                code.emit(I.POP()) #pops the value of each intermediate expression in the AST, so that we can
                                   #return the evaluation of the last expression in the Sequence.
            codegen_(seq[-1])


        case If(cond, e1, e2):
            E = code.label()
            F = code.label()

            codegen_(cond)
            code.emit(I.JMP_IF_FALSE(F))
            code.emit(I.PUSH_FRAME)
            codegen_(e1)
            code.emit(I.POP_FRAME)
            code.emit(I.JMP(E))

            code.emit_label(F)
            code.emit(I.PUSH_FRAME)
            codegen_(e2)
            code.emit(I.POP_FRAME)
            code.emit_label(E)



        case While(cond, body):
            B = code.label()
            E = code.label()
            code.emit_label(B)
            codegen_(cond)
            code.emit(I.JMP_IF_FALSE(E))

            #each iteration of the loop gets it's own frame
            code.emit(I.PUSH_FRAME)
            codegen_(body)
            code.emit(I.POP_FRAME)
            code.emit(I.POP()) ###IS THIS REQUIRED??
            #the frame is popped after the iteration is over, also the value after
            #evaluation of the iteration is popped- while returns a None value now.

            code.emit(I.JMP(B))
            code.emit_label(E)
            code.emit(I.PUSH(None))


        case Variable() as v:
            code.emit(I.LOAD(v.name))

        # case Let(Variable() as v, e1, e2) | LetMut(Variable() as v, e1, e2):
        #     codegen_(e1)
        #     code.emit(I.STORE(v.localID))
        #     codegen_(e2)

        case Declare(Variable() as v,value):
            codegen_(value)
            code.emit(I.DECLARE(v.name))

        # case Put(Variable() as v, e):
        #     codegen_(e)
        #     code.emit(I.STORE(v.localID))
        #     code.emit(I.PUSH(None))

        case Assign(Variable() as v, expression):
            codegen_(expression)
            code.emit(I.STORE(v.name))





        #TODO change these
        case funct_def(Variable(name), arg_list, body):
            EXPRBEGIN = code.label()
            FBEGIN = code.label()
            code.emit(I.STORE_SCOPE(name))
            code.emit(I.JMP(EXPRBEGIN))
            code.emit_label(FBEGIN)
            for param in reversed(arg_list):
                code.emit(I.STORE(param.name))
            codegen_(body)
            code.emit_label(EXPRBEGIN)
            code.emit(I.PUSHFN(FBEGIN))
            code.emit(I.STORE(name))


        case funct_call(Variable(name), args):
            for arg in args:
                codegen_(arg)
            code.emit(I.LOAD_SCOPE(name))
            code.emit(I.LOAD(name))
            code.emit(I.CALL())
        
        case funct_ret(funct_val):
            codegen_(funct_val)
            code.emit(I.RETURN())
        
        case Print(expression):
            codegen_(expression)
            code.emit(I.PRINT())


        # case TypeAssertion(expr, _):
        #     codegen_(expr)









#The virtual machine class- stores the instructions(bytecode), the instruction pointer(ip)
#and the stack(data). VM also accesses a Frame for local variables(currentFrame)

class VM:
    bytecode: ByteCode
    ip: int
    data: List[Value]
    allFrames: List[Frame]
    scp: int
    funct_sc : List[int]
    def __init__(self):
        self.ip = 0
        self.allFrames=[Frame()]
        self.scp=0
        self.funct_sc = []
        self.data = []
    
    def add_bytcode(self,bytcode):
        self.bytecode = bytcode
        self.ip = 0

    def add_frame(self, index = None):

        if(index == None):
            new_frame = Frame()
            self.allFrames.append(new_frame)
        else:
            new_frame = Frame()
            self.allFrames.insert(index,new_frame)

    def end_frame(self):
        self.allFrames.pop()

    # def load(self, bytecode):
    #     self.bytecode = bytecode
    #     self.restart()


    def restart(self):
        self.ip = 0
        self.data = []
        self.allFrames=[Frame()]
        

    def ret_scope(self):
        if(len(self.funct_sc) == 0):
            return(len(self.allFrames) - 1)
        else:
            return(self.funct_sc[-1])

    def execute(self) -> Value:
        # print(self.bytecode)
        while True:

            # print(self.data)
            # print(self.allFrames[self.scp].locals)

            if not self.ip < len(self.bytecode.insns):
                raise RuntimeError()

            match self.bytecode.insns[self.ip]:
                case I.PUSH(val):
                    self.data.append(val)
                    self.ip += 1


                case I.PUSHFN(Label(offset)):
                    self.data.append(offset)
                    self.ip += 1

                case I.CALL():
                    # self.currentFrame = Frame (
                    #     retaddr=self.ip + 1
                    # )
                    # self.allFrames.append(self.currentFrame)
                    cf = self.data.pop()
                    cur_scope = self.data.pop()
                    self.add_frame(cur_scope + 1)
                    self.allFrames[cur_scope + 1].retaddr = self.ip + 1
                    self.scp = cur_scope + 1
                    self.funct_sc.append(self.scp)
                    self.ip = cf

                case I.RETURN():
                    self.ip = self.allFrames[self.scp].retaddr
                    # self.ip = self.currentFrame.retaddr
                    self.allFrames.pop(self.scp)
                    self.funct_sc.pop()
                    self.scp = self.ret_scope()



                case I.LOAD_SCOPE(name):
                    scp = self.ret_scope()
                    val = None
                    
                    while(scp>=0):
                        if name in self.allFrames[scp].locals:
                            val = self.allFrames[scp].locals[name]['scope']
                        else:
                            scp-=1
                    
                    if val is None:
                        raise DeclarationError(name)
                    else:
                        self.data.append(val)
                        self.ip += 1

                case I.STORE_SCOPE(name):
                    scp = self.ret_scope()
        

                    if name in self.allFrames[scp].locals:
                        raise VariableRedeclarationError(name)
                    
                    v = -1
                    tp = type(v)

                    self.allFrames[scp].locals[name] = {}
                    self.allFrames[scp].locals[name]['value'] = v
                    self.allFrames[scp].locals[name]['type'] = tp
                    self.allFrames[scp].locals[name]['scope'] = scp

                    self.ip+=1


                case I.UMINUS():
                    op = self.data.pop()
                    self.data.append(-op)
                    self.ip += 1

                case I.ADD():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left+right)
                    self.ip += 1

                case I.SUB():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left-right)
                    self.ip += 1

                case I.MUL():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left*right)
                    self.ip += 1

                case I.DIV():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left/right)
                    self.ip += 1

                case I.EXP():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left**right)
                    self.ip += 1

                case I.QUOT():
                    right = self.data.pop()
                    left = self.data.pop()
                    if left.denominator != 1 or right.denominator != 1:
                        raise RuntimeError("Can't find quotient on division by non-integral values.")
                    left, right = int(left), int(right)
                    self.data.append(Fraction(left // right, 1))
                    self.ip += 1

                case I.REM():
                    right = self.data.pop()
                    left = self.data.pop()
                    if left.denominator != 1 or right.denominator != 1:
                        raise RuntimeError("Can't find remainder on division by non-integral values.")
                    left, right = int(left), int(right)
                    self.data.append(Fraction(left % right, 1))
                    self.ip += 1

                case I.EQ():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left==right)
                    self.ip += 1

                case I.NEQ():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left!=right)
                    self.ip += 1

                case I.LT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left<right)
                    self.ip += 1

                case I.GT():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left>right)
                    self.ip += 1

                case I.LE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left<=right)
                    self.ip += 1

                case I.GE():
                    right = self.data.pop()
                    left = self.data.pop()
                    self.data.append(left>=right)
                    self.ip += 1

                case I.JMP(label):
                    self.ip = label.target

                case I.JMP_IF_FALSE(label):
                    op = self.data.pop()

                    if not op:
                        self.ip = label.target
                    else:
                        self.ip += 1

                case I.JMP_IF_TRUE(label):
                    op = self.data.pop()

                    if op:
                        self.ip = label.target
                    else:
                        self.ip += 1

                case I.NOT():
                    op = self.data.pop()
                    self.data.append(not op)
                    self.ip += 1

                case I.DUP():
                    op = self.data.pop()
                    self.data.append(op)
                    self.data.append(op)
                    self.ip += 1

                case I.POP():
                    self.data.pop()
                    self.ip += 1

                case I.LOAD(name):
                    scp = self.ret_scope()
                    # print(scp)
                    val = None
                    
                    while(scp>=0):
                        if name in self.allFrames[scp].locals:
                            val = self.allFrames[scp].locals[name]['value']
                            break
                        else:
                            scp-=1
                    
                    if val is None:
                        raise DeclarationError(name)
                    else:
                        self.data.append(val)
                        self.ip += 1


                case I.STORE(name):
                    v = self.data.pop()
                    tp = type(v)
                    var_type = None

                    scp = self.ret_scope()
                    while(scp>=0):
                        if name in self.allFrames[scp].locals:
                            var_type = self.allFrames[scp].locals[name]['type']
                            break
                        else:
                            scp-=1
                    

                    if var_type is None:
                        raise DeclarationError(name)
                    
                    if tp is not var_type:
                        raise BadAssignment(name,var_type,tp)
                    
                    self.allFrames[scp].locals[name]['value'] = v                    
                    self.ip += 1


                
                case I.DECLARE(name):
                    scp = self.ret_scope()

                    if name in self.allFrames[scp].locals:
                        raise VariableRedeclarationError(name)
                    
                    v = self.data.pop()
                    tp = type(v)

                    self.allFrames[scp].locals[name] = {}
                    self.allFrames[scp].locals[name]['value'] = v
                    self.allFrames[scp].locals[name]['type'] = tp

                    self.ip+=1

                case I.PUSH_FRAME():
                    self.add_frame()
                
                case I.POP_FRAME():
                    self.end_frame()
                
                case I.PRINT():
                    val = self.data.pop()
                    print(val)
                    self.ip+=1

                case I.HALT():
                    #automatically exits the execution loop.
                    return self.data.pop()



