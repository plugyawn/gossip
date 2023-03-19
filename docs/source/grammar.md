# Grammar

The grammar page provides a detailed description of the Gossip-lang grammar, including information on the different types of expressions, statements, and literals used in the language.

```{code-block} ruby

program: statement*

statement:
    | "let" identifier "=" expression
    | "assign" identifier "=" expression
    | "print" expression
    | compound_statement
    | if_statement
    | while_statement
    | repeat_statement
    | "declare" variable_declaration+ "in" statement "end"

compound_statement:
    | "for" identifier "in" range "do" statement "end"
    | "for" identifier "," identifier "in" matrix_range "do" statement "end"
    | "with" expression "as" identifier "do" statement "end"

if_statement:
    | "if" expression "then" statement "else" statement "end"
    | "if" expression "then" statement "end"

while_statement:
    | "while" expression "do" statement "end"

repeat_statement:
    | "repeat" statement "until" expression

variable_declaration:
    | identifier ("," identifier)*

range:
    | expression "to" expression

matrix_range:
    | range "by" expression "," expression "to" expression

expression:
    | comparison (("and" | "or") comparison)*

comparison:
    | term ((">" | "<" | ">=" | "<=" | "==" | "!=") term)*

term:
    | factor (("+" | "-") factor)*

factor:
    | power (("*" | "/" | "quot" | "rem") power)*

power:
    | call ("**" power)?

call:
    | atom ("(" call_arguments ")")?

call_arguments:
    | expression ("," expression)*

atom:
    | "True" | "False"
    | identifier
    | number
    | string
    | "(" expression ")"

identifier:
    | /[a-zA-Z_][a-zA-Z0-9_]*/

number:
    | /[0-9]+(\.[0-9]+)?/

string:
    | /"(\\.|[^"])*"/
```