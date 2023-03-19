from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from utils.datatypes import AST, NumLiteral, BinOp, Variable, Value, Let, If, BoolLiteral, UnOp, ASTSequence, Variable, Assign, ForLoop, Range, Print, Declare, Assign, While, DoWhile, StringLiteral, ListObject, StringSlice, ListCons, ListOp, funct_call, funct_def, funct_ret
from utils.datatypes import NumType,BoolType,StringType,ListType

from utils.errors import DeclarationError, InvalidProgramError, InvalidConditionError, VariableRedeclarationError, AssignmentUsingNone, InvalidConcatenationError, IndexOutOfBoundsError, InvalidOperation, InvalidArgumentToList, ListError, ReferentialError, BadAssignment


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
            
            case BoolLiteral(value):
                return value
            
            case StringLiteral(value):
                return value
            
            case StringSlice(Variable(name),start, end):
                full_string = self.eval(Variable(name))

                #slice indices must be integers and our default type is Fraction for numbers
                strt = int(self.eval(start))
                d_end = int(self.eval(end))

                
                try:
                    return full_string[strt:d_end]
                except:
                    if(strt<0 or d_end>len(full_string)):
                        raise IndexOutOfBoundsError("Slice Index out of range")
                    else:
                        raise IndexOutOfBoundsError()

            case ListObject(elements,element_type):
                n = len(elements)

                for i in range(n):
                    if(type(self.eval(elements[i])) is not element_type):
                        raise InvalidArgumentToList(element_type)
                    elements[i] = self.eval(elements[i])
                
                return elements
            

            case ListCons(to_add, base_list):
                to_add = self.eval(to_add)
                the_type = None
                scp = self.scope

                if(isinstance(base_list,ListObject)):
                    the_type = base_list.element_type
                elif(isinstance(base_list,Variable)):

                    while(scp>=0):
                        if(base_list.name in self.environments[scp]):
                            the_type = self.environments[scp][base_list.name]['element_type']
                    
                        scp-=1

                    if(the_type==None):
                        raise ListError("Variable referenced during Cons operation doesn't exist.")
                                        
                else:
                    raise ListError("Argument to Cons() is not a list.")
                
                if(type(to_add) is not the_type):
                    raise ListError("Input element is not of the same type as given list type.")

                new_list = []
                new_list.append(to_add)
                
                if isinstance(base_list,ListObject):
                    for num in base_list:
                        new_list.append(num)
                else:
                    for num in self.eval(base_list):
                        new_list.append(num)
                

                if isinstance(base_list,Variable):
                    SCOPE = self.scope
                    self.environments[SCOPE][base_list.name]['value'] = new_list
                
                return new_list            
            

            case Variable(name):
                scope = self.scope
                while len(self.environments) < (scope + 1):
                    scope -= 1

                while scope >= 0:
                    if name in self.environments[scope]:
                        return self.environments[scope][name]['value']
                    scope -= 1

                raise DeclarationError(name)
            
            
            case Declare(Variable(name), value):

                curent_scope = self.scope
                if name in self.environments[curent_scope]:
                    return VariableRedeclarationError(name)

                if isinstance(value,ListObject):
                    elems = self.eval(value)
                    scp = self.scope
                    
                    self.environments[curent_scope][name] = {}
                    self.environments[scp][name]['value'] = elems
                    self.environments[scp][name]['type'] = list
                    self.environments[scp][name]['element_type'] = value.element_type

                    return elems
                
                elif isinstance(value,Variable):
                    value_to_be_declared = self.eval(value)
                    value_type = None
                    value_name = value.name
                    if_val_is_list_its_el_type = None

                    scp = self.scope
                    while len(self.environments) < (scp + 1):
                        scp-= 1

                    while scp >= 0:
                        if value_name in self.environments[scp]:
                            value_type = self.environments[scp][value_name]['type']

                            if(value_type is list):
                                if_val_is_list_its_el_type = self.environments[scp][value_name]['element_type']

                        scp -= 1

                    curent_scope = self.scope

                    if if_val_is_list_its_el_type == None:
                        
                        self.environments[curent_scope][name] = {}
                        self.environments[curent_scope][name]['value'] = value_to_be_declared
                        self.environments[curent_scope][name]['type'] = type(value_to_be_declared)

                    else:
                        
                        self.environments[curent_scope][name] = {}
                        self.environments[curent_scope][name]['value'] = value_to_be_declared
                        self.environments[curent_scope][name]['type'] = type(value_to_be_declared)
                        self.environments[curent_scope][name]['element_type'] = if_val_is_list_its_el_type
                
                    return value_to_be_declared

                else:
                    value_to_be_declared = self.eval(value)
                    curent_scope = self.scope
                    
                    
                    self.environments[curent_scope][name] = {}
                    self.environments[curent_scope][name]['value'] = value_to_be_declared
                    self.environments[curent_scope][name]['type'] = type(value_to_be_declared)

                    return value_to_be_declared
                
            
            case Assign(Variable(name), expression):
                val = self.eval(expression)

                var_type = None
                scp = self.scope

                if len(self.environments) < (scp + 1):
                    scp = len(self.environments) - 1 

                while scp >= 0:
                    if name in self.environments[scp]:
                        var_type = self.environments[scp][name]['type']
                        break 
                    scp -= 1
                
                if(var_type is not type(val)):
                    raise BadAssignment(name,var_type,type(val))

                if name in self.environments[scp]:
                    self.environments[scp][name]['value'] = val
                else:
                    flag = False
                    scope = self.scope - 1
                    while scope >= 0:
                        if name in self.environments[scope]:
                            flag = True
                            self.environments[scope][name]['value'] = val
                            break
                        else:
                            scope -= 1
                    
                    if not flag:
                        raise DeclarationError(name)    
                
                return val
            
            case ASTSequence(seq):
                """
                Special case. Evaluates all but the last element in a loop, 
                then returns the evaluation of the last element.
                """
                for ast in seq[:-1]:
                    x = self.eval(ast)

                return self.eval(seq[-1])
            

            case Let(Variable(name), e1, e2):
                """
                Let is a special case. It evaluates e1, then adds the result
                to the environment, then evaluates e2 with the new environment.
                """
                val = self.eval(e1)
                self.scope += 1
                self.environments.append({ name: {'value': val} })
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

            
            case ListOp("is-empty?", base_list):
                base_list = self.eval(base_list)

                if(len(base_list)!=0):
                    return False
                else:
                    return True

            case ListOp("head", base_list):
                base_list = self.eval(base_list)

                if(len(base_list)==0):
                    raise ListError("No head in an empty list")
                else:
                    return base_list[0]
            
            case ListOp("tail", base_list):
                base_list = self.eval(base_list)

                if(len(base_list)==0):
                    raise ListError("No tail in an empty list")
                else:
                    return base_list[1:]

            # Binary operations are all the same, except for the operator.
            case BinOp("+", left, right):
                try:
                    if(left.type==StringType and right.type==StringType):
                        print("gotcha")
                        dummy_string = left.value + right.value
                        return dummy_string
                    else:
                        left = self.eval(left)
                        right = self.eval(right)
                        return left + right
                except:
                    return InvalidConcatenationError

            case BinOp("-", left, right):
                left = self.eval(left)
                right = self.eval(right)
                try:
                    return left - right
                except:
                    raise InvalidOperation("-",left,right)
                
            case BinOp("*", left, right):
                left = self.eval(left)
                right = self.eval(right)
                try:
                    return left * right
                except:
                    raise InvalidOperation("*",left,right)
                
            case BinOp("/", left, right):
                left = self.eval(left)
                right = self.eval(right)
                try:
                    return left / right
                except:
                    raise InvalidOperation("/",left,right)
            
            case BinOp("%", left, right):
                left = self.eval(left)
                right = self.eval(right)

                try:
                    return left%right
                except:
                    raise InvalidOperation("%", left, right)
                
            case BinOp("==", left, right):
                left = self.eval(left)
                right = self.eval(right)
                
                try:
                    return left == right
                except:
                    raise InvalidOperation("==",left,right)
                
            case BinOp("!=", left, right):
                left = self.eval(left)
                right = self.eval(right)
                
                try:
                    return left != right
                except:
                    raise InvalidOperation("!=",left,right)
                
            case BinOp("<", left, right):
                left = self.eval(left)
                right = self.eval(right)

                try:
                    return left < right
                except:
                    raise InvalidOperation("<",left,right)
                
            case BinOp(">", left, right):
                left = self.eval(left)
                right = self.eval(right)

                try:
                    return left > right
                except:
                    raise InvalidOperation(">",left,right)
                
            case BinOp("<=", left, right):
                left = self.eval(left)
                right = self.eval(right)
                
                try:
                    return left <= right
                except:
                    raise InvalidOperation("<=",left,right)
                
            case BinOp(">=", left, right):
                left = self.eval(left)
                right = self.eval(right)
                
                try:
                    return left >= right
                except:
                    raise InvalidOperation(">=",left,right)
                
            case BinOp("&&", left, right):
                left = self.eval(left)
                right = self.eval(right)
                
                try:
                    return left and right
                except:
                    raise InvalidOperation("&&",left,right)
                
            case BinOp("||", left, right):
                left = self.eval(left)
                right = self.eval(right)
                
                try:
                    return left or right
                except:
                    raise InvalidOperation("||",left,right)

            # Unary operation is the same, except for the operator.
            case UnOp("-", right):
                try:
                    return 0 - self.eval(right)
                except:
                    InvalidOperation("Unary Negation",right)

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
                    return InvalidConditionError(cond)
                
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
                    return InvalidConditionError
                
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
            
            case funct_def(Variable(name), arg_list, body):
            
                func = [arg_list, body]
                funct_1 =  {"value":func, "type": str}
                scp = self.scope
                while len(self.environments) < (scp + 1):
                        scp-= 1
                
                self.environments[scp][name] = funct_1
                # print(self.environments)
                return(self.eval(NumLiteral(0)))
            

            #dynamic scoping on function calls 
            case funct_call(Variable(name), arg_val):
                self.scope +=1
                src = self.scope
                # print(src)
                if(len(self.environments)<self.scope + 1):
                    src = len(self.environments) - 1

                # print(src)
                while src >=0:
                    if name in self.environments[src]:  
                        dictt = {}
                        arg_name = self.environments[src][name]["value"][0]

                        if(len(arg_name)!=len(arg_val)):
                            raise Exception("Not enough arguements")
                        
                        for x in range(len(arg_name)):
                            v1 = self.eval(arg_val[x])
                            dictt[arg_name[x].name] = {"value":v1, "type": type(v1)}

                        self.environments.append(dictt)
                        m = self.eval(self.environments[src][name]["value"][1])
                        if(len(self.environments)>1):
                            self.environments.pop()
                        self.scope -= 1 
                        return(m)
                    else:
                            src -= 1 
                    
                raise Exception("Function is not defined")               
            
                
        raise InvalidProgramError(f"Runtime environment does not support program: {program}.")
