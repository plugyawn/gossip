from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping

class DeclarationError(Exception):
    """
    Raised when a variable is called but has not been defined before.
    """

    def __init__(self, name):
        self.name = name
        print(f"DeclarationError: {name} is not declared.")

class InvalidProgramError(Exception):
    """
    Raised when a program is invalid.
    """
    def __init__(self, message, verbose = True):
        self.message = message
        print(f"InvalidProgramError: {message}")
class EndOfStream(Exception):
    """
    Raised when the end of a stream is reached.
    """
    pass

class EndOfTokens(Exception):
    """
    Raised when the end of a stream of tokens is reached.
    """
    pass

class TokenError(Exception):
    """
    Raised when the end of a stream of tokens is reached.
    """
    pass


class TypeCheckError(Exception):
    """
    Raised when the type of the operands in the operation are not of valid type
    """

    def __init__(self, oprtype = None, message:str = None):
        self.oprtype = str(oprtype)
        if not message:
            print(f"TypeError: Operand(s) should have the type: {oprtype}.")
        else:
            print(f"TypeError: {message}")

            
            
class InvalidCondition(Exception):

    """
    raised when an invalid condition is passed to a while loop
    """

    def __init__(self,cond):
        self.error = cond
        print(f"Invalid Condition: {cond} is not a valid condition.")   

        
        
class VariableRedeclaration(Exception):

    def __init__(self,var):
        self.var = var
        print(f"Redeclaration Error: {var} has already been declared in the current scope.")
     
    
    
class AssignmentUsingNone(Exception):

    def __init__(self,var):
        self.var = var
        print(f"Trying to assign using {var} which has no assigned value itself.")

class InvalidFileExtensionError(Exception):
    """
    Raised when the file extension is not valid.
    """
    def __init__(self, ext):
        print(f"InvalidFileExtension: {ext} is not a valid file extension for gossip language.")