#file to manage syntax_tree and lex
#Tanner Madsen and Ryan McCullough

import lex
import syntax_tree
import tree
import sys
from os import path
from tree import Tree
from enum import Enum

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


def manager(i):
    output = []
    if len(i) < 2:
        raise ValueError("Invalid source file received")

    if not(path.exists(i[1])):
        raise IOError("1 Source file missing")

    try:
         source = open(i[1], 'rt')
    except Exception as e:
        raise IOError("2 Couldnt open source file\confirm permissions on source file")

    try:
        grammar = open("grammar2.txt", 'rt')
    except Exception as e:
        raise IOError("4 Couldnt open grammar file\nUnable to locate/validate grammar text file")

    try:
        gtable = open("grammarv6.csv", 'rt')
    except Exception as e:
        raise IOError("5 Couldnt open SLR table file\nUnable to locate/validate SLR table csv file")

    input = source.read()
    while(True):
        input, lexeme, token = lex.lex(input)
        if lexeme == None:
            break
        output.append((lexeme, token))

    print(output)

    grammar = syntax_tree.loadGrammar(grammar)
    actions, gotos = syntax_tree.loadTable(gtable)

    if output[1][1] != Token.IDENTIFIER:
        raise Exception("Error 07: identifier expected")
    if output[2][0] != 'VAR':
        raise Exception("Error 08: special word missing")

    #syntax_tree.printGrammar(grammar)
    #syntax_tree.printActions(actions)
    #syntax_tree.printGotos(gotos)

    tree = syntax_tree.parse(output, grammar, actions, gotos)

    if tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        tree.print()
    else:
        raise SyntaxError("Syntax Error")

if __name__ == "__main__":
  manager(sys.argv)
