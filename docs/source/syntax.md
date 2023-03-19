# Gossip Syntax

Gossip is a dynamically typed, interpreted programming language. This document specifies the syntax of the language. 

## General Syntax

All statements in gossip compulsorily end with a semicolon. Variables are dynamically typed, and typechecked with a typechecker. 

```python
declare a = 9;
print(a);

print(123812073);

assign a = 123;
print(a);

declare t = 5;
print(let r = 100 in let t = 10 in r + t ; ;);
```

We recommend writing Gossip code as closely as possible to `python`'s PEP-8 standards; explicitly, we recommend spaces between operators and operands, declaring variables near the top of the codebase, and separating semicolons in the middle of a line with a whitespace.

## Data Types

Gossip has a number of built-in data types: NumLiterals, Booleans, StringLiterals, and Lists.

### Numbers

Numbers in Gossip can be integers or floating-point numbers. They can be written in decimal notation. Here are some examples:

```python
10
3.14
```

In Gossip, all numbers are inherently handled as Fractions, so 2.5 is actually the simplified fraction 5/2, and is calculated as such.

### Booleans

Booleans in Gossip are `True` and `False`, and can arise both explicitly or as the result of a boolean operation.

## Variables

Variables in Gossip are dynamically typed, which means that they can be assigned values of any type. A variable is declared using the `declare` keyword. Here is an example:
    
```python
declare x = 10;
```

Once declared, a variable cannot be re-declared in the same or a child scope. Forward declarations are not allowed, and changing values requires the `assign` flag.

```python
assign x = 20;
```

## Strings

Strings are defined the same way as numbers, and are written exclusively with single quotes ('). 

```python
declare x = 'Hello World!'
assign x = x+x 
print(x)
```

This prints out `HelloWorld!HelloWorld!`, as is expected. Strings cannot be operated upon with numbers.

## Operators

Gossip has several built-in operators.

### Arithmetic Operators

Gossip has the following arithmetic operators:

```
+ - * ** / %  
```


Here is an example:

```
10 + 5 * 2
```

The `+` operator is overloaded to also work on Strings, where it handles concatenation.

### Comparison Operators

Gossip has the following comparison operators:

```
< > <= >= == !=
```

Here is an example:

```
10 < 20
```

These return a boolean value, that can be used to evaluate an If-Else construct.

### Logical Operators

Gossip has the following logical operators:

```
and or not
```


Here is an example:

```python
a > b and a < 2*b
```

### Assignment Operators

Gossip has two assignment operators:

```
declare assign
```

Here is an example:

```
declare x = 10;
assign x = 20;
```

## Control Flow

Gossip has the following control flow statements.

### If Statements

An if statement in Gossip looks like this:

```
if a < b then{
x = 10;
} else {
x = 20;
};
```

### While Loops

A while loop in Gossip looks like this:

```
while x < 10 do {
x = x + 1;
};
```

### For Loops

A for loop in Gossip looks like this:

```
for i in range 1 to 10; do {
print(i);
};
```

### Repeat Loops

A repeat loop in Gossip looks like this:

```
repeat{
x = x + 1;
} until x == 10;
```
### Print Statements

A print statement in Gossip looks like this:

```
print('Hello, world!')
```
