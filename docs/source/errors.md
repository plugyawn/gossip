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
## InvalidTokenError

Raised when an invalid token is encountered.

For example,
```
```

```python
class InvalidTokenError(Exception):
    """
    Raised when an invalid token is encountered.
    """

    def __init__(self, token, verbose=True):
        self.token = token
        print(f"{RED}InvalidTokenError{RESET}: {token} is not a valid token.")
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

## InvalidConcatenationError

Raised when a variable is assigned using a variable that has no assigned value itself.

```python
class InvalidConcatenationError(Exception):
    def __init__(self):
        print(f"{RED}InvalidConcatenationError{RESET}: Invalid attempted concatenation of different operand types.")
```

## IndexOutOfBoundsError

Raised when the index passed to a list is out of bounds.

```python
class IndexOutOfBoundsError(Exception):
    def __init__(self, msg=None):
        if msg == None:
            print(msg)
        else:
            print(f"{RED}IndexOutOfBoundsError{RESET}: Slice index out of range.")
```

## InvalidOperation

Raised when an invalid operation is performed on an object.

```python
class InvalidOperation(Exception):
    def __init__(self, op, opr1, opr2=None):
        if opr2 == None:
            print(f"{RED}InvalidOperationError{RESET}: Cannot perform {op} on {opr1} objects.")
```

## InvalidArgumentToList

Raised when one or more arguments passed to the `list` construct are not of the same type.

```python
class InvalidArgumentToList(Exception):
    def __init__(self, list_type):
        print(f"{RED}InvalidArgumentToListError{RESET}: One or more inputs to list are not of type {list_type}.")
```

## ListError

Raised if any errors occur when using the `list` construct.

```python
class ListError(Exception):
    def __init__(self, msg):
        print(f"{RED}ListError{RESET}: {msg}")
```

## ReferentialError

Raised when a variable is referenced during assignment but has not been declared before.

```python
class ReferentialError(Exception):
    def __init__(self, var):
        print(f"{RED}ReferentialError{RESET}: The variable {var} referenced during assignment does not exist.")
```

## BadAssignment

Raised when a variable is assigned a value of a different type.

```python
class BadAssignment(Exception):
    def __init__(self,var,var_type,val_type):
        print(f"Assignment Error- Trying to assign value of {val_type} to variable {var} of {var_type} type")
```

## StringError

Raised when a string is assigned a value of a different type.

```python
class StringError(Exception):
    def __init__(self):
        print("Invalid value being assigned to string")
```

## ListOpError

Raised when an invalid operation is performed on a list.

```python
class ListOpError(Exception):
    def __init__(self,msg):
        print(msg)
```

## InvalidFileExtensionError

Raised when the file extension is not valid.

```python
class InvalidFileExtensionError(Exception):
    def __init__(self, ext):
        print(f"InvalidFileExtension: {ext} is not a valid file extension for gossip language.")
```
Refer to the [syntax](syntax.md) for more information on how to avoid these errors.