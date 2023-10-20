# flake8-multiline-function-call-equals

A (higly opinonated) flake8 extension that checks for spaces around `=` in multiline function calls

## Motivation

For improved readability, function calls that span multiple physical lines should have a single space on either side of the `=` when using named arguments. Additionally, each physical line may hve exatly one argument (named, or otherwise).

By contrast, there should be no spaces around the `=`, when a function with named arguments is called on one physical line (i.e. not a multiline function call)

## Examples

### EQA100

```
foo(a = 5, b = 2)
```

This is a single line function call with named arguments. In this case, there should be no spaces around the `=` when passing values to the named arguments. The correct call would be

```
foo(a=5, b=2)
```

### EQA101

```
foo(a  = 5,  # incorrect
    b = 2,  # correct
    )
```

This is a multiline function call with named arguments. In this case, there should be a single space on each side of the `=` when passing values to the named arguments. The correct call would be

```
foo(a = 5,
    b = 2,
    )
```

### EQA102

```
foo(a= 5,  # incorrect - no space on the left
    b = 2,  # correct
    )
```

```
foo(a=5,  # incorrect - no spaces at all
    b = 2,  # correct
    )
```

These are multiline function calls with named arguments. In these cases, there should be a single space on each side of the `=` when passing values to the named arguments. The correct call would be

```
foo(a = 5,
    b = 2,
    )
```

### EQA103

```
foo(a = 5,
           # incorrect - there should be no empty line here
    b = 2,
    )
```

```
foo(a = 5,
    b = 2,
           # incorrect - there should be no empty line here
    )
```

These are multiline function calls with named arguments. In these cases, there should be no empty lines within the function call. The correct call would be

```
foo(a = 5,
    b = 2,
    )
```


### EQA104

```
foo(a = 5, b = 2,  # incorrect - only one argument per line
    )
```

```
foo(3, 4,  # incorrect - only one argument per line
    a = 5,
    b = 2,
    )
```


These are multiline function calls. In these cases, only one argument may be listed per line. The correct calls would be

```
foo(a = 5,
    b = 2,  # incorrect - only one argument per line
    )
```

```
foo(3,
    4,  # incorrect - only one argument per line
    a = 5,
    b = 2,
    )
```

### EQA105

```
foo(  # incorrect - the first argument should be on this line
    a = 5,
    b = 2,
    )
```

This is a multiline function call. In this case, the first argument should be on the line with the open paren. The correct call would be

```
foo(a = 5,
    b = 2,
    )
```

### EQA106

```
foo(a = 5,
    b = 2,)  # incorrect - closing paren should be on a separate line
```


This is a multiline function call. In this case, the closing parenthesis should be on its own line. The correct call would be

```
foo(a = 5,
    b = 2,
    )
```

## List of Error Codes

| Code          | Description   |
|:-------------:|:--------------|
| EQA100      | Too many whitespaces surrounding assignment operator in single-line function call |
| EQA101      | Too many whitespaces surrounding assignment operator in multiline function call |
| EQA102      | Too few whitespaces surrounding assignment operator in multiline function call |
| EQA103      | Empty line in multiline function call |
| EQA104      | Multiple arguments on the same line in multiline function call |
| EQA105      | First argument does not start on the call line in multiline function call |
| EQA106      | Closing paren is on the same line as the last argument |


## Limitations

Python's AST parser does not mention the position of the `=` in argument passing. Consequently, the following code block will pass linting, even though it violates the spirit of the rule this linter attempts to enforce

```
foo(a=  5,  # this will incorrectly pass the lint check
    b = 2,
    )
```
