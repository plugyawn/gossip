from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from utils.datatypes import AST, NumLiteral, BinOp, Variable, Value, Let, If, BoolLiteral, UnOp, ASTSequence, Variable, Assign, ForLoop, Range, Print
from utils.errors import DefinitionError, InvalidProgramError

class RuntimeEnvironment():
    """
    The runtime environment. Instantiate to start a new environment.
    Includes, most importantly, the eval method, which evaluates an AST
    recursively.
    """
    def __init__(self):
        self.environments = []
        self.environments.append({})
        self.environment = self.environments[0]
        self.scope = 0

    def eval(self, program: AST or ASTSequence, environment = None, reset_scope = False) -> Value:
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
                max_depth = self.scope
                while max_depth >= 0:
                    if name in self.environments[max_depth]:
                        return self.environments[max_depth][name]
                    max_depth -= 1

                raise DefinitionError(name)

            case ASTSequence(seq):
                """
                Special case. Evaluates all but the last element in a loop, 
                then returns the evaluation of the last element.
                """
                for ast in seq[:-1]:
                    self.eval(ast)

                return self.eval(seq[-1])

            case Assign(Variable(name), e1):
                """
                Special case. Assigns a value to a variable.
                """

                v1 = self.eval(e1)
                self.environments[0] = self.environments[0] | { name: v1 }
                return v1

            case Let(Variable(name), e1, e2):
                """
                Let is a special case. It evaluates e1, then adds the result
                to the environment, then evaluates e2 with the new environment.
                """
                value = self.eval(e1)
                self.scope += 1
                self.environments.append({ name: value })
                expression = self.eval(e2)
                self.environments.pop()
                self.scope -= 1
                return expression

            case Range(left, right):
                """
                Evaluates and returns range from left to return, as an ASTSequence.
                """
                AST_sequence = []
                for i in range(int(left.value), int(right.value)+1):
                    AST_sequence.append(NumLiteral(i))
                return ASTSequence(AST_sequence)

            case Print(expression):
                if isinstance(expression, ASTSequence):
                    expression_list = expression.seq
                    for expression in expression_list[:-1]:
                        print(expression.value) # TODO replace with something like: extract_value(exp)
                                                # TODO so it works both for strings and numbers.
                    print(expression_list[-1].value, end="")
                    return expression_list[-1].value
                else:
                    to_return = self.eval(expression)
                    print(to_return)
                    return to_return

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

            case BinOp("=", Variable(name), right):
                right = self.eval(right)
                self.environments[0] = self.environments[0] | { name: right }
                return right

            # Unary operation is the same, except for the operator.
            case UnOp("-", right):
                return 0 - self.eval(right)

            # Again, If is different, so we define it separately.
            case If(cond, e1, e2):
                if self.eval(cond) == True:
                    self.scope += 1
                    to_return = self.eval(e1)
                    self.scope -= 1
                else:
                    self.scope += 1
                    to_return = self.eval(e2)
                    self.scope -= 1
                
                return to_return
            
            case ForLoop(Variable(name), sequence, stat):
                if not isinstance(sequence, ASTSequence):
                    sequence = self.eval(sequence)
                length = sequence.length
                value_list = sequence.seq
                for expression in value_list: 
                    v1 = self.eval(expression)
                    self.scope += 1
                    self.environments.append({ name : v1 })
                    result = self.eval(stat)
                    self.scope -= 1
                    self.environments.pop()
                return(result)
                        
        raise InvalidProgramError(f"Runtime environment does not support program: {program}.")
