from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
import os

from bytecode import *

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
from utils.errors import InvalidTokenError, TokenError

def interpret(feedback=False, visualize=False):
    runtime = RuntimeEnvironment()
    persist = False

    while True:
        try:
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
            L_ = Lexer.from_stream(Stream.from_string(line))
            S = Parser.from_lexer(L)
            S_ = Parser.from_lexer(L_)

            assert len([s for s in S_]) != 0 or persist
        except (AssertionError, TokenError, ) as e:
            print(f"{RED}InvalidTokenError{RESET}: Invalid token encountered.")
            pass
        try:
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
        except Exception as e:
            print(e)

def compile_gossip(lines):
    runtime = RuntimeEnvironment()
    
    L = Lexer.from_stream(Stream.from_string(lines))
    S = Parser.from_lexer(L)

    #for bytecode
    vm = VM()
    f = 1

    for s in S:

        ##for eval
        r = runtime.eval(s)


        #for bytecode
        # codegen(s,f,vm.get_bytecode())
        f=0
    
    #for bytecode
    vm.execute()

        
            
