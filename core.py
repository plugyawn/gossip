from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from utils.datatypes import AST, NumLiteral, BinOp, Variable, Value, Let, If, BoolLiteral, UnOp, ASTSequence, Variable, Assign, ForLoop, Range, Print, Declare, Assign, While, DoWhile, funct_call, funct_def, funct_ret
from utils.errors import DeclarationError, InvalidProgramError, InvalidCondition, VariableRedeclaration, AssignmentUsingNone

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
        self.func_defs = {}
        self.func_defns = []

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
                #can add one more part about variables declared without a value 
                #referring to outer scope variables with the same name
                scope_1 = self.scope
                while ( len(self.environments) < (scope_1+1)):
                    scope_1 = scope_1 - 1
                
                #adding the not None helps me to assign an inner-scope "x" which was declared None
                #with an outer-scope x

                #this bypasses the rule of referring to the innermost declaration of "x" because "x" when
                #declared None can create problems in Assign(x,(x+1))
                #Only in such cases where I want to assign the new None "x" using the value of an
                #outer "x"

                ## OR

                #We stay in the current scope, and raise an error that we are assigning a 
                # initially-None variable in terms of itself.

                while(scope_1>=0):
                        if name in self.environments[scope_1]:
                            return self.environments[scope_1][name]

                        #   if(self.environment[scope_1][name]==None):
                        #         raise AssignmentUsingNone(name)
                            
                        scope_1 = scope_1 - 1

                raise DeclarationError(name)
            
            
            #a declaration returns the value to be declared
            case Declare(Variable(name), value):
                while ( len(self.environments) < (self.scope+1)):
                    self.scope = self.scope - 1
                    
                value_to_be_declared = self.eval(value)
                curent_scope = self.scope

                if(name in self.environments[curent_scope]):
                    raise VariableRedeclaration(name)
                else:
                    self.environments[curent_scope][name] = value_to_be_declared

                return value_to_be_declared
            
            
            case Assign(Variable(name) ,expression):

                
                while ( len(self.environments) < (self.scope+1)):
                    self.scope = self.scope - 1
                scp = self.scope
                val = self.eval(expression)
                if(name in self.environments[scp]):
                    #variable has been declared in the current scope already
                    #so, update it's assignment
                    self.environments[scp][name]=val
                else:
                    flag = False
                    scope_x = scp-1

                    while(scope_x>=0):
                        if(name in self.environments[scope_x]):
                            #variable found declared in some outer scope
                            #so, apply the assignment in that outer scope

                            flag = True
                            self.environments[scope_x][name]=val
                            break
                        else:
                            scope_x=scope_x-1
                    
                    #trying to assign to an undeclared variable
                    if(flag==False):
                        raise DeclarationError(name)    
                
                return val
            

            case ASTSequence(seq):
                """
                Special case. Evaluates all but the last element in a loop, 
                then returns the evaluation of the last element.
                """
                for ast in seq[:-1]:
                    match ast:
                        case funct_ret(ret_val):
                            return self.eval(ast)
                        case _:
                            x = self.eval(ast)

                return self.eval(seq[-1])
            

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
            
            case While(cond, sequence):

                truth_value = self.eval(cond)

                if type(truth_value) != bool:
                    raise InvalidCondition(cond)
                
                final_value = None

                while(truth_value):

                    self.scope += 1
                    scp = self.scope
                    
                    current_scope_mappings={}
                    self.environments.append(current_scope_mappings)
                    final_value = self.eval(sequence)
                    
                    truth_value= self.eval(cond)
                    self.environments.pop()
                    self.scope -= 1
                
                return final_value
            
            case DoWhile(sequence, cond):

                final_value = None
                self.scope += 1
                scp = self.scope
                    
                current_scope_mappings={}
                self.environments.append(current_scope_mappings)
                final_value = self.eval(sequence)

                self.environments.pop()
                self.scope -= 1

                truth_value = self.eval(cond)

                if type(truth_value) != bool:
                    raise InvalidCondition
                
                while(truth_value):

                    self.scope += 1
                    scp = self.scope
                    
                    current_scope_mappings={}
                    self.environments.append(current_scope_mappings)
                    final_value = self.eval(sequence)
                    
                    truth_value= self.eval(cond)
                    self.environments.pop()
                    self.scope -= 1
                
                return final_value


            case funct_ret(funct_val):
                #print(funct_val)
                return(self.eval(funct_val))
            
            case funct_def(name, arg_list, body):
                func = [arg_list, body]
                self.func_defs[name] = func
                return(NumLiteral(0))

            #dynamic scoping on function calls 
            case funct_call(name, arg_val):
                if name in self.func_defs:
                    self.scope = self.scope + 1
                    dict = {}
                    arg_name = self.func_defs[name][0]
                    if(len(arg_name)!=len(arg_val)):
                        raise Exception("Not enough arguements")
                    for x in range(len(arg_name)):
                        v1 = self.eval(arg_val[x])
                        dict[arg_name[x].name] = v1
                    self.environments.append(dict)
                    m = self.eval(self.func_defs[name][1])
                    self.environments.pop()
                    self.scope -= 1 
                    return(m)
                else:
                    raise Exception("Function is not defined")           
            
            
            
                
        raise InvalidProgramError(f"Runtime environment does not support program: {program}.")
