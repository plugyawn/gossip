from dataclasses import dataclass
from utils.datatypes import *

class StaticTypeChecker:
    def __init__(self):
        pass
    
    def check(self, program: AST) -> AST:
        match program:
            case NumLiteral() | BoolLiteral() as e:
                return e

            case BinOp(op, left, right) if op in ["+", "-", "*", "/", "<", ">", "<=", ">="]:
                left = self.check(left)
                right = self.check(right)
                if left.type != NumType() or right.type != NumType():
                    raise TypeError(NumType())
                return BinOp(op, left, right, NumType())
            
            case BinOp(op, left, right) if op in ["==", "!="]:
                left = self.check(left)
                right = self.check(right)
                if (left.type != right.type):
                    raise TypeError(message="The operands do not have the same type.")
                elif(left.type != NumType()) or (left.type != BoolType()):
                    raise TypeError(message="The operands should be either NumType or BoolType.")
                else:
                    return BinOp(op, left, right, BoolType())
            