# Gossip Syntax

Gossip is a dynamically typed, interpreted programming language. This document specifies the syntax of the language.

## Data Types

Gossip has two built-in data types: numbers and booleans.

### Numbers

Numbers in Gossip can be integers or floating-point numbers. They can be written in decimal notation. Here are some examples:

```python
10
3.14
```

### Booleans

Booleans in Gossip are `True` and `False`.

## Variables

Variables in Gossip are dynamically typed, which means that they can be assigned values of any type. A variable is declared using the `let` keyword. Here is an example:
    
```python
let x = 10
```

## Operators

Gossip has several built-in operators.

### Arithmetic Operators

Gossip has the following arithmetic operators:

```
+ - * ** / rem quot  
```


Here is an example:

```
10 + 5 * 2
```

### Comparison Operators

Gossip has the following comparison operators:

```
< > <= >= == !=
```

Here is an example:

```
10 < 20
```

### Logical Operators

Gossip has the following logical operators:

```
and or not
```


Here is an example:

```
True and False
```

### Assignment Operators

Gossip has two assignment operators:

```
let assign
```

Here is an example:

```
let x = 10
x assign 20
```

## Control Flow

Gossip has the following control flow statements.

### If Statements

An if statement in Gossip looks like this:

```
if a < b then
x = 10
else
x = 20
end
```

### While Loops

A while loop in Gossip looks like this:

```
while x < 10 do
x = x + 1
end
```

### For Loops

A for loop in Gossip looks like this:

```
for i in 1 to 10 do
print i
end
```

### Repeat Loops

A repeat loop in Gossip looks like this:

```
repeat
x = x + 1
until x == 10
```
### Print Statements

A print statement in Gossip looks like this:

```
print "Hello, world!"
```
