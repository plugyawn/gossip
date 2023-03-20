# Errors And Exceptions

Gossip-lang comes with custom errors to help you debug your code. This page provides details on each of the custom errors that can be raised when using Gossip-lang.

## DeclarationError

Raised when a variable is called but has not been defined before. For example,

```python
declare a = 10;
assign a = a * b;
```
When `b` hasn't been declared.

```python
class DeclarationError(Exception):
    def __init__(self, name):
        self.name = name
        print(f"DeclarationError: {name} is not declared.")
```

## InvalidProgramError

Raised when a program is invalid.

For example,

```
declare;
```
Without any other attributes, the declare flag fails.

```python
class InvalidProgramError(Exception):
    def __init__(self, message, verbose=True):
        self.message = message
        print(f"InvalidProgramError: {message}")
```

## EndOfStream

Raised when the end of a stream is reached without any resolution.

For example,
```
for i in range
```
Without any further code, this hanging ForLoop construct is meaningless.

```python
class EndOfStream(Exception):
    pass
```

## EndOfTokens

Raised when the end of a stream of tokens is reached. This is similar to `EndOfStreams` and often occurs together.

```python
class EndOfTokens(Exception):
    pass
```

## TokenError

Raised when an invalid token is encountered. 
```
declare a ~ 40;
```

In the March, 2023 version of Gossip, the tilde (`~`) is meaningless.

```python
class TokenError(Exception):
    pass
```

## TypeCheckError

Raised when the type of the operands in the operation are not of valid type.

```python
declare sample = True * False
```

```python
class TypeCheckError(Exception):
    def __init__(self, oprtype=None, message=None):
        self.oprtype = str(oprtype)
        if not message:
            print(f"TypeError: Operand(s) should have the type: {oprtype}.")
        else:
            print(f"TypeError: {message}")
```

## InvalidCondition

Raised when an invalid condition is passed to a while loop.
```python
while a + 2 do {
    print(a);
};
```

```python
class InvalidCondition(Exception):
    def __init__(self, cond):
        self.error = cond
        print(f"Invalid Condition: {cond} is not a valid condition.")
```

## VariableRedeclaration

Raised when a variable is re-declared in the same or a child scope.

```python
declare a = 20;
declare a = 10;
```

In such a case, one should employ the `assign` construct.

```python
class VariableRedeclaration(Exception):
    def __init__(self, var):
        self.var = var
        print(f"Redeclaration Error: {var} has already been declared in the current scope.")
```


## AssignmentUsingNone

Raised when trying to assign using a variable that has no assigned value itself.
```
assign a = 20;
```
When `a` has not been declared before.

```python
class AssignmentUsingNone(Exception):
    def __init__(self, var):
        self.var = var
        print(f"Trying to assign using {var} which has no assigned value itself.")
```

Refer to the [syntax](syntax.md) for more information on how to avoid these errors.