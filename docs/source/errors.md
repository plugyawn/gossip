# Errors And Exceptions

Gossip-lang comes with custom errors to help you debug your code. This page provides details on each of the custom errors that can be raised when using Gossip-lang.

## DeclarationError

Raised when a variable is called but has not been defined before.

```python
class DeclarationError(Exception):
    def __init__(self, name):
        self.name = name
        print(f"DeclarationError: {name} is not declared.")
```

## InvalidProgramError

Raised when a program is invalid.

```python
class InvalidProgramError(Exception):
    def __init__(self, message, verbose=True):
        self.message = message
        print(f"InvalidProgramError: {message}")
```

## EndOfStream

Raised when the end of a stream is reached.

```python
class EndOfStream(Exception):
    pass
```

## EndOfTokens

Raised when the end of a stream of tokens is reached.

```python
class EndOfTokens(Exception):
    pass
```

## TokenError

Raised when an invalid token is encountered.

```python
class TokenError(Exception):
    pass
```

## TypeCheckError

Raised when the type of the operands in the operation are not of valid type.

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
class InvalidCondition(Exception):
    def __init__(self, cond):
        self.error = cond
        print(f"Invalid Condition: {cond} is not a valid condition.")
```

## VariableRedeclaration

Raised when a variable is re-declared in the same scope.

```python
class VariableRedeclaration(Exception):
    def __init__(self, var):
        self.var = var
        print(f"Redeclaration Error: {var} has already been declared in the current scope.")
```


## AssignmentUsingNone

Raised when trying to assign using a variable that has no assigned value itself.

```python
class AssignmentUsingNone(Exception):
    def __init__(self, var):
        self.var = var
        print(f"Trying to assign using {var} which has no assigned value itself.")
```

Refer to the [syntax](syntax.md) for more information on how to avoid these errors.