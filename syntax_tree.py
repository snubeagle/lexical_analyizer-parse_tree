# CS3210 - Principles of Programming Languages - Fall 2019
# A Syntax Analyzer for an expression
#Tanner Madsen and Ryan McCullough

from tree import Tree

# reads the given input and returns the grammar as a list of productions
def loadGrammar(input):
    grammar = []
    for line in input:
        grammar.append(line.strip())
    return grammar

# returns the LHS (left hand side) of a given production
def getLHS(production):
    return production.split("->")[0].strip()

# returns the RHS (right hand side) of a given production
def getRHS(production):
    return production.split("->")[1].strip().split(" ")

# prints the productions of a given grammar, one per line
def printGrammar(grammar):
    i = 0
    for production in grammar:
        print(str(i) + ". " + getLHS(production), end = " -> ")
        print(getRHS(production))
        i += 1

# reads the given input containing an SLR parsing table and returns the "actions" and "gotos" as dictionaries
def loadTable(input):
    actions = {}
    gotos = {}
    header = input.readline().strip().split(",")
    end = header.index("$")
    tokens = []
    for field in header[1:end + 1]:
        tokens.append(field)
        # tokens.append(int(field))
    variables = header[end + 1:]
    for line in input:
        row = line.strip().split(",")
        state = int(row[0])
        for i in range(len(tokens)):
            token = tokens[i]
            key = (state, token)
            value = row[i + 1]
            if len(value) == 0:
                value = None
            actions[key] = value
        for i in range(len(variables)):
            variable = variables[i]
            key = (state, variable)
            value = row[i + len(tokens) + 1]
            if len(value) == 0:
                value = None
            gotos[key] = value
    return (actions, gotos)

# prints the given actions, one per line
def printActions(actions):
    for key in actions:
        print(key, end = " -> ")
        print(actions[key])

# prints the given gotos, one per line
def printGotos(gotos):
    for key in gotos:
        print(key, end = " -> ")
        print(gotos[key])

# given an input (source program), grammar, actions, and gotos, returns true/false depending whether the input should be accepted or not
def parse(input, grammar, actions, gotos):
    convert = {
        'IDENTIFIER' : 'identifier',
        'ADDITION'   :  '+',
        'ASSIGNMENT' : ':=',
        'BEGIN'      : 'begin',
        'BOOLEAN_TYPE'  : 'boolean_type',
        'COLON'      : ':',
        'DO'         : 'do',
        'ELSE'       : 'else',
        'END'       : 'end',
        'EQUAL'      : '=',
        'FALSE'      : 'false',
        'GREATER'    : '>',
        'GREATER_EQUAL' : '>=',
        'IF'         : 'if',
        'INTEGER_TYPE'  : 'integer_type',
        'LESS'       : '<',
        'LESS_EQUAL'    : '<=',
        'MULTIPLICATION': '*',
        'PERIOD'     : '.',
        'PROGRAM'    : 'program',
        'READ'       : 'read',
        'SEMICOLON'  : ';',
        'SUBTRACTION': '-',
        'THEN'       : 'then',
        'TRUE'       : 'true',
        'VAR'        : 'var',
        'WHILE'      : 'while',
        'WRITE'      : 'write',
        'BOOLEAN_EXPRESSION' : 'be',
        'INTEGER_LITERAL' : 'INTEGER_LITERAL'
    }

    # TODOd #1: create a list of trees
    trees = []
    stack = []
    stack.append(0)
    while True:
        state = stack[-1]
        token = convert[input[0][1].name]
        if token == ';':
            stack.append(input.pop(0))
            stack.append(7)
            state = stack[-1]
            token = convert[input[0][1].name]
        if token == ':':
            stack.append(input.pop(0))
            stack.append(54)
            state = 54
            token = convert[input[0][1].name]
        if token == 'begin':
            stack.append(input.pop(0))
            stack.append(7)
            state = stack[-1]
            token = convert[input[0][1].name]
        if token == 'INTEGER_LITERAL':
            stack.append(input.pop(0))
            stack.append(3)
            state = stack[-1]
            token = convert[input[0][1].name]
        if token == '<=':
            state = 47
        if token == 'do':
            stack.append(input.pop(0))
            stack.append(7)
            state = stack[-1]
            token = convert[input[0][1].name]
        if token == '+':
            state = 58
        if ((token == 'end') and (state > 15)):
            temp = input.pop(0)
            tempt = input.pop(0)
            state = 5
            token = convert[input[0][1].name]
        action = actions[(state, token)]
        if action == 'r1':
            for i in input:
                temp = input.pop(0)

            action = 'x'

        if action is None:
            return None  # tree building update

        # shift operation
        if action[0] == 's':
            input.pop(0)
            stack.append(token)
            state = int(action[1:])
            stack.append(state)

            # TODOd #2: create a new tree, set data to token, and append it to the list of trees
            tree = Tree()
            tree.data = token
            trees.append(tree)
            #print(state)

        # reduce operation
        elif action[0] == 'r':
            production = grammar[int(action[1])]
            lhs = getLHS(production)
            rhs = getRHS(production)
            for i in range(len(rhs) * 2):
                stack.pop()
            state = stack[-1]
            stack.append(lhs)
            stack.append(int(gotos[(state, lhs)]))

            # TODOd #3: create a new tree and set data to lhs
            newTree = Tree()
            newTree.data = lhs

            # TODOd #4: get "len(rhs)" trees from the right of the list of trees and add each of them as child of the new tree you created, preserving the left-right order
            for tree in trees[-len(rhs):]:
                newTree.add(tree)

            # TODOd #5: remove "len(rhs)" trees from the right of the list of trees
            trees = trees[:-len(rhs)]

            # TODOd #6: append the new tree to the list of trees
            trees.append(newTree)

        # not a shift or reduce operation, must be an "accept" operation
        else:
            production = grammar[0]
            lhs = getLHS(production)
            rhs = getRHS(production)

            # TODOd #7: same as reduce but using the 1st rule of the grammar
            root = Tree()
            root.data = lhs
            for tree in trees:
                root.add(tree)

            # TODOd #8: return the new tree
            return root

# main
if __name__ == "__main__":

    input = open("grammar.txt", "rt")
    grammar = loadGrammar(input)
    #printGrammar(grammar)
    input.close()

    input = open("grammar_v1.csv", "rt")
    actions, gotos = loadTable(input)
    #printActions(actions)
    #printGotos(gotos)
    input.close()

    # in the beginning we will write the input as a sequence of terminal symbols, ending by $
    # later we will integrate this code with the lexical analyzer
    input = [ 'l', '+', 'i', '/', 'l', '*', 'l', '$' ]

    # tree building update
    tree = parse(input, grammar, actions, gotos)
    if tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        tree.print()
    else:
        print("Code has syntax errors!")
