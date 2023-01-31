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

    def __init__(self, program):
        self.program = program
        print(f"InvalidProgramError: Runtime environment does not support program: {program}.")

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