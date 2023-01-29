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