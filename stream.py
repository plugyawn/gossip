from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType
from utils.errors import EndOfStream, EndOfTokens, TokenError
from utils.datatypes import Num, Bool, Keyword, Identifier, Operator, NumLiteral, BinOp, Variable, Let, If, BoolLiteral, UnOp, ASTSequence, AST, Buffer

keywords = "let if then else in end".split()
symbolic_operators = "+ - * ** / < > <= >= == != =".split()
word_operators = "and or not quot rem".split()
whitespace = " \t\n"
symbols = ", ; ( )".split()

@dataclass
class Stream:
    source: str
    pos: int

    def from_string(string:str , position:int = 0):
        """
        Creates a stream from a string. Position reset to 0.
        """
        return Stream(string, position)

    def next_char(self):
        """
        Returns the next character in the stream.
        """
        if self.pos >= len(self.source):
            raise EndOfStream()
        self.pos = self.pos + 1
        return self.source[self.pos - 1]

    def unget(self):
        """
        Moves the stream back one character.
        """
        assert self.pos > 0
        self.pos = self.pos - 1

# Define the token types.
Token = Num | Bool | Keyword | Identifier | Operator

def word_to_token(word):
    if word in keywords:
        return Keyword(word)
    if word in word_operators:
        return Operator(word)
    if word == "True":
        return Bool(True)
    if word == "False":
        return Bool(False)
    if word in symbolic_operators:
        return Operator(word)
    return Identifier(word)

@dataclass
class Lexer:
    stream: Stream
    save: Token = None

    def from_stream(s):
        return Lexer(s)
        
    def next_token(self) -> Token:
        try:
            match self.stream.next_char():
                case c if c.isdigit():
                    # TODO: Handle different bases.
                    n = int(c)  
                    base_multiplier = 10
                    floating = False
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isdigit() and not floating:
                                n = n*base_multiplier + int(c)
                            elif c.isdigit() and floating:
                                n = n + int(c) / base_multiplier
                                base_multiplier = base_multiplier * 10
                            elif c == ".":          
                                if floating:
                                    raise Exception("Cannot have two decimal points in a number.")
                                floating = floating | True
                            else:
                                self.stream.unget()
                                return Num(n, floating= floating)
                        except EndOfStream:
                            return Num(n)

                case c if c in symbolic_operators: 
                     s = c
                     while True:
                        try:
                            c = self.stream.next_char()
                            if c in symbolic_operators:
                                s = s + c
                            else:
                                self.stream.unget()
                                return word_to_token(s)
                        except EndOfStream:
                            return word_to_token(s)

                case c if c.isalpha():
                    s = c
                    while True:
                        try:
                            c = self.stream.next_char()
                            if c.isalpha():
                                s = s + c
                            else:
                                self.stream.unget()
                                return word_to_token(s)
                        except EndOfStream:
                            return word_to_token(s)
                case c if c in whitespace:
                    return self.next_token()
        except EndOfStream:
            raise EndOfTokens

    def peek_token(self):
        """
        Peeks at the next token, but doesn't advance the stream.
        """
        if self.save is not None:
            return self.save
        self.save = self.next_token()
        return self.save

    def match(self, expected):
        """
        Matches the next token to the expected token.
        """
        if self.peek_token() == expected:
            return self.advance()
        raise TokenError()

    def advance(self):
        """
        Advances the stream by one token.
        """
        assert self.save is not None
        self.save = None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.curr_token = self.next_token()
            return self.curr_token
        except EndOfTokens:
            raise StopIteration

@dataclass
class Parser:
    lexer: Lexer

    def from_lexer(lexer):
        """
        Generate a parser from a lexer.
        """
        return Parser(lexer)

    def parse_expression(self):
        """
        Parse a complete expression.
        For | a == b |, this will parse the entire expression.
        """
        match self.lexer.peek_token():
            case Keyword("if"):
                return self.parse_if()
            case Keyword("while"):
                return self.parse_while()
            case Keyword("let"):
                return self.parse_let()
            case Keyword("end"):
                return self.lexer.__next__()
            case _:
                return self.parse_simple()

    def parse_atomic_expression(self):
        """
        Parse an atomic expression.
        For | a == b |, this will parse | a |.
        """
        match self.lexer.peek_token():
            case Identifier(name):
                self.lexer.advance()
                return Variable(name)
            case Num(value):
                self.lexer.advance()
                return NumLiteral(value)
            case Bool(value):
                self.lexer.advance()
                return BoolLiteral(value)

    def parse_addition(self):
        """
        Parse an addition expression.
        For | a + b |, this will parse the entire expression.
        """
        left = self.parse_multiplication()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in "+-":
                    self.lexer.advance()
                    m = self.parse_multiplication()
                    left = BinOp(op, left, m)
                case _:
                    break
        return left

    def parse_multiplication(self):
        """
        Parse a multiplication expression.
        For | a * b |, this will parse the entire expression.
        """
        left = self.parse_atomic_expression()
        while True:
            match self.lexer.peek_token():
                case Operator(op) if op in "*/":
                    self.lexer.advance()
                    m = self.parse_atomic_expression()
                    left = BinOp(op, left, m)
                case _:
                    break
        return left

    def parse_simple(self):
        """
        Parse a simple expression. 
        # TODO - This is a bit of a misnomer, as it just calls parse_comparison().
        """
        return self.parse_comparison()

    def parse_comparison(self):
        """
        Parse a comparison expression.
        For | a == b |, this will parse the entire expression.
        """
        left = self.parse_addition()
        match self.lexer.peek_token():
            case Operator(op) if op in symbolic_operators:
                self.lexer.advance()
                right = self.parse_addition()
                return BinOp(op, left, right)
        return left

    def parse_let(self):
        """
        Parse a let function. 
        Examples: | let a  = 6 end |, to define a.
                  | let a  = 6 in a + 1 end |, to define a and use it in an expression.
        """
        self.lexer.match(Keyword("let"))
        var = self.parse_atomic_expression()
        self.lexer.match(Operator("="))
        a = self.parse_atomic_expression()
        try:
            self.lexer.match(Keyword("in"))
            b = self.parse_atomic_expression()
        except TokenError:
            self.lexer.match(Keyword("end"))
            return Let(var, a)
        self.lexer.match(Keyword("end"))
        return Let(var, a, b)

    def parse_if(self):
        """
        Parse an if function.
        Examples: | if a == b then a+2 else a+1 end |, to define a and use it in an expression.
        """
        self.lexer.match(Keyword("if"))
        cond = self.parse_expression()
        self.lexer.match(Keyword("then"))
        e1 = self.parse_expression()
        self.lexer.match(Keyword("else"))
        e2 = self.parse_expression()
        self.lexer.match(Keyword("end"))
        return If(cond, e1, e2)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            return self.parse_expression()
        except EndOfTokens:
            raise StopIteration