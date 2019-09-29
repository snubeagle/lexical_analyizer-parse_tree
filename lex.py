# CS3210 - Principles of Programming Languages - Fall 2019
# A Lexical Analyzer for an expression
#Tanner Madsen and Ryan McCullough

from enum import Enum
import sys

# all char classes
class CharClass(Enum):
    EOF        = 1
    LETTER     = 2
    DIGIT      = 3
    OPERATOR   = 4
    PUNCTUATOR = 5
    QUOTE      = 6
    BLANK      = 7
    OTHER      = 8

# reads the next char from input and returns its class
def getChar(input):
    if len(input) == 0:
        return (None, CharClass.EOF)
    c = input[0].lower()
    if c.isalpha():
        return (c, CharClass.LETTER)
    if c.isdigit():
        return (c, CharClass.DIGIT)
    if c == '"':
        return (c, CharClass.QUOTE)
    if c in ['+', '-', '*', '/', '>', '=', '<']:
        return (c, CharClass.OPERATOR)
    if c in ['.', ':', ',', ';']:
        return (c, CharClass.PUNCTUATOR)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    return (c, CharClass.OTHER)

# calls getChar and getChar until it returns a non-blank
def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

# all tokens
class Token(Enum):
    ADDITION   = 1
    ASSIGNMENT = 2
    BEGIN      = 3
    BOOLEAN_TYPE = 4
    COLON      = 5
    DO         = 6
    ELSE       = 7
    END        = 31
    EQUAL      = 9
    FALSE      = 10
    GREATER    = 11
    GREATER_EQUAL = 12
    IDENTIFIER = 13
    IF         = 14
    INTEGER_LITERAL = 15
    INTEGER_TYPE = 16
    LESS       = 17
    LESS_EQUAL = 18
    MULTIPLICATION = 19
    PERIOD     = 20
    PROGRAM    = 21
    READ       = 22
    SEMICOLON  = 23
    SUBTRACTION = 24
    THEN       = 25
    TRUE       = 26
    VAR        = 27
    WHILE      = 28
    WRITE      = 29
    BLOCK      = 30
    LITERAL    = 32

ab = {
    'ADDITION':Token.ADDITION,
    'ASSIGNMENT':Token.ASSIGNMENT,
    'BEGIN' :Token.BEGIN,
    'BOOLEAN_TYPE':Token.BOOLEAN_TYPE,
    'COLON':Token.COLON,
    'DO':Token.DO,
    'ELSE':Token.ELSE,
    'END.':Token.END,
    'EQUAL':Token.EQUAL,
    'FALSE':Token.FALSE,
    'GREATER':Token.GREATER,
    'GREATER_EQUAL':Token.GREATER_EQUAL,
    'IDENTIFIER':Token.IDENTIFIER,
    'IF':Token.IF,
    'INTEGER_TYPE':Token.INTEGER_TYPE,
    'LESS':Token.LESS,
    'LESS_EQUAL':Token.LESS_EQUAL,
    'MULTIPLICATION':Token.MULTIPLICATION,
    'PERIOD':Token.PERIOD,
    'PROGRAM':Token.PROGRAM,
    'READ':Token.READ,
    'SEMICOLON':Token.SEMICOLON,
    'SUBTRACTION':Token.SUBTRACTION,
    'THEN':Token.THEN,
    'TRUE':Token.TRUE,
    'VAR':Token.VAR,
    'WHILE':Token.WHILE,
    'WRITE':Token.WRITE,
    'LITERAL':Token.LITERAL
}

# lexeme to token conversion
lookup = {
    "+"      : Token.ADDITION,
    "-"      : Token.SUBTRACTION,
    ""      : Token.MULTIPLICATION,
    "PR"     : Token.PROGRAM,
    "ASSIGNMENT" : Token.ASSIGNMENT,
    "BEGIN"  : Token.BEGIN,
    "BOOLEAN_TYPE" :Token.BOOLEAN_TYPE,
    ":"      : Token.COLON,
    "DO"     : Token.DO,
    "ELSE"   : Token.ELSE,
    "END"    : Token.END,
    "="      : Token.EQUAL,
    "FALSE"  : Token.FALSE,
    ">"      : Token.GREATER,
    ">="     : Token.GREATER_EQUAL,
    "ID"     : Token.IDENTIFIER,
    "IF"     : Token.IF,
    "IL"     : Token.INTEGER_LITERAL,
    "INT_TYPE": Token.INTEGER_TYPE,
    "<"      : Token.LESS,
    "<="     : Token.LESS_EQUAL,
    ""      : Token.MULTIPLICATION,
    "."      : Token.PERIOD,
    "PROGRAM"     : Token.PROGRAM,
    "READ"   : Token.READ,
    ";"      : Token.SEMICOLON,
    "-"      : Token.SUBTRACTION,
    "THEN"   : Token.SUBTRACTION,
    "TRUE"   : Token.TRUE,
    "VAR"    : Token.VAR,
    "WHILE"  : Token.WHILE,
    "WRITE"  : Token.WRITE
}

# returns the next (lexeme, token) pair or None if EOF is reached
def lex(input):
    bad_chars = ['.', ';', ':']
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return (input, None, None)

    # TODO: reading letters
    if charClass == CharClass.LETTER:
        while ((c not in bad_chars) and (charClass != charClass.BLANK)):
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
        if lexeme.upper() in ab:
            token = ab[lexeme.upper()]
        else:
            token = Token.IDENTIFIER
        if ((lexeme == "INTEGER") or (lexeme == "integer")):
            token = Token.INTEGER_TYPE
        if ((lexeme == "END") or (lexeme == 'end')):
            token = Token.END
        return (input, lexeme, token)


    # TODO: reading digits
    if charClass == CharClass.DIGIT:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass != CharClass.DIGIT:
                break
        return (input, lexeme, Token.INTEGER_LITERAL)

    # TODO: reading an operator
    if charClass == CharClass.OPERATOR:
        if ((c == '<') or (c == '>')):
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if c == "=":
                input, lexeme = addChar(input, lexeme)
                return (input, lexeme, lookup[lexeme])
            else:
                return (input, lexeme, lookup[lexeme])
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookup:
            return (input, lexeme, lookup[lexeme])

    # TODO: anything else, raise an exception
    if charClass == CharClass.PUNCTUATOR:
        if c == ":":
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if c == "=":
                input, lexeme = addChar(input, lexeme)
                return (input, lexeme, Token.ASSIGNMENT)
            else:
                return (input, lexeme, Token.COLON)
        else:
            input, lexeme = addChar(input, lexeme)
            return (input, lexeme, lookup[lexeme])

    raise Exception("3 Lexical Error: unrecognized symbol was found!")

# main
if __name__ == "__main__":

    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Couldn't open source file")
    input = source.read()
    source.close()
    output = []

    # main loop
    while True:
        input, lexeme, token = lex(input)
        if lexeme == None:
            break
        output.append((lexeme, token))

    # prints the output
    for (lexeme, token) in output:
        print(lexeme, token)
