from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
import os

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
from utils.colors import GREEN, BOLD, RESET, RED, BLACK, YELLOW, BLUE, INVERSE, BRIGHT_INVERSE

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
        if line == "clear":
            os.system("clear")
            continue
        if line == "":
            continue

        persist = True if line[-1] == "{" else False if line[-2:] == "};" else persist

        L = Lexer.from_stream(Stream.from_string(line))
        S = Parser.from_lexer(L)

        for s in S:
            try:
                if visualize:
                    vis = ASTViz(depth=0, code=line)
                    vis.treebuilder(s)
                if feedback:
                    if not persist:
                        print(f"{RED}{runtime.eval(s)}{RESET}")
                else:
                    if not persist:
                            runtime.eval(s)
            except:
                continue
