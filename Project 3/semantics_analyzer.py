import lexical_analyzer

types = lexical_analyzer.getType()
lexemes = lexical_analyzer.getLexemes()
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
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBR literal"):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][0] == int(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBAR literal"):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0] == float(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
            elif types[lineNumber][expressionIndex + 2] == "NUMBR literal": # x = NUMBR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (int(lexemes[lineNumber][expressionIndex + 2]) == newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                    return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
            elif types[lineNumber][expressionIndex + 2] == "NUMBAR literal":    # x = NUMBAR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (float(lexemes[lineNumber][expressionIndex + 2]) == newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                    return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
            else:
                return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
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
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBR literal"):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][0] != int(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                        if (newSymbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBAR literal"):
                            if (newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0] != float(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
            elif types[lineNumber][expressionIndex + 2] == "NUMBR literal": # x = NUMBR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (int(lexemes[lineNumber][expressionIndex + 2]) != newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                    return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
            elif types[lineNumber][expressionIndex + 2] == "NUMBAR literal":    # x = NUMBAR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if newSymbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (float(lexemes[lineNumber][expressionIndex + 2]) != newSymbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                    return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
            else:
                return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"

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
                                return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] <= int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0] <= float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) <= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) <= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
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
                                return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] >= int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0] >= float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) >= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) >= newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
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
                                return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] > int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0] > float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) > newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) > newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
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
                                return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][0] < int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (newSymbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0] < float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticsError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) < newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if newSymbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) < newSymbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
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
                        return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticsError: Invalid operands for comparison operation"


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
    
    print(lexemes[lineNumber][expressionIndex])
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
                    return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
            else:
                tempVal += str(lexemes[lineNumber][anIndices[counter] - 1])
            
            if (types[lineNumber][anIndices[counter] + 1] == "identifier"):
                if (newSymbolTable.get(lexemes[lineNumber][anIndices[counter] + 1])):
                    tempVal += str(newSymbolTable[lexemes[lineNumber][anIndices[counter] + 1]][0])
                else:
                    return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
            else:
                tempVal += str(lexemes[lineNumber][anIndices[counter] + 1])

            break
        
        if (types[lineNumber][anIndices[counter] - 1] == "identifier"):
            if (newSymbolTable.get(lexemes[lineNumber][anIndices[counter] - 1])):
                tempVal += str(newSymbolTable[lexemes[lineNumber][anIndices[counter] - 1]][0])
            else:
                return "[Line " + str(lineNumber) + "] SemanticsError: Uninitialized identifier"
        else:
            tempVal += str(lexemes[lineNumber][anIndices[counter] - 1])


        counter += 1
    
    # * STORES THE FINAL VALUE OF TEMP HERE
    if(variable != "IT"):
        variable = lexemes[lineNumber][1]
    
    tempVal = [tempVal, "YARN literal"]

    updateSymbolTable(lineNumber, [tempVal[0], tempVal[1]], variable)

    return "OK"
        

    



def iHasASemantics(lineNumber):
    if("variable initialization keyword" in types[lineNumber]): #variable has value
        itzLexeme = lexemes[lineNumber].index("ITZ")

        # TODO (Eikou): doesnt accept if assigns to variable

        if(types[lineNumber][itzLexeme + 1] in literals): #checks if value is literal
            semanticsError = updateSymbolTable(lineNumber, itzLexeme + 1, lexemes[lineNumber][itzLexeme - 1])

            if(semanticsError != "OK"):
                return semanticsError

        elif(types[lineNumber][itzLexeme + 1] == "string delimiter" and types[lineNumber][itzLexeme + 2] == "YARN literal" and types[lineNumber][itzLexeme + 3] == "string delimiter"): #checks if string
            semanticsError = updateSymbolTable(lineNumber, itzLexeme + 2, lexemes[lineNumber][itzLexeme - 1])

            if(semanticsError != "OK"):
                return semanticsError

        elif(lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["arithmetic"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["boolean"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["comparison"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["concatenation"]): #if expression
            semanticsError = expressionSemantics(lineNumber, lexemes[lineNumber][itzLexeme - 1])

            if(semanticsError != "OK"):
                return semanticsError

    else:   #variable has no value
        iHasALexeme = lexemes[lineNumber].index("I HAS A")

        semanticsError = updateSymbolTable(lineNumber, "NOOB", lexemes[lineNumber][iHasALexeme + 1])

        if(semanticsError != "OK"):
            return semanticsError

    return "OK"

def visibleSemantics(lineNumber):
    visibleLexeme = lexemes[lineNumber].index("VISIBLE")

    # TODO: doesnt catch when more than one arity
    if(types[lineNumber][visibleLexeme + 1] == "identifier"):
        for i in newSymbolTable.keys():
            if(i == lexemes[lineNumber][visibleLexeme + 1]):
                if(newSymbolTable[i][1] == "TROOF literal"):
                    if(newSymbolTable[i][0] == True):
                        print("WIN")
                    else:
                        print("FAIL")
                else:
                    print(newSymbolTable[i][0])
                return "OK"
    elif(types[lineNumber][visibleLexeme + 1] in literals):
        print(lexemes[lineNumber][visibleLexeme + 1])
        return "OK"
    elif(types[lineNumber][visibleLexeme + 1] == "string delimiter" and types[lineNumber][visibleLexeme + 2] == "YARN literal" and types[lineNumber][visibleLexeme + 3] == "string delimiter"):
        print(lexemes[lineNumber][visibleLexeme + 2])
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
            
        print(newSymbolTable['IT'][0])
        return "OK"

    return "[Line " + str(lineNumber) + "] SemanticError: identifier not found"
    
def gimmehSemantics(lineNumber):
    gimmehLexeme = lexemes[lineNumber].index("GIMMEH")

    semanticsError = updateSymbolTable(lineNumber, [input(), "YARN literal"], lexemes[lineNumber][gimmehLexeme + 1])

    if(semanticsError != "OK"):
        return semanticsError

    return "OK"

lineNumber = list(lexemes.keys())[0]
lexemeIndex = 0

while(lineNumber):
    if(lexemes[lineNumber][lexemeIndex] == "I HAS A"):
        semanticsError = iHasASemantics(lineNumber)

        if(semanticsError != "OK"):
            print(semanticsError)
            break
        
        lineNumber = nextLineNumber(lineNumber)
        continue
    elif(lexemes[lineNumber][lexemeIndex] == "VISIBLE"):
        semanticsError = visibleSemantics(lineNumber)

        if(semanticsError != "OK"):
            print(semanticsError)
            break

        lineNumber = nextLineNumber(lineNumber)
        continue
    elif(lexemes[lineNumber][lexemeIndex] == "GIMMEH"):
        gimmehSemantics(lineNumber)

        lineNumber = nextLineNumber(lineNumber)
        continue

    # * GO NEXT LINE
    else:
        lineNumber = nextLineNumber(lineNumber)
        continue

# print()
# for i in newSymbolTable.keys():         
#     print(str(i) + ": " + str(newSymbolTable[i]))
        
        
