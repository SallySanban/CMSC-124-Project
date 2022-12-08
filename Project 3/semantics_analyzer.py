import lexical_analyzer
import syntax_analyzer
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkinter.filedialog
import tkinter.scrolledtext as scrolledtext

types = {}
lexemes = {}
newSymbolTable = {}

literals = ["NUMBR literal",
            "NUMBAR literal",
            "YARN literal",
            "TROOF literal",
            "TYPE literal"
            ]

expressionKeywords = {
                        "arithmetic":
                            ["SUM OF",
                            "DIFF OF",
                            "PRODUKT OF",
                            "QUOSHUNT OF",
                            "MOD OF",
                            "BIGGR OF",
                            "SMALLR OF"],
                        "boolean":
                            ["BOTH OF",
                            "EITHER OF",
                            "WON OF",
                            "NOT",
                            "ANY OF",
                            "ALL OF"],
                        "comparison":
                            ["BOTH SAEM",
                            "DIFFRINT"],
                        "concatenation":
                            ["SMOOSH"]
                    }

BACKGROUND_COLOR = "#e0e0de"
filename = ""

def makeTokens():
    global listOfTokens, tokensTree

    tokens = []
    for i in lexemes.keys():
        for j in range(0, len(lexemes[i])):
            tokens.append((lexemes[i][j], types[i][j]))

    x = tokensTree.get_children()
    for item in x:
        tokensTree.delete(item)

    for i in tokens:
        tokensTree.insert('', 'end', text="1", values=i)

def makeSymbolTable(symbolTable):
    global listOfSymbolTable, symbolTableTree

    refactoredSymbolTable = []
    for i in symbolTable.keys():
        refactoredSymbolTable.append((i, symbolTable[i][0], symbolTable[i][1]))

    for item in symbolTableTree.get_children():
      symbolTableTree.delete(item)

    for i in refactoredSymbolTable:
        symbolTableTree.insert('', 'end', text="1", values=i)

def openFile():
    global filename

    textEditor.delete(1.0, END)

    filename = tkinter.filedialog.askopenfilename()

    file = open(filename)

    for i in file.readlines():
        textEditor.insert(END, i)

def getInput():
    inputBox.config(state=NORMAL)
    enterButton.config(state=NORMAL)
    enterButton.wait_variable(enterClicked)

    return inputBox.get()
    
def saveInput():
    enterClicked.set("button pressed")

def run():
    global filename, lexemes, types, newSymbolTable

    lexemes = {}
    types = {}
    newSymbolTable = {}

    if(textEditor.get(1.0, END) != "\n"):
        console.config(state=NORMAL)
        console.delete(1.0, END)
        console.config(state=DISABLED)

        listOfLines = []
        for i in textEditor.get(1.0, END).splitlines():
            listOfLines.append(i + "\n")

        lines = lexical_analyzer.readFile(listOfLines)
        lexical_analyzer.findLexemes(lines, lexemes, types)

        #syntaxError = syntax_analyzer.syntax(lexemes, types)

        # if("SyntaxError" in syntaxError):
        #     messagebox.showinfo('Syntax Error', syntaxError)
        # else:
        semanticError = semantics()

        if("SemanticError" in semanticError):
            messagebox.showinfo('Semantic Error', semanticError)
        else:
            makeTokens()
            makeSymbolTable(semanticError)
    else:
        textEditor.insert(END, "Please open a file or type some code")

def nextLineNumber(lineNumber):
    found = False

    for i in types.keys():
        if(i == lineNumber):
            found = True
            continue
        
        if(found):
            return i

#takes line number, index of the value of variable (which also has the type), and name of variable
def updateSymbolTable(lineNumber, value, variable):
    if(value == "NOOB"):
        newSymbolTable[variable] = ["NOOB", "NOOB"]
    elif(isinstance(value, list)):
        newSymbolTable[variable] = value
    else:
        if(types[lineNumber][value] == "NUMBR literal"):  #value is numbr
            newSymbolTable[variable] = [int(lexemes[lineNumber][value]), "NUMBR literal"]
        elif(types[lineNumber][value] == "NUMBAR literal"):   #value is numbar
            newSymbolTable[variable] = [float(lexemes[lineNumber][value]), "NUMBAR literal"]
        elif(types[lineNumber][value] == "YARN literal"): #value is yarn
            newSymbolTable[variable] = [str(lexemes[lineNumber][value]), "YARN literal"]
        elif(types[lineNumber][value] == "TROOF literal"):    #value is troof
            if(lexemes[lineNumber][value] == "WIN"):
                newSymbolTable[variable] = [True, "TROOF literal"]
            elif(lexemes[lineNumber][value] == "FAIL"):
                newSymbolTable[variable] = [False, "TROOF literal"]
        else:   #value is type
            return "[Line " + str(lineNumber) + "] SemanticError: cannot store TYPE in identifier"
    
    return "OK"

def arithmeticExpressionSemantics(lineNumber, variable):
    operatorCount = 0    

    # * Gets the index of ITZ
    if("variable initialization keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("ITZ")
    #put other cases where the arithmetic expression might be
    elif("print keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("VISIBLE")
    else:
        expressionIndex = -1       
    
    # * Counts the number of operations in the arithmetic expression
    for typeLiteral in ['add operator', 'subtract operator', 'multiply operator', 'divide operator', 'modulo operator']:
        operatorCount += types[lineNumber].count(typeLiteral)
    
    # print(lexemes[lineNumber])
    # print(types[lineNumber])
    # print(operatorCount)
    
    # Flow: Start sa innermost to outermost
        # first operator appears +n from ITZ
        # Implicit typecasting for troof, 
        # Check if current type of identifier is numbar, numbr
        # Check if current type of literal is numbr, numbar

    # I HAS A sum ITZ SUM OF DIFF OF num AN 13 AN 21
    # I HAS A sum ITZ SUM OF DIFF OF PRODUKT OF num AN 13 AN 21 AN 4

    # ! CHECKLIST CASES:
    #  ! SUM OF SUM OF <x> AN <y> AN <z>
        
    tempVal = 0         # Accumulator
    tempCount = 1           # Index for the source operands
    boolNested = False      # Flag if nested arithmetic operation
    while operatorCount > 1:
        boolNested = True
        if tempCount == 1:          # Innermost operation
            # * 1st N
            if (newSymbolTable.get(lexemes[lineNumber][expressionIndex + operatorCount + tempCount])):         # Existing Identifier
                # ! Check type
                if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                    tempVal = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0], "NUMBR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                    tempVal = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0], "NUMBAR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "YARN literal"):
                    try:
                        tempVal = [int(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                    except ValueError:
                        try:
                            tempVal = [float(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                        except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                    if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]):
                        tempVal = [1, "NUMBR literal"]
                    else:
                        tempVal = [0, "NUMBR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NOOB"):
                    return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"

                # * 2nd N
                if (newSymbolTable.get(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2])): # Existing Identifier
                    temp = 0
                    # ! Check type
                    if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NUMBR literal"):
                        temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0], "NUMBR literal"]
                    elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NUMBAR literal"):
                        temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0], "NUMBAR literal"]
                    elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "YARN literal"):
                        try:
                            temp = [int(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                        except ValueError:
                            try:
                                temp = [float(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]), "NUMBAR literal"]
                            except ValueError:
                                return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                    elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "TROOF literal"):
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]):
                            if (tempVal[1] == "NUMBR literal"):
                                temp = [1, "NUMBR literal"]
                            else:
                                temp = [1.0, "NUMBAR literal"]
                        else:
                            if (tempVal[1] == "NUMBR literal"):
                                temp = [0, "NUMBR literal"]
                            else:
                                temp = [0.0, "NUMBAR literal"]
                    elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NOOB"):
                        return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"

                    if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                        tempVal[0] += temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                        tempVal[0] -= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                        tempVal[0] *= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                        tempVal[0] /= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                        tempVal[0] %= temp[0]
                else:           # * Literal
                    # if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "invalid keyword"):
                    #     print(f"[Line " + str(lineNumber) + "] SemanticError: Invalid identifier used in arithmetic expression")
                    #     break
                    # ! Check type
                    temp = 0
                    if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NUMBR literal"):
                        temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                    elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NUMBAR literal"):
                        temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBAR literal"]
                    elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "YARN literal"):
                        try:
                            temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                        except ValueError:
                            try:
                                temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                            except ValueError:
                                return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                    elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "TROOF literal"):
                        if (lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "WIN"):
                            if (tempVal[1] == "NUMBR literal"):
                                temp = [1, "NUMBR literal"]
                            else:
                                temp = [1.0, "NUMBAR literal"]
                        else:
                            if (tempVal[1] == "NUMBR literal"):
                                temp = [0, "NUMBR literal"]
                            else:
                                temp = [0.0, "NUMBAR literal"]
                    elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NOOB"):
                        return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"


                    if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                        tempVal[0] += temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                        tempVal[0] -= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                        tempVal[0] *= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                        tempVal[0] /= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                        tempVal[0] %= temp[0]

            # * 1st N
            else:           # * Literal
                # if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "invalid keyword"):
                #     print(f"[Line " + str(lineNumber) + "] SemanticError: Invalid identifier used in arithmetic expression")
                #     break

                # ! Check type
                if (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NUMBR literal"):
                    tempVal = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NUMBAR literal"):
                    tempVal = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBAR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "YARN literal"):
                    try:
                        tempVal = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                    except ValueError:
                        try:
                            tempVal = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                        except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "TROOF literal"):
                    if (lexemes[lineNumber][expressionIndex + operatorCount + tempCount] == "WIN"):
                        tempVal = [1, "NUMBR literal"]
                    else:
                        tempVal = [0, "NUMBR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NOOB"):
                    return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"
                
                # * 2nd N
                if (newSymbolTable.get(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2])): # Existing Identifier
                    temp = 0
                    # ! Check type
                    if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NUMBR literal"):
                        temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0], "NUMBR literal"]
                    elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NUMBAR literal"):
                        temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0], "NUMBAR literal"]
                    elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "YARN literal"):
                        try:
                            temp = [int(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                        except ValueError:
                            try:
                                temp = [float(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                            except ValueError:
                                return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                    elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "TROOF literal"):
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]):
                            if (tempVal[1] == "NUMBR literal"):
                                temp = [1, "NUMBR literal"]
                            else:
                                temp = [1.0, "NUMBAR literal"]
                        else:
                            if (tempVal[1] == "NUMBR literal"):
                                temp = [0, "NUMBR literal"]
                            else:
                                temp = [0.0, "NUMBAR literal"]
                    elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NOOB"):
                        return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"
                    
                    if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                        tempVal[0] += temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                        tempVal[0] -= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                        tempVal[0] *= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                        tempVal[0] /= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                        tempVal[0] %= temp[0]
                else:           # * Literal
                    # if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "invalid keyword"):
                    #     print(f"[Line " + str(lineNumber) + "] SemanticError: Invalid identifier used in arithmetic expression")
                    #     break

                    # ! Check type
                    temp = 0
                    if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NUMBR literal"):
                        temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                    elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NUMBAR literal"):
                        temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBAR literal"]
                    elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "YARN literal"):
                        try:
                            temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                        except ValueError:
                            try:
                                temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                            except ValueError:
                                return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                    elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "TROOF literal"):
                        if (lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "WIN"):
                            if (tempVal[1] == "NUMBR literal"):
                                temp = [1, "NUMBR literal"]
                            else:
                                temp = [1.0, "NUMBAR literal"]
                        else:
                            if (tempVal[1] == "NUMBR literal"):
                                temp = [0, "NUMBR literal"]
                            else:
                                temp = [0.0, "NUMBAR literal"]
                    elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NOOB"):
                        return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"


                    if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                        tempVal[0] += temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                        tempVal[0] -= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                        tempVal[0] *= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                        tempVal[0] /= temp[0]
                    elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                        tempVal[0] %= temp[0]


            operatorCount -= 1
            tempCount += 5
            continue
        else:   # * More nested expressions
            # ! Check type 
            temp = 0

            if (newSymbolTable.get(lexemes[lineNumber][expressionIndex + operatorCount + tempCount])): # Existing Identifier
                temp = 0
                # ! Check type
                if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                    temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0], "NUMBR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                    temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0], "NUMBAR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "YARN literal"):
                    try:
                        temp = [int(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                    except ValueError:
                        try:
                            temp = [float(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                        except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                    if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]):
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [1, "NUMBR literal"]
                        else:
                            temp = [1.0, "NUMBAR literal"]
                    else:
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [0, "NUMBR literal"]
                        else:
                            temp = [0.0, "NUMBAR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NOOB"):
                    return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"

                if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                    tempVal[0] += temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                    tempVal[0] -= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                    tempVal[0] *= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                    tempVal[0] /= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                    tempVal[0] %= temp[0]
            else:           # * Literal
                # if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "invalid keyword"):
                #     print(f"[Line " + str(lineNumber) + "] SemanticError: Invalid identifier used in arithmetic expression")
                #     break
                
                # ! Check type
                temp = 0
                if (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NUMBR literal"):
                    temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NUMBAR literal"):
                    temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBAR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "YARN literal"):
                    try:
                        temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                    except ValueError:
                        try:
                            temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                        except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "TROOF literal"):
                    if (lexemes[lineNumber][expressionIndex + operatorCount + tempCount] == "WIN"):
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [1, "NUMBR literal"]
                        else:
                            temp = [1.0, "NUMBAR literal"]
                    else:
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [0, "NUMBR literal"]
                        else:
                            temp = [0.0, "NUMBAR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NOOB"):
                    return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"


                if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                    tempVal[0] += temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                    tempVal[0] -= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                    tempVal[0] *= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                    tempVal[0] /= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                    tempVal[0] %= temp[0]


        operatorCount -= 1
        tempCount += 3

    
    # * ONLY REACHES HERE IF THIS IS THE OUTERMOST OPERATION
    # I HAS A sum ITZ SUM OF num AN 13                                  # 3
    # I HAS A sum ITZ SUM OF DIFF OF num AN 13 AN 21                        # 6
    # I HAS A sum ITZ SUM OF DIFF OF PRODUKT OF num AN 13 AN 21 AN 4            # 9
    # I HAS A sum ITZ SUM OF DIFF OF PRODUKT OF SUM OF num AN 13 AN 21 AN 4 AN 11   # 12

    if (not boolNested):          # ! SINGLE OPERATION
        # * 1st N
        if (newSymbolTable.get(lexemes[lineNumber][expressionIndex + operatorCount + tempCount])):         # Existing Identifier
            # ! Check type
            if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                tempVal = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0], "NUMBR literal"]
            elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                tempVal = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0], "NUMBAR literal"]
            elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "YARN literal"):
                try:
                    tempVal = [int(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                except ValueError:
                    try:
                        tempVal = [float(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                    except ValueError:
                        return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
            elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]):
                    tempVal = [1, "NUMBR literal"]
                else:
                    tempVal = [0, "NUMBR literal"]
            elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NOOB"):
                return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"

            # * 2nd N
            if (newSymbolTable.get(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2])): # Existing Identifier
                temp = 0
                # ! Check type
                if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NUMBR literal"):
                    temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0], "NUMBR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NUMBAR literal"):
                    temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0], "NUMBAR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "YARN literal"):
                    try:
                        temp = [int(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                    except ValueError:
                        try:
                            temp = [float(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                        except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "TROOF literal"):
                    if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]):
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [1, "NUMBR literal"]
                        else:
                            temp = [1.0, "NUMBAR literal"]
                    else:
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [0, "NUMBR literal"]
                        else:
                            temp = [0.0, "NUMBAR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NOOB"):
                    return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"

                if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                    tempVal[0] += temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                    tempVal[0] -= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                    tempVal[0] *= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                    tempVal[0] /= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                    tempVal[0] %= temp[0]
            else:           # * Literal
                # if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "invalid keyword"):
                #     print(f"[Line " + str(lineNumber) + "] SemanticError: Invalid identifier used in arithmetic expression")
                #     break
                
                # ! Check type
                temp = 0
                if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NUMBR literal"):
                    temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NUMBAR literal"):
                    temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBAR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "YARN literal"):
                    try:
                        temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                    except ValueError:
                        try:
                            temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                        except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "TROOF literal"):
                    if (lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "WIN"):
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [1, "NUMBR literal"]
                        else:
                            temp = [1.0, "NUMBAR literal"]
                    else:
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [0, "NUMBR literal"]
                        else:
                            temp = [0.0, "NUMBAR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NOOB"):
                    return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"

                if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                    tempVal[0] += temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                    tempVal[0] -= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                    tempVal[0] *= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                    tempVal[0] /= temp[0]
                elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                    tempVal[0] %= temp[0]
        # * 1st N
        else:           # * Literal
            # if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "invalid keyword"):
            #     print(f"[Line " + str(lineNumber) + "] SemanticError: Invalid identifier used in arithmetic expression")
            #     break
            # ! Check type

            if (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NUMBR literal"):
                tempVal = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
            elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NUMBAR literal"):
                tempVal = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBAR literal"]
            elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "YARN literal"):
                try:
                    tempVal = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                except ValueError:
                    try:
                        tempVal = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                    except ValueError:
                        return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
            elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "TROOF literal"):
                if (lexemes[lineNumber][expressionIndex + operatorCount + tempCount] == "WIN"):
                    tempVal = [1, "NUMBR literal"]
                else:
                    tempVal = [0, "NUMBR literal"]
            elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NOOB"):
                return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"

            # * 2nd N
            if (newSymbolTable.get(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2])): # Existing Identifier
                temp = 0
                # ! Check type
                if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NUMBR literal"):
                    temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0], "NUMBR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NUMBAR literal"):
                    temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0], "NUMBAR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "YARN literal"):
                    try:
                        temp = [int(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                    except ValueError:
                        try:
                            temp = [float(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                        except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "TROOF literal"):
                    if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][0]):
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [1, "NUMBR literal"]
                        else:
                            temp = [1.0, "NUMBAR literal"]
                    else:
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [0, "NUMBR literal"]
                        else:
                            temp = [0.0, "NUMBAR literal"]
                elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]][1] == "NOOB"):
                    return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"
            else:           # * Literal
                # if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "invalid keyword"):
                #     print(f"[Line " + str(lineNumber) + "] SemanticError: Invalid identifier used in arithmetic expression")
                #     break
                
                # ! Check type
                temp = 0
                if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NUMBR literal"):
                    temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NUMBAR literal"):
                    temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBAR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "YARN literal"):
                    try:
                        temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                    except ValueError:
                        try:
                            temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                        except ValueError:
                            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "TROOF literal"):
                    if (lexemes[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "WIN"):
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [1, "NUMBR literal"]
                        else:
                            temp = [1.0, "NUMBAR literal"]
                    else:
                        if (tempVal[1] == "NUMBR literal"):
                            temp = [0, "NUMBR literal"]
                        else:
                            temp = [0.0, "NUMBAR literal"]
                elif (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "NOOB"):
                    return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"


            if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                tempVal[0] += temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                tempVal[0] -= temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                tempVal[0] *= temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                tempVal[0] /= temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                tempVal[0] %= temp[0]
        
        # * STORES THE FINAL VALUE OF TEMP HERE
        if(variable != "IT"):
            variable = lexemes[lineNumber][1]

        updateSymbolTable(lineNumber, [tempVal[0], tempVal[1]], variable)
    else:     
        temp = 0
        if (newSymbolTable.get(lexemes[lineNumber][expressionIndex + operatorCount + tempCount])): # Existing Identifier
            temp = 0
            # ! Check type
            if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0], "NUMBR literal"]
            elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                temp = [newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0], "NUMBAR literal"]
            elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "YARN literal"):
                try:
                    temp = [int(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                except ValueError:
                    try:
                        temp = [float(newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                    except ValueError:
                        return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
            elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                if (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][0]):
                    if (tempVal[1] == "NUMBR literal"):
                        temp = [1, "NUMBR literal"]
                    else:
                        temp = [1.0, "NUMBAR literal"]
                else:
                    if (tempVal[1] == "NUMBR literal"):
                        temp = [0, "NUMBR literal"]
                    else:
                        temp = [0.0, "NUMBAR literal"]
            elif (newSymbolTable[lexemes[lineNumber][expressionIndex + operatorCount + tempCount]][1] == "NOOB"):
                return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"

            if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                tempVal[0] += temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                tempVal[0] -= temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                tempVal[0] *= temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                tempVal[0] /= temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                tempVal[0] %= temp[0]
        else:           # * Literal
            # if (types[lineNumber][expressionIndex + operatorCount + tempCount + 2] == "invalid keyword"):
            #     print(f"[Line " + str(lineNumber) + "] SemanticError: Invalid identifier used in arithmetic expression")
            #     break
            
            # ! Check type
            temp = 0
            if (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NUMBR literal"):
                temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
            elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NUMBAR literal"):
                temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBAR literal"]
            elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "YARN literal"):
                try:
                    temp = [int(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                except ValueError:
                    try:
                        temp = [float(lexemes[lineNumber][expressionIndex + operatorCount + tempCount]), "NUMBR literal"]
                    except ValueError:
                        return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR or NUMBAR literal"
            elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "TROOF literal"):
                if (lexemes[lineNumber][expressionIndex + operatorCount + tempCount] == "WIN"):
                    if (tempVal[1] == "NUMBR literal"):
                        temp = [1, "NUMBR literal"]
                    else:
                        temp = [1.0, "NUMBAR literal"]
                else:
                    if (tempVal[1] == "NUMBR literal"):
                        temp = [0, "NUMBR literal"]
                    else:
                        temp = [0.0, "NUMBAR literal"]
            elif (types[lineNumber][expressionIndex + operatorCount + tempCount] == "NOOB"):
                return "[Line " + str(lineNumber) + "] SemanticError: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal"


            if (types[lineNumber][expressionIndex + operatorCount] == "add operator"):
                tempVal[0] += temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "subtract operator"):
                tempVal[0] -= temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "multiply operator"):
                tempVal[0] *= temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "divide operator"):
                tempVal[0] /= temp[0]
            elif (types[lineNumber][expressionIndex + operatorCount] == "modulo operator"):
                tempVal[0] %= temp[0]

        # * STORES THE FINAL VALUE OF TEMP HERE
        if(variable != "IT"):
            variable = lexemes[lineNumber][1]

        updateSymbolTable(lineNumber, [tempVal[0], tempVal[1]], variable)

    return "OK"

def comparisonExpressionSemantics(lineNumber, variable):
    # ! NO AUTOMATIC TYPECASTING IN COMPARISON SEMANTICS

    # * Gets the index of ITZ
    if("variable initialization keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("ITZ")
    #put other cases where the arithmetic expression might be
    elif("print keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("VISIBLE")
    else:
        expressionIndex = -1    
    
    # print(lexemes[lineNumber][expressionIndex])
    anIndices = []
    for index in range(len(lexemes[lineNumber])):
        if lexemes[lineNumber][index] == "AN":
            anIndices.append(index)
    
    
    if (len(anIndices) == 1):      # (x == y OR x != y)
        if lexemes[lineNumber][expressionIndex + 1] == "BOTH SAEM": # x == y
            if types[lineNumber][expressionIndex + 2] == "identifier":  # x = identifier
                if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 2]):
                    if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][0] == newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBR literal"):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][0] == int(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBAR literal"):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0] == float(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif types[lineNumber][expressionIndex + 2] == "NUMBR literal": # x = NUMBR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (int(lexemes[lineNumber][expressionIndex + 2]) == newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) == int(lexemes[lineNumber][expressionIndex + 4])):
                        temp = ["WIN", "TROOF literal"]
                    else:
                        temp = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) == float(lexemes[lineNumber][expressionIndex + 4])):
                        temp = ["WIN", "TROOF literal"]
                    else:
                        temp = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            elif types[lineNumber][expressionIndex + 2] == "NUMBAR literal":    # x = NUMBAR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (float(lexemes[lineNumber][expressionIndex + 2]) == newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) == int(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) == float(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:
                return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
        else:   # DIFFRINT      x != y
            if types[lineNumber][expressionIndex + 2] == "identifier":  # x = identifier
                if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 2]):
                    if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][0] != newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBR literal"):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][0] != int(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBAR literal"):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0] != float(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif types[lineNumber][expressionIndex + 2] == "NUMBR literal": # x = NUMBR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (int(lexemes[lineNumber][expressionIndex + 2]) != newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) != int(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) != float(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            elif types[lineNumber][expressionIndex + 2] == "NUMBAR literal":    # x = NUMBAR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (float(lexemes[lineNumber][expressionIndex + 2]) != newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) != int(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) != float(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:
                return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"

    else:       # (x <= y, x >= y, x < y, x > y)
        bigCnt = lexemes[lineNumber].count("BIGGR OF")
        try:
            sizeIndex = lexemes[lineNumber].index("BIGGR OF")
        except ValueError:
            sizeIndex = lexemes[lineNumber].index("SMALLR OF")


        if lexemes[lineNumber][expressionIndex + 1] == "BOTH SAEM": # x <= y, x >= y
            if (bigCnt == 0):       # x <= y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] <= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] <= int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0] <= float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) <= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) <= int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) <= float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) <= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) <= int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) <= float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:       # x >= y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] >= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] >= int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0] >= float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) >= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) >= int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) >= float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) >= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) >= int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) >= float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
        else: # DIFFRINT (x < y, x > y)
            if (bigCnt == 0):       # x > y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] > newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] > int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0] > float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) > newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) > int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) > float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) > newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) > int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) > float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:       # x < y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] < newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] < int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0] < float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) < newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) < int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) < float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) < newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) < int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) < float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"


    # * STORES THE FINAL VALUE OF TEMP HERE
    if(variable != "IT"):
        variable = lexemes[lineNumber][1]

    updateSymbolTable(lineNumber, [tempVal[0], tempVal[1]], variable)

    return "OK"

def concatenationExpressionSemantics(lineNumber, variable):
    # * AUTOMATICALLY TYPECAST INTO YARN EVERY DATA TYPE
    # ! NO OPERATIONS AS OPERANDS YET

    # * Gets the index of ITZ
    if("variable initialization keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("ITZ")
    #put other cases where the arithmetic expression might be
    elif("print keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("VISIBLE")
    else:
        expressionIndex = -1    
    
    #print(lexemes[lineNumber][expressionIndex])
    anIndices = []
    for index in range(len(lexemes[lineNumber])):
        if lexemes[lineNumber][index] == "AN":
            anIndices.append(index)
    
    counter = 0
    tempVal = ''
    while True:
        if (counter == len(anIndices) - 1):
            if (types[lineNumber][anIndices[counter] - 1] == "identifier"):
                if (newSymbolTable.get(lexemes[lineNumber][anIndices[counter] - 1])):
                    tempVal += str(newSymbolTable[lexemes[lineNumber][anIndices[counter] - 1]][0])
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif (types[lineNumber][anIndices[counter] - 1] == "string delimiter"):     # YARN literal
                if (types[lineNumber][anIndices[counter] - 3] == "string delimiter"):   # another delimiter
                    tempVal += lexemes[lineNumber][anIndices[counter] - 2]
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Invalid syntax of YARN literal"     # ! TAKE NOTE
            else:
                tempVal += str(lexemes[lineNumber][anIndices[counter] - 1])
            
            if (types[lineNumber][anIndices[counter] + 1] == "identifier"):
                if (newSymbolTable.get(lexemes[lineNumber][anIndices[counter] + 1])):
                    tempVal += str(newSymbolTable[lexemes[lineNumber][anIndices[counter] + 1]][0])
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif (types[lineNumber][anIndices[counter] + 1] == "string delimiter"):     # YARN literal
                if (types[lineNumber][anIndices[counter] + 3] == "string delimiter"):   # another delimiter
                    tempVal += lexemes[lineNumber][anIndices[counter] + 2]
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Invalid syntax of YARN literal"     # ! TAKE NOTE
            else:
                tempVal += str(lexemes[lineNumber][anIndices[counter] + 1])

            break
        
        if (types[lineNumber][anIndices[counter] - 1] == "identifier"):
            if (newSymbolTable.get(lexemes[lineNumber][anIndices[counter] - 1])):
                tempVal += str(newSymbolTable[lexemes[lineNumber][anIndices[counter] - 1]][0])
            else:
                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
        elif (types[lineNumber][anIndices[counter] - 1] == "string delimiter"):     # YARN literal
                if (types[lineNumber][anIndices[counter] - 3] == "string delimiter"):   # another delimiter
                    tempVal += lexemes[lineNumber][anIndices[counter] - 2]
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Invalid syntax of YARN literal"     # ! TAKE NOTE
        else:
            tempVal += str(lexemes[lineNumber][anIndices[counter] - 1])


        counter += 1
    
    # * STORES THE FINAL VALUE OF TEMP HERE
    if(variable != "IT"):
        variable = lexemes[lineNumber][1]
    
    tempVal = [tempVal, "YARN literal"]

    updateSymbolTable(lineNumber, [tempVal[0], tempVal[1]], variable)

    return "OK"
        
def switchCaseSemantics(lineNumber, variable):
    # ! FLOW
    # * First line is WTF?
    # * Succeeding lines is OMG, OMGWTF (default case)
    # * Execution stops when there is an GTFO or OIC

    omgLineNumber = []
    omgWtfLineNumber = -1

    # * Gets the line number of the OMG and OMGWTF
    while lexemes[lineNumber][0] != "OIC":
        if lexemes[lineNumber][0] == "OMG":
            omgLineNumber.append(lineNumber)
        elif lexemes[lineNumber][0] == "OMGWTF":
            omgWtfLineNumber = lineNumber
        
        lineNumber = nextLineNumber(lineNumber)
    
    lineNumber = omgLineNumber[0] - 1       # Returns back the line number to where WTF? is
    
    # print(omgLineNumber)            # Checker
    # print(omgWtfLineNumber)
    # print(lineNumber)

    # * Checks if the IT value is equal to the cases in OMG
    checkedLine = -1
    for omg in omgLineNumber:
        if types[omg][1] in ["identifier", "NUMBR literal", "NUMBAR literal", "TROOF literal", "string literal"]:
            if types[omg][1] == "identifier":
                if newSymbolTable.get(lexemes[omg]):
                    if newSymbolTable[lexemes[omg]][0] == newSymbolTable["IT"][0] and newSymbolTable[lexemes[omg]][1] == "NUMBR literal" and newSymbolTable["IT"][1] == "NUMBR literal":
                        checkedLine = omg
                        break
                    elif newSymbolTable[lexemes[omg]][0] == newSymbolTable["IT"][0] and newSymbolTable[lexemes[omg]][1] == "NUMBAR literal" and newSymbolTable["IT"][1] == "NUMBAR literal":
                        checkedLine = omg
                        break
                    elif newSymbolTable[lexemes[omg]][0] == newSymbolTable["IT"][0] and newSymbolTable[lexemes[omg]][1] == "YARN literal" and newSymbolTable["IT"][1] == "YARN literal":
                        checkedLine = omg
                        break
                    elif newSymbolTable[lexemes[omg]][0] == newSymbolTable["IT"][0] and newSymbolTable[lexemes[omg]][1] == "TROOF literal" and newSymbolTable["IT"][1] == "TROOF literal":
                        checkedLine = omg
                        break
                    else:
                        continue        # If not equal or NOOB type
                else:
                    return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
            elif types[omg][1] == "NUMBR literal":
                if int(lexemes[omg][1]) == newSymbolTable["IT"][0]:
                    checkedLine = omg
                    break
            elif types[omg][1] == "NUMBAR literal":
                if float(lexemes[omg][1]) == newSymbolTable["IT"][0]:
                    checkedLine = omg
                    break
            elif types[omg][1] == "string delimiter":       # YARN literal
                if lexemes[omg][2] == newSymbolTable["IT"][0]:
                    checkedLine = omg
                    break
            elif types[omg][1] == "TROOF literal":          # DOUBLE CHECK FOR TROOF LITERALS
                if lexemes[omg][1] == "WIN":
                    if newSymbolTable["IT"][0]:
                        checkedLine = omg
                        break
                    else:
                        continue
                else:
                    if not newSymbolTable["IT"][0]:
                        checkedLine = omg
                        break
                    else:
                        continue
        else:
            continue
    
    if checkedLine == -1:       # GO TO DEFAULT CASE
        if omgWtfLineNumber == -1:      # No default case
            print("hahah")
        else:       # Go to default case
            print("hahah")
        print("")       
    else:
        print("hahah")

def iHasASemantics(lineNumber):
    if("variable initialization keyword" in types[lineNumber]): #variable has value
        itzLexeme = lexemes[lineNumber].index("ITZ")

        # TODO: doesnt accept if assigns to variable

        if(types[lineNumber][itzLexeme + 1] in literals): #checks if value is literal
            semanticsError = updateSymbolTable(lineNumber, itzLexeme + 1, lexemes[lineNumber][itzLexeme - 1])

            if(semanticsError != "OK"):
                return semanticsError

        elif(types[lineNumber][itzLexeme + 1] == "string delimiter" and types[lineNumber][itzLexeme + 2] == "YARN literal" and types[lineNumber][itzLexeme + 3] == "string delimiter"): #checks if string
            semanticsError = updateSymbolTable(lineNumber, itzLexeme + 2, lexemes[lineNumber][itzLexeme - 1])

            if(semanticsError != "OK"):
                return semanticsError

        elif(lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["arithmetic"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["boolean"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["comparison"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["concatenation"]): #if expression
            semanticsError = arithmeticExpressionSemantics(lineNumber, lexemes[lineNumber][itzLexeme - 1])

            if(semanticsError != "OK"):
                return semanticsError

    else:   #variable has no value
        iHasALexeme = lexemes[lineNumber].index("I HAS A")

        semanticsError = updateSymbolTable(lineNumber, "NOOB", lexemes[lineNumber][iHasALexeme + 1])

        if(semanticsError != "OK"):
            return semanticsError

    return "OK"

def visibleSemantics(lineNumber):
    console.config(state=NORMAL)
    visibleLexeme = lexemes[lineNumber].index("VISIBLE")

    # TODO: doesnt catch when more than one arity
    if(types[lineNumber][visibleLexeme + 1] == "identifier"):
        for i in newSymbolTable.keys():
            if(i == lexemes[lineNumber][visibleLexeme + 1]):
                if(newSymbolTable[i][1] == "TROOF literal"):
                    if(newSymbolTable[i][0] == True):
                        #print("WIN")
                        console.insert(END, "WIN\n")
                        console.config(state=DISABLED)
                    else:
                        #print("FAIL")
                        console.insert(END, "FAIL\n")
                        console.config(state=DISABLED)
                else:
                    #print(newSymbolTable[i][0])
                    console.insert(END, str(newSymbolTable[i][0]) + "\n")
                    console.config(state=DISABLED)
                return "OK"
    elif(types[lineNumber][visibleLexeme + 1] in literals):
        #print(lexemes[lineNumber][visibleLexeme + 1])
        console.insert(END, str(lexemes[lineNumber][visibleLexeme + 1]) + "\n")
        console.config(state=DISABLED)
        return "OK"
    elif(types[lineNumber][visibleLexeme + 1] == "string delimiter" and types[lineNumber][visibleLexeme + 2] == "YARN literal" and types[lineNumber][visibleLexeme + 3] == "string delimiter"):
        #print(lexemes[lineNumber][visibleLexeme + 2])
        console.insert(END, str(lexemes[lineNumber][visibleLexeme + 2]) + "\n")
        console.config(state=DISABLED)
        return "OK"
    elif(lexemes[lineNumber][visibleLexeme + 1] in expressionKeywords["arithmetic"] or lexemes[lineNumber][visibleLexeme + 1] in expressionKeywords["boolean"] or lexemes[lineNumber][visibleLexeme + 1] in expressionKeywords["comparison"] or lexemes[lineNumber][visibleLexeme + 1] in expressionKeywords["concatenation"]):
        if (lexemes[lineNumber][visibleLexeme + 1] in expressionKeywords["arithmetic"]):
            semanticError = arithmeticExpressionSemantics(lineNumber, "IT")
        # if (lexemes[lineNumber][visibleLexeme + 1] in expressionKeywords["boolean"]):
        #     semanticError = expressionSemantics(lineNumber, "IT")
        if (lexemes[lineNumber][visibleLexeme + 1] in expressionKeywords["comparison"]):
            semanticError = comparisonExpressionSemantics(lineNumber, "IT")
        if (lexemes[lineNumber][visibleLexeme + 1] in expressionKeywords["concatenation"]):
            semanticError = concatenationExpressionSemantics(lineNumber, "IT")

        if(semanticError != "OK"):
            return semanticError
            
        #print(newSymbolTable['IT'][0])
        console.insert(END, str(newSymbolTable['IT'][0]) + "\n")
        console.config(state=DISABLED)
        return "OK"

    return "[Line " + str(lineNumber) + "] SemanticError: identifier not found"
    
def gimmehSemantics(lineNumber):
    gimmehLexeme = lexemes[lineNumber].index("GIMMEH")

    semanticsError = updateSymbolTable(lineNumber, [getInput(), "YARN literal"], lexemes[lineNumber][gimmehLexeme + 1])

    inputBox.delete(0, END)
    inputBox.config(state=DISABLED)
    enterButton.config(state=DISABLED)

    if(semanticsError != "OK"):
        return semanticsError

    return "OK"

def semantics():
    lineNumber = list(lexemes.keys())[0]
    lexemeIndex = 0

    while(lineNumber):
        if(lexemes[lineNumber][lexemeIndex] == "I HAS A"):
            semanticsError = iHasASemantics(lineNumber)

            if(semanticsError != "OK"):
                return semanticsError
            
            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "VISIBLE"):
            semanticsError = visibleSemantics(lineNumber)

            if(semanticsError != "OK"):
                return semanticsError

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "GIMMEH"):
            gimmehSemantics(lineNumber)
            
            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "WTF?"):
            semanticsError = switchCaseSemantics(lineNumber, "IT")      # Returns a line number

            # print(type(lineNumber))
            if (type(semanticsError) != int):
                print(semanticsError)
                break

            lineNumber = nextLineNumber(semanticsError)
            continue
        elif (types[lineNumber][lexemeIndex] == "identifier"):
            if newSymbolTable.get(lexemes[lineNumber][lexemeIndex]):
                newSymbolTable["IT"] = [newSymbolTable[lexemes[lineNumber][lexemeIndex]][0], newSymbolTable[lexemes[lineNumber][lexemeIndex]][1]]
                continue
            else:
                print("[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier")

                lineNumber = nextLineNumber(lineNumber)
                continue

        # * GO NEXT LINE
        else:
            lineNumber = nextLineNumber(lineNumber)
            continue
    
    return newSymbolTable

# MAIN
#MAIN
screen = Tk()
screen.title('LOLCODE Interpreter')
screen.geometry("1200x750")
screen.configure(bg=BACKGROUND_COLOR)
screen.resizable(False, False)

style = ttk.Style()
style.theme_use('vista')

fileButton = ttk.Button(
    screen,
    text='Open File',
    command=lambda:openFile()
)
fileButton.place(x=20, y=15)

textEditor = scrolledtext.ScrolledText(screen, undo=True, height=20, width=52)
# textEditor = Text(screen, height=20, width=54, state=DISABLED)
textEditor.place(x=20, y=40)


tokensLabel = ttk.Label(screen, text="Tokens", background=BACKGROUND_COLOR)
tokensLabel.place(x=470, y=20)
listOfTokens = Listbox(screen, height=20, width=53)
listOfTokens.place(x=470, y=40)

symbolTableLabel = ttk.Label(screen, text="Symbol Table", background=BACKGROUND_COLOR)
symbolTableLabel.place(x=855, y=20)
listOfSymbolTable = Listbox(screen, height=20, width=60, state=DISABLED)
listOfSymbolTable.place(x=845, y=40)

console = scrolledtext.ScrolledText(screen, height=18, width=142, state=DISABLED)
console.place(x=21, y=380)

inputBox = Entry(screen, width=180, state=DISABLED)
inputBox.place(x=21, y=670)

enterClicked = StringVar()
enterButton = ttk.Button(
    screen,
    text='Enter',
    state=DISABLED,
    command=lambda:saveInput()
)
enterButton.place(x=1100, y=667)

runButton = ttk.Button(
    screen,
    text='Run',
    command=lambda:run()
)
runButton.place(x=1100, y=715)

tokensTree = ttk.Treeview(listOfTokens, column=("c1", "c2"), show='headings', height=15)

scrollBarTokens = ttk.Scrollbar(listOfTokens, orient ="vertical", command = tokensTree.yview)
scrollBarTokens.pack(side = RIGHT, fill = Y)

tokensTree.pack(side=LEFT)

tokensTree.configure(yscrollcommand = scrollBarTokens.set)
tokensTree.column("# 1", anchor=CENTER, width=170)
tokensTree.heading("# 1", text="Lexeme")
tokensTree.column("# 2", anchor=CENTER, width=170)
tokensTree.heading("# 2", text="Type")

symbolTableTree = ttk.Treeview(listOfSymbolTable, column=("c1", "c2", "c3"), show='headings', height=15)

scrollBarSymbolTable = ttk.Scrollbar(listOfSymbolTable, orient ="vertical", command = symbolTableTree.yview)
scrollBarSymbolTable.pack(side = RIGHT, fill = Y)

symbolTableTree.pack(side=LEFT)

symbolTableTree.configure(yscrollcommand = scrollBarSymbolTable.set)
symbolTableTree.column("# 1", anchor=CENTER, width=102)
symbolTableTree.heading("# 1", text="Identifier")
symbolTableTree.column("# 2", anchor=CENTER, width=102)
symbolTableTree.heading("# 2", text="Value")
symbolTableTree.column("# 3", anchor=CENTER, width=102)
symbolTableTree.heading("# 3", text="Type")

screen.mainloop()
        
        
