#file to manage syntax_tree and lex
#Tanner and Ryan McCullough

import lex
import syntax_tree
import tree
import sys
from os import path
from tree import Tree

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
        grammar = open("grammar1.txt", 'rt')
    except Exception as e:
        raise IOError("4 Couldnt open grammar file\nUnable to locate/validate grammar text file")

    try:
        gtable = open("grammar_v3_updt.csv", 'rt')
    except Exception as e:
        raise IOError("5 Couldnt open SLR table file\nUnable to locate/validate SLR table csv file")

    input = source.read()
    while(True):
        input, lexeme, token = lex.lex(input)
        if lexeme == None:
            break
        output.append((lexeme, token))

    print(len(output))

    grammar = syntax_tree.loadGrammar(grammar)
    actions, gotos = syntax_tree.loadTable(gtable)

    #syntax_tree.printGrammar(grammar)
    #syntax_tree.printActions(actions)
    #syntax_tree.printGotos(gotos)

    #tree = syntax_tree.parse(output, grammar, actions, gotos)
"""
    if tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        tree.print()
    else:
        raise SyntaxError("Syntax Error")
"""
if __name__ == "__main__":
  manager(sys.argv)
