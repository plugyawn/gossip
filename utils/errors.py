from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping

class DefinitionError(Exception):
    """
    Raised when a variable is called but has not been defined before.
    """

    def __init__(self, name):
        self.name = name
        print(f"DefinitionError: {name} is not defined.")

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
