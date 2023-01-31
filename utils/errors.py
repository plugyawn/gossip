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

class InvalidCondition(Exception):

    """
    raised when an invalid condition is passed to a while loop
    """

    def __init__(self,cond):
        self.error = cond
        print(f"Invalid Condition: {cond} is not a valid condition.")
        