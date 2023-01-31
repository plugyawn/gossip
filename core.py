from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from utils.datatypes import AST, NumLiteral, BinOp, Variable, Let, Value, If, BoolLiteral, UnOp, ASTSequence
from utils.errors import DefinitionError, InvalidProgramError

class RuntimeEnvironment():
    """
    The runtime environment. Instantiate to start a new environment.
    Includes, most importantly, the eval method, which evaluates an AST
    recursively.
    """
    def __init__(self):
        self.environment = []
        self.environment.append({})
        self.scope = 0 

    def eval(self, program: AST or ASTSequence) -> Value:
        """
        Recursively evaluates an AST or ASTSequence, returning a Value.
        By default, retains the environment from the runtime environment.
        However, you can pass in an environment to override this.
        """
        match program:

            case NumLiteral(value):
                return value

            case Variable(name):
                if name in self.environment[self.scope]:
                    return self.environment[self.scope][name]
                scope_1 = self.scope
                while(scope_1>=0):
                        if name in self.environment[scope_1]:
                            return self.environment[scope_1][name]
                        scope_1 = scope_1 - 1

                raise DefinitionError(name)

            case ASTSequence(seq):
                """
                Special case. Evaluates all but the last element in a loop, 
                then returns the evaluation of the last element.
                """
                for ast in seq[:-1]:
                    self.eval(ast)

                return self.eval(seq[-1])

            case Let(Variable(name), e1, e2):
                """
                Let is a special case. It evaluates e1, then adds the result
                to the environment, then evaluates e2 with the new environment.
                """
                v1 = self.eval(e1)
                self.scope = self.scope + 1
                dict = {name : v1}
                self.environment.append(dict)
                val = self.eval(e2)
                self.environment.pop()
                self.scope = self.scope - 1
                return(val)

            # Binary operations are all the same, except for the operator.
            case BinOp("+", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left + right
            case BinOp("-", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left - right
            case BinOp("*", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left * right
            case BinOp("/", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left / right
            case BinOp("==", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left == right
            case BinOp("!=", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left != right
            case BinOp("<", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left < right
            case BinOp(">", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left > right
            case BinOp("<=", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left <= right
            case BinOp(">=", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left >= right
            case BinOp("&&", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left and right
            case BinOp("||", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return left or right
            
            # Unary operation is the same, except for the operator.
            case UnOp("-", right):
                return 0 - self.eval(right)

            # Again, If is different, so we define it separately.
            case If(cond, e1, e2):
                if self.eval(cond) == True:
                    self.scope = self.scope + 1
                    val = self.eval(e1)
                    self.scope = self.scope - 1
                    return val
                else:
                    self.scope = self.scope + 1
                    val =  self.eval(e2)
                    self.scope = self.scope - 1
                    return val
        raise InvalidProgramError(program)
