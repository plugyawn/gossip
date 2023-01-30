from dataclasses import dataclass
from utils.datatypes import AST, NumLiteral, BinOp, Variable, Let, Value, If, BoolLiteral, UnOp, ASTSequence, NumType, BoolType
from utils.errors import TypeCheckError

class StaticTypeChecker:
    def __init__(self):
        pass
    
    def check(self, program: AST) -> AST:
        match program:
            case NumLiteral() | BoolLiteral():
                return program

            case BinOp(op, left, right) if op in ["+", "-", "*", "/", "<", ">", "<=", ">="]:
                left = self.check(left)
                right = self.check(right)
                if left.type != NumType() or right.type != NumType():
                    raise TypeCheckError(oprtype=NumType())
                return BinOp(op, left, right, NumType())
            
            case BinOp(op, left, right) if op in ["==", "!="]:
                left = self.check(left)
                right = self.check(right)
                if (left.type != right.type):
                    raise TypeCheckError(message="The operands do not have the same type.")
                elif(left.type == NumType()) or (left.type == BoolType()):
                    return BinOp(op, left, right, BoolType())                    
                else:
                    raise TypeCheckError(message="The operands should be either NumType or BoolType.")
            
            case BinOp(op, left, right) if op in ["&&", "||"]:
                left = self.check(left)
                right = self.check(right)
                if left.type != BoolType() or right.type != BoolType():
                    raise TypeCheckError(oprtype=BoolType())
                return BinOp(op, left, right, BoolType())

            case UnOp(op, right) if op in ["-"]:
                right = self.check(right)
                if right.type != NumType():
                    raise TypeCheckError(oprtype=NumType())
                return UnOp(op, right)
            
            case If(cond, e1, e2):
                cond = self.check(cond)
                e1 = self.check(e1)
                e2 = self.check(e2)
                if cond.type != BoolType():
                    raise TypeCheckError(oprtype=BoolType())
                if e1.type != e2.type:
                    raise TypeCheckError(message="The two branches do not have the same type.")
                return If(cond, e1, e2, e1.type)
            
            case ASTSequence(seq):
                seq_type = []
                for i in range(len(seq)):
                    seq_type[i] = self.check(seq[i])
                return ASTSequence(seq, seq_type[-1].type)
            
            case Let(var, e1, e2):
                e1 = self.check(e1)
                var.type = e1.type
                e2 = self.check(e2)
                return Let(var, e1, e2)