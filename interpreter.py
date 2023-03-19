from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from core import RuntimeEnvironment
from utils.datatypes import (
    AST,
    NumLiteral,
    BinOp,
    Variable,
    Value,
    Let,
    If,
    BoolLiteral,
    UnOp,
    ASTSequence,
    Declare,
)
from utils.visualizer import ASTViz
from stream import Stream, Lexer, Parser

color_codes = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
    "bright_black": "90",
    "bright_red": "91",
    "bright_green": "92",
    "bright_yellow": "93",
    "bright_blue": "94",
    "bright_magenta": "95",
    "bright_cyan": "96",
    "bright_white": "97",
}

bold_color_codes = {f"bright_{k}": f"{v};1" for k, v in color_codes.items()}
color_codes.update(bold_color_codes)

special_codes = {
    "reset": "0",
    "bold": "1",
    "inverse": "7",
    "bright_inverse": "7;1",
}

color_codes.update(special_codes)

# Useful dictionary with color codes for easy access.
COLORMAP = {k: f"\x1b[{v}m" for k, v in color_codes.items()}

# Some commonly used colours for easier access.
BLACK = COLORMAP["black"]
RED = COLORMAP["red"]
GREEN = COLORMAP["green"]
YELLOW = COLORMAP["yellow"]
BLUE = COLORMAP["blue"]
RESET = COLORMAP["reset"]

# Some commonly used styles for easier access.
BOLD = COLORMAP["bold"]
INVERSE = COLORMAP["inverse"]
BRIGHT_INVERSE = COLORMAP["bright_inverse"]


def interpret(feedback=False, visualize=False):
    runtime = RuntimeEnvironment()
    persist = False

    while True:

        if not persist:
            line = input(f"{GREEN}{BOLD}gossip{RESET} >>> ")
        else:
            line += input(f"{GREEN}{BOLD}gossip{RESET} ... ... ")

        if line == "exit":
            break

        persist = True if line[-1] == "{" else False if line[-2:] == "};" else persist

        L = Lexer.from_stream(Stream.from_string(line))
        S = Parser.from_lexer(L)

        for s in S:
            if visualize:
                vis = ASTViz(depth=0, code=line)
                vis.treebuilder(s)
            if feedback:
                print(f"{RED}{runtime.eval(s)}{RESET}")
            else:
                if not persist:
                    runtime.eval(s)
