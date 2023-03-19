from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from utils.colors import GREEN, BOLD, RESET, RED, BLACK, YELLOW, BLUE, INVERSE, BRIGHT_INVERSE

class DeclarationError(Exception):
    """
    Raised when a variable is called but has not been defined before.
    """

    def __init__(self, name):
        self.name = name
        print(f"{RED}DeclarationError{RESET}: {name} is not declared.")


class InvalidProgramError(Exception):
    """
    Raised when a program is invalid.
    """

    def __init__(self, message, verbose=True):
        self.message = message
        print(f"{RED}InvalidProgramError{RESET}: {message}")


class EndOfStream(Exception):
    """
    Raised when the end of a stream is reached.
    """
    
    print(f"{RED}EndOfStreamError{RESET}: Reached End of Stream. Exiting...")


class EndOfTokens(Exception):
    """
    Raised when the end of a stream of tokens is reached.
    """
    print(f"{RED}EndOfTokensError{RESET}: Reached End of Tokens without resolving the expression.")


class TokenError(Exception):
    """
    Raised when the end of a stream of tokens is reached.
    """

    def __init__(self, message):
        self.message = message
        print(f"{RED}TokenError{RESET}: {message}")


class TypeCheckError(Exception):
    """
    Raised when the type of the operands in the operation are not of valid type
    """

    def __init__(self, oprtype=None, message: str = None):
        self.oprtype = str(oprtype)
        if not message:
            print(f"{RED}TypeError{RESET}: Operand(s) should have the type: {oprtype}.")
        else:
            print(f"{RED}TypeError{RESET}: {message}")


class InvalidConditionError(Exception):
    """
    Raised when an invalid condition is passed to a while loop
    """

    def __init__(self, cond):
        self.error = cond
        print(f"{RED}InvalidConditionError{RESET}: {cond} is not a valid condition.")


class VariableRedeclarationError(Exception):
    """
    Raised when a variable is redeclared in the same scope or a child scope.
    """

    def __init__(self, var):
        self.var = var
        print(
            f"{RED}RedeclarationError{RESET}: {var} has already been declared in the current scope."
        )


class AssignmentUsingNone(Exception):
    """
    Raised when a variable is assigned using a variable that has no assigned value itself.
    """

    def __init__(self, var):
        self.var = var
        print(f"{RED}AssignmentsUsingNoneError{RESET}: Trying to assign using {var} which has no assigned value itself.")


class InvalidConcatenationError(Exception):
    """
    Raised when a variable is assigned using a variable that has no assigned value itself.
    """

    def __init__(self):
        print(f"{RED}InvalidConcatenationError{RESET}: Invalid attempted concatenation of different operand types.")


class IndexOutOfBoundsError(Exception):
    """
    Raised when the index passed to a list is out of bounds.
    """

    def __init__(self, msg=None):
        if msg == None:
            print(msg)
        else:
            print(f"{RED}IndexOutOfBoundsError{RESET}: Slice index out of range.")


class InvalidOperation(Exception):
    def __init__(self, op, opr1, opr2=None):
        if opr2 == None:
            print(f"{RED}InvalidOperationError{RESET}: Cannot perform {op} on {opr1} objects.")

class InvalidArgumentToList(Exception):
    def __init__(self, list_type):
        print(f"{RED}InvalidArgumentToListError{RESET}: One or more inputs to list are not of type {list_type}.")


class ListError(Exception):
    def __init__(self, msg):
        print(f"{RED}ListError{RESET}: {msg}")


class ReferentialError(Exception):
    def __init__(self, var):
        print(f"{RED}ReferentialError{RESET}: The variable {var} referenced during assignment does not exist.")

class StringError(Exception):
    def __init__(self):
        print("Invalid value being assigned to string")

class ListOpError(Exception):
    def __init__(self,msg):
        print(msg)

class BadAssignment(Exception):
    def __init__(self, var, var_type, val_type):
        print(f"{RED}Assignment Error{RESET}: Trying to assign value of {val_type} to variable {var} of {var_type} type")
