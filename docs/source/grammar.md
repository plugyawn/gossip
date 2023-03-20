# Grammar

The grammar page provides a detailed description of the Gossip-lang grammar, including information on the different types of expressions, statements, and literals used in the language.

```{code-block} ruby

program: expression*

expression:
    | "let" atomic_expression "=" expression "in" expression ";"
    | "assign" atomic_expression "=" expression ";"
    | "print(" expression ");"
    | "range" "(" atomic_expression "," atomic_expression ")"
    | "if" expression "then" expression
    | "if" expression "then" expression "else" expression ";"
    | "while" expression "do" expression ";"
    | "for" atomic_expression "in" expression "do" expression ";"
    | "declare" atomic_expression "=" expression ";"
    | "repeat" expression "while" expression ";"
    | "deffunct" atomic_expression "("  (atomic_expression,",")*  ")"  AST_sequence ";"
    | "callfun" atomic_expression "("  (expression, ",")*  ")" ";"
    | "functret" "(" expression ")" ";"
    | "'" atomic_expression "'"
    | "[" (expression, ",")* "]"
    | simple_expression

AST_sequence:
    | "{" expression* "}"
    
simple_expression:
    | comparison_expression
    | comparison_expression "&&" comparison_expression
    | comparison_expression "||" comparison_expression
    

comparison_expression:
    | addition_expression
    | addition_expression "+ - * ** / < > <= >= == != = % & && || | !"  addition_expression


addition_expression:
    | multiplication_expression
    | multiplication_expression   ("+-", multiplication_expression)*


multiplication_expression:
    | modulo_expression
    | modulo_expression ("*/", modulo_expression)*


modulo_expression:
    | uneg_expression
    | uneg_expression ("%", uneg_expression)*


uneg_expression:
    | "-" atomic_expression
    | atomic_expression

atomic_expression:
    | Identifier "." list_op
    | Identifier "[" slice "]"
    | Number
    | Bool

list_op:
    | head
    | tail
    | empty
    | cons "(" expression ")"

slice:
    | expression
    | expression "," expression
   
Identifier:
    | /[a-zA-Z_][a-zA-Z0-9_]*/

Number:
    | /[0-9]+(\.[0-9]+)?/

Bool:
    | True
    | False
```
