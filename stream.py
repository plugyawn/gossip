from fractions import Fraction
from dataclasses import dataclass
from typing import Optional, NewType
from utils.errors import EndOfStream, EndOfTokens, TokenError
from utils.datatypes import Num, Bool, Keyword, Symbols, Identifier, Whitespace, Operator, NumLiteral, BinOp, Variable, Let, Assign, If, BoolLiteral, UnOp, ASTSequence, AST, Buffer, ForLoop, Range, Declare, While, DoWhile, Print
from core import RuntimeEnvironment


keywords = "let assign for while repeat print declare range do to if then else in  ".split()
symbolic_operators = "+ - * ** / < > <= >= == != =".split()
word_operators = "and or not quot rem".split()
whitespace = [" ", "\n"]
symbols = "; , ( ) { } [ ] ".split()


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
Token = Num | Bool | Keyword | Identifier | Operator | Symbols | Whitespace

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
    if word in symbols:
        return Symbols(word)
    if word in whitespace:
        return Whitespace(word)
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

                case c if c in symbols: 
                    s = c
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
            case Keyword("assign"):
                return self.parse_assign()
            case Keyword("for"):
                return self.parse_for()
            case Keyword("range"):
                return self.parse_range()
            case Keyword("print"):
                return self.parse_print()
            case Keyword("declare"):
                return self.parse_declare()
            case Keyword("while"):
                return self.parse_while()
            case Keyword("repeat"):
                return self.parse_repeat()
            case Symbols(";"):
                return self.lexer.__next__()
            case Symbols("{"):
                return self.parse_AST_sequence()
            case Symbols("}"):
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
        a = self.parse_expression()
        self.lexer.match(Keyword("in"))
        b = self.parse_expression()
        self.lexer.match(Symbols(";"))
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
        if self.lexer.peek_token() != Keyword("else"):
            return If(cond, e1, None)
        self.lexer.match(Keyword("else"))
        e2 = self.parse_expression()
        return If(cond, e1, e2)

    def parse_assign(self):
        """
        Parse an assignment.
        Examples: | a = 6 |, to assign 6 to a.
        """
        self.lexer.match(Keyword("assign"))
        var = self.parse_atomic_expression()
        self.lexer.match(Operator("="))
        a = self.parse_expression()
        self.lexer.match(Symbols(";"))
        return Assign(var, a)

    def parse_for(self):
        """
        Parse a for loop.
        Examples: | for a = 1 in 10 do a + 1 end |, to define a and use it in an expression.
        """
        self.lexer.match(Keyword("for"))
        var = self.parse_atomic_expression()
        self.lexer.match(Keyword("in"))
        iter = self.parse_expression()
        self.lexer.match(Keyword("do"))

        task = self.parse_expression()

        self.lexer.match(Symbols(";"))

        return ForLoop(var, iter, task)

    def parse_range(self):
        """
        Parse a range.
        Examples: | range 1 to 10 |, to define a range from 1 to 10.
        """
        self.lexer.match(Keyword("range"))
        self.lexer.match(Symbols("("))
        left = self.parse_atomic_expression()
        self.lexer.match(Symbols(","))
        right = self.parse_atomic_expression()
        self.lexer.match(Symbols(")"))
        return Range(left, right)

    def parse_print(self):
        """
        Parse a print statement.
        Examples: | print a |, to print the value of a.
        """
        self.lexer.match(Keyword("print"))
        self.lexer.match(Symbols("("))
        expression = self.parse_expression()
        self.lexer.match(Symbols(")"))
        self.lexer.match(Symbols(";"))
        return Print(expression)

    def parse_while(self):
        """
        Parse a while loop.
        Examples: | while a == b do a + 1 end |, to define a and use it in an expression.
        """
        self.lexer.match(Keyword("while"))
        cond = self.parse_expression()
        self.lexer.match(Keyword("do"))
        task = self.parse_expression()
        self.lexer.match(Symbols(";"))
        return While(cond, task)

    def parse_repeat(self):
        """
        Parse a repeat loop.
        Examples: | repeat a + 1 until a == b |, to define a and use it in an expression.
        """
        self.lexer.match(Keyword("repeat"))
        task = self.parse_expression()
        self.lexer.match(Keyword("while"))
        cond = self.parse_expression()
        self.lexer.match(Symbols(";"))
        return DoWhile(task, cond)

    def parse_declare(self):
        """
        Parse a declaration.
        Examples: | declare a = 10 |, to declare a."""
        self.lexer.match(Keyword("declare"))
        var = self.parse_atomic_expression()
        self.lexer.match(Operator("="))
        a = self.parse_expression()
        self.lexer.match(Symbols(";"))
        return Declare(var, a)
    
    def parse_AST_sequence(self):
        li = []
        self.lexer.match(Symbols("{"))
        while self.lexer.peek_token() != Symbols("}"):    
            var = self.parse_expression()
            li.append(var)
        self.lexer.match(Symbols("}"))
        return ASTSequence(li)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            return self.parse_expression()
        except EndOfTokens:
            raise StopIteration
