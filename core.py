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
        self.environment = {}

    def eval(self, program: AST or ASTSequence, environment = None) -> Value:
        """
        Recursively evaluates an AST or ASTSequence, returning a Value.
        By default, retains the environment from the runtime environment.
        However, you can pass in an environment to override this.
        """
        if environment:
            self.environment = environment
        if not self.environment:
            self.environment = {}
        
        match program:

            case NumLiteral(value):
                return value

            case Variable(name):
                if name in self.environment:
                    return self.environment[name]

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
                return self.eval(e2, self.environment | { name: v1 })

            # Binary operations are all the same, except for the operator.
            case BinOp("+", left, right):
                environment = self.environment
                left = self.eval(left, environment)
                right = self.eval(right, environment)
                return left + right
            case BinOp("-", left, right):
                left = self.eval(left, environment)
                right = self.eval(right, environment)
                return left - right
            case BinOp("*", left, right):
                left = self.eval(left, environment)
                right = self.eval(right, environment)
                return left * right
            case BinOp("/", left, right):
                left = self.eval(left, environment)
                right = self.eval(right, environment)
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
                return self.eval(left) > self.eval(right)
            case BinOp("<=", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return self.eval(left) <= self.eval(right)
            case BinOp(">=", left, right):
                left = self.eval(left)
                right = self.eval(right)
                return self.eval(left) >= self.eval(right)
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
                    return self.eval(e1)
                else:
                    return self.eval(e2)
        raise InvalidProgramError(program)
