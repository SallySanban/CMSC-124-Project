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

def nextLineNumber(lineNumber):
    found = False

    for i in types.keys():
        if(i == lineNumber):
            found = True
            continue
        
        if(found):
            return i

lineNumber = list(lexemes.keys())[0]
lexemeIndex = 0

while(lineNumber):
    if(lexemes[lineNumber][lexemeIndex] == "I HAS A"):
        if("ITZ" in lexemes[lineNumber]):
            
            # * TYPE LITERALS
            if(types[lineNumber][lexemeIndex + 3] in literals or types[lineNumber][lexemeIndex + 3] == "string delimiter"):
                if(newSymbolTable.get(lexemes[lineNumber][lexemeIndex + 1])):
                    # TODO: If the identifier is existing, check if implicitly typecasted or not first before updating value
                    break
                else: #check first if numbr
                    if (types[lineNumber][lexemeIndex + 3] == "NUMBR literal"):
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [int(lexemes[lineNumber][lexemeIndex + 3]), types[lineNumber][lexemeIndex + 3]]
                    elif (types[lineNumber][lexemeIndex + 3] == "NUMBAR literal"):
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [float(lexemes[lineNumber][lexemeIndex + 3]), types[lineNumber][lexemeIndex + 3]]
                    elif (types[lineNumber][lexemeIndex + 3] == "string delimiter"):        # YARN literal
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [lexemes[lineNumber][lexemeIndex + 4], types[lineNumber][lexemeIndex + 4]]
                    elif (types[lineNumber][lexemeIndex + 3] == "TROOF literal"):
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [True if lexemes[lineNumber][lexemeIndex + 3] == "WIN" else False, types[lineNumber][lexemeIndex + 3]]
                    else:
                        # ! type is TYPE literal or "NOOB"
                        # Change this 
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [lexemes[lineNumber][lexemeIndex + 3], types[lineNumber][lexemeIndex + 3]]
                        
            # * OPERATIONS   
            else:
                operatorCount = 0    

                # * Gets the index of ITZ
                itzIndex = lexemes[lineNumber].index("ITZ")        
                
                # * Counts the number of operations in the arithmetic expression
                for typeLiteral in ['add operator', 'subtract operator', 'multiply operator', 'divide operator', 'modulo operator']:
                    operatorCount += types[lineNumber].count(typeLiteral)
                
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
                        if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])):         # Existing Identifier
                            # ! Check type
                            if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                                tempVal = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0], "NUMBR literal"]
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                                tempVal = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0], "NUMBAR literal"]
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
                                try:
                                    tempVal = [int(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                                except ValueError:
                                    try:
                                        tempVal = [float(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                                    except ValueError:
                                        print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                        break
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                                if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]):
                                    tempVal = [1, "NUMBR literal"]
                                else:
                                    tempVal = [0, "NUMBR literal"]
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
                                print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                break

                            # * 2nd N
                            if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])): # Existing Identifier
                                break
                                temp = 0
                                # ! Check type
                                if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "NUMBR literal"):
                                    temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0], "NUMBR literal"]
                                elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "NUMBAR literal"):
                                    temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0], "NUMBAR literal"]
                                elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "YARN literal"):
                                    try:
                                        temp = [int(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                                    except ValueError:
                                        try:
                                            temp = [float(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0]), "NUMBAR literal"]
                                        except ValueError:
                                            print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                            break
                                elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "TROOF literal"):
                                    if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0]):
                                        if (tempVal[1] == "NUMBR literal"):
                                            temp = [1, "NUMBR literal"]
                                        else:
                                            temp = [1.0, "NUMBAR literal"]
                                    else:
                                        if (tempVal[1] == "NUMBR literal"):
                                            temp = [0, "NUMBR literal"]
                                        else:
                                            temp = [0.0, "NUMBAR literal"]
                                elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "TYPE literal"):
                                    print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                    break

                                if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                    tempVal[0] += temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                    tempVal[0] -= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                    tempVal[0] *= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                    tempVal[0] /= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
                                    tempVal[0] %= temp[0]
                            else:           # * Literal
                                if (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "identifier"):
                                    print(f"Line {lineNumber} Semantic Error: Uninitialized variable used in arithmetic expression")
                                    break
                                # ! Check type
                                temp = 0
                                if (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "NUMBR literal"):
                                    temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                                elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "NUMBAR literal"):
                                    temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBAR literal"]
                                elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "YARN literal"):
                                    try:
                                        temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                                    except ValueError:
                                        try:
                                            temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                                        except ValueError:
                                            print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                            break
                                elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "TROOF literal"):
                                    if (lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2] == "WIN"):
                                        if (tempVal[1] == "NUMBR literal"):
                                            temp = [1, "NUMBR literal"]
                                        else:
                                            temp = [1.0, "NUMBAR literal"]
                                    else:
                                        if (tempVal[1] == "NUMBR literal"):
                                            temp = [0, "NUMBR literal"]
                                        else:
                                            temp = [0.0, "NUMBAR literal"]
                                elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "TYPE literal"):
                                    print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                    break


                                if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                    tempVal[0] += temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                    tempVal[0] -= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                    tempVal[0] *= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                    tempVal[0] /= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
                                    tempVal[0] %= temp[0]

                        # * 1st N
                        else:           # * Literal
                            if (types[lineNumber][itzIndex + operatorCount + tempCount] == "identifier"):
                                print(f"Line {lineNumber} Semantic Error: Uninitialized variable used in arithmetic expression")
                                break

                            # ! Check type
                            if (types[lineNumber][itzIndex + operatorCount + tempCount] == "NUMBR literal"):
                                tempVal = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBR literal"]
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "NUMBAR literal"):
                                tempVal = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBAR literal"]
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "YARN literal"):
                                try:
                                    tempVal = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBR literal"]
                                except ValueError:
                                    try:
                                        tempVal = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBR literal"]
                                    except ValueError:
                                        print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                        break
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "TROOF literal"):
                                if (lexemes[lineNumber][itzIndex + operatorCount + tempCount] == "WIN"):
                                    tempVal = [1, "NUMBR literal"]
                                else:
                                    tempVal = [0, "NUMBR literal"]
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "TYPE literal"):
                                print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                break
                            
                            # * 2nd N
                            if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])): # Existing Identifier
                                temp = 0
                                # ! Check type
                                if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "NUMBR literal"):
                                    temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0], "NUMBR literal"]
                                elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "NUMBAR literal"):
                                    temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0], "NUMBAR literal"]
                                elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "YARN literal"):
                                    try:
                                        temp = [int(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                                    except ValueError:
                                        try:
                                            temp = [float(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                                        except ValueError:
                                            print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                            break
                                elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "TROOF literal"):
                                    if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0]):
                                        if (tempVal[1] == "NUMBR literal"):
                                            temp = [1, "NUMBR literal"]
                                        else:
                                            temp = [1.0, "NUMBAR literal"]
                                    else:
                                        if (tempVal[1] == "NUMBR literal"):
                                            temp = [0, "NUMBR literal"]
                                        else:
                                            temp = [0.0, "NUMBAR literal"]
                                elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "TYPE literal"):
                                    print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                    break
                                
                                if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                    tempVal[0] += temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                    tempVal[0] -= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                    tempVal[0] *= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                    tempVal[0] /= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
                                    tempVal[0] %= temp[0]
                            else:           # * Literal
                                if (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "identifier"):
                                    print(f"Line {lineNumber} Semantic Error: Uninitialized variable used in arithmetic expression")
                                    break

                                # ! Check type
                                temp = 0
                                if (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "NUMBR literal"):
                                    temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                                elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "NUMBAR literal"):
                                    temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBAR literal"]
                                elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "YARN literal"):
                                    try:
                                        temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                                    except ValueError:
                                        try:
                                            temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                                        except ValueError:
                                            print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                            break
                                elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "TROOF literal"):
                                    if (lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2] == "WIN"):
                                        if (tempVal[1] == "NUMBR literal"):
                                            temp = [1, "NUMBR literal"]
                                        else:
                                            temp = [1.0, "NUMBAR literal"]
                                    else:
                                        if (tempVal[1] == "NUMBR literal"):
                                            temp = [0, "NUMBR literal"]
                                        else:
                                            temp = [0.0, "NUMBAR literal"]
                                elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "TYPE literal"):
                                    print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                    break


                                if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                    tempVal[0] += temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                    tempVal[0] -= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                    tempVal[0] *= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                    tempVal[0] /= temp[0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
                                    tempVal[0] %= temp[0]


                        operatorCount -= 1
                        tempCount += 5
                        continue
                    else:   # * More nested expressions
                        # ! Check type 
                        temp = 0

                        if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])): # Existing Identifier
                            temp = 0
                            # ! Check type
                            if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                                temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0], "NUMBR literal"]
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                                temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0], "NUMBAR literal"]
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
                                try:
                                    temp = [int(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                                except ValueError:
                                    try:
                                        temp = [float(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                                    except ValueError:
                                        print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                        break
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                                if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]):
                                    if (tempVal[1] == "NUMBR literal"):
                                        temp = [1, "NUMBR literal"]
                                    else:
                                        temp = [1.0, "NUMBAR literal"]
                                else:
                                    if (tempVal[1] == "NUMBR literal"):
                                        temp = [0, "NUMBR literal"]
                                    else:
                                        temp = [0.0, "NUMBAR literal"]
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
                                print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                break

                            if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                tempVal[0] += temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                tempVal[0] -= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                tempVal[0] *= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                tempVal[0] /= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
                                tempVal[0] %= temp[0]
                        else:           # * Literal
                            print(f"Line {lineNumber} Semantic Error: Invalid number")
                            break
                            
                            # ! Check type
                            temp = 0
                            if (types[lineNumber][itzIndex + operatorCount + tempCount] == "NUMBR literal"):
                                temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBR literal"]
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "NUMBAR literal"):
                                temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBAR literal"]
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "YARN literal"):
                                try:
                                    temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBR literal"]
                                except ValueError:
                                    try:
                                        temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBR literal"]
                                    except ValueError:
                                        print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                        break
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "TROOF literal"):
                                if (lexemes[lineNumber][itzIndex + operatorCount + tempCount] == "WIN"):
                                    if (tempVal[1] == "NUMBR literal"):
                                        temp = [1, "NUMBR literal"]
                                    else:
                                        temp = [1.0, "NUMBAR literal"]
                                else:
                                    if (tempVal[1] == "NUMBR literal"):
                                        temp = [0, "NUMBR literal"]
                                    else:
                                        temp = [0.0, "NUMBAR literal"]
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "TYPE literal"):
                                print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                break


                            if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                tempVal[0] += temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                tempVal[0] -= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                tempVal[0] *= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                tempVal[0] /= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
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
                    if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])):         # Existing Identifier
                        # ! Check type
                        if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                            tempVal = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0], "NUMBR literal"]
                        elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                            tempVal = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0], "NUMBAR literal"]
                        elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
                            try:
                                tempVal = [int(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                            except ValueError:
                                try:
                                    tempVal = [float(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                                except ValueError:
                                    print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                    break
                        elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                            if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]):
                                tempVal = [1, "NUMBR literal"]
                            else:
                                tempVal = [0, "NUMBR literal"]
                        elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
                            print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                            break

                        # * 2nd N
                        if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])): # Existing Identifier
                            temp = 0
                            # ! Check type
                            if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "NUMBR literal"):
                                temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0], "NUMBR literal"]
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "NUMBAR literal"):
                                temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0], "NUMBAR literal"]
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "YARN literal"):
                                try:
                                    temp = [int(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                                except ValueError:
                                    try:
                                        temp = [float(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0]), "NUMBR literal"]
                                    except ValueError:
                                        print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                        break
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "TROOF literal"):
                                if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][0]):
                                    if (tempVal[1] == "NUMBR literal"):
                                        temp = [1, "NUMBR literal"]
                                    else:
                                        temp = [1.0, "NUMBAR literal"]
                                else:
                                    if (tempVal[1] == "NUMBR literal"):
                                        temp = [0, "NUMBR literal"]
                                    else:
                                        temp = [0.0, "NUMBAR literal"]
                            elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]][1] == "TYPE literal"):
                                print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                break

                            if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                tempVal[0] += temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                tempVal[0] -= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                tempVal[0] *= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                tempVal[0] /= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
                                tempVal[0] %= temp[0]
                        else:           # * Literal
                            if (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "identifier"):
                                print(f"Line {lineNumber} Semantic Error: Uninitialized variable used in arithmetic expression")
                                break
                            # ! Check type
                            temp = 0
                            if (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "NUMBR literal"):
                                temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "NUMBAR literal"):
                                temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBAR literal"]
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "YARN literal"):
                                try:
                                    temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                                except ValueError:
                                    try:
                                        temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2]), "NUMBR literal"]
                                    except ValueError:
                                        print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "TROOF literal"):
                                if (lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2] == "WIN"):
                                    if (tempVal[1] == "NUMBR literal"):
                                        temp = [1, "NUMBR literal"]
                                    else:
                                        temp = [1.0, "NUMBAR literal"]
                                else:
                                    if (tempVal[1] == "NUMBR literal"):
                                        temp = [0, "NUMBR literal"]
                                    else:
                                        temp = [0.0, "NUMBAR literal"]
                            elif (types[lineNumber][itzIndex + operatorCount + tempCount + 2] == "TYPE literal"):
                                print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                                break


                            if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                tempVal[0] += temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                tempVal[0] -= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                tempVal[0] *= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                tempVal[0] /= temp[0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
                                tempVal[0] %= temp[0]

                    break
                else:     
                    temp = 0

                    if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])): # Existing Identifier
                        temp = 0
                        # ! Check type
                        if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                            temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0], "NUMBR literal"]
                        elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                            temp = [newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0], "NUMBAR literal"]
                        elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
                            try:
                                temp = [int(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                            except ValueError:
                                try:
                                    temp = [float(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]), "NUMBR literal"]
                                except ValueError:
                                    print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                    break
                        elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                            if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]):
                                if (tempVal[1] == "NUMBR literal"):
                                    temp = [1, "NUMBR literal"]
                                else:
                                    temp = [1.0, "NUMBAR literal"]
                            else:
                                if (tempVal[1] == "NUMBR literal"):
                                    temp = [0, "NUMBR literal"]
                                else:
                                    temp = [0.0, "NUMBAR literal"]
                        elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
                            print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                            break

                        if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                            tempVal[0] += temp[0]
                        elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                            tempVal[0] -= temp[0]
                        elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                            tempVal[0] *= temp[0]
                        elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                            tempVal[0] /= temp[0]
                        elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
                            tempVal[0] %= temp[0]
                    else:           # * Literal
                        if (types[lineNumber][itzIndex + operatorCount + tempCount] == "identifier"):
                            print(f"Line {lineNumber} Semantic Error: Uninitialized variable used in arithmetic expression")
                            break
                        
                        # ! Check type
                        temp = 0
                        if (types[lineNumber][itzIndex + operatorCount + tempCount] == "NUMBR literal"):
                            temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBR literal"]
                        elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "NUMBAR literal"):
                            temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBAR literal"]
                        elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "YARN literal"):
                            try:
                                temp = [int(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBR literal"]
                            except ValueError:
                                try:
                                    temp = [float(lexemes[lineNumber][itzIndex + operatorCount + tempCount]), "NUMBR literal"]
                                except ValueError:
                                    print(f"Line {lineNumber} Semantic Error: YARN literal cannot be converted to NUMBR or NUMBAR literal")
                                    break
                        elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "TROOF literal"):
                            if (lexemes[lineNumber][itzIndex + operatorCount + tempCount] == "WIN"):
                                if (tempVal[1] == "NUMBR literal"):
                                    temp = [1, "NUMBR literal"]
                                else:
                                    temp = [1.0, "NUMBAR literal"]
                            else:
                                if (tempVal[1] == "NUMBR literal"):
                                    temp = [0, "NUMBR literal"]
                                else:
                                    temp = [0.0, "NUMBAR literal"]
                        elif (types[lineNumber][itzIndex + operatorCount + tempCount] == "TYPE literal"):
                            print(f"Line {lineNumber} Semantic Error: NOOB type literal cannot be implicitly casted to NUMBR or NUMBAR literal")
                            break


                        if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                            tempVal[0] += temp[0]
                        elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                            tempVal[0] -= temp[0]
                        elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                            tempVal[0] *= temp[0]
                        elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                            tempVal[0] /= temp[0]
                        elif (types[lineNumber][itzIndex + operatorCount] == "modulo operator"):
                            tempVal[0] %= temp[0]

                # * STORES THE FINAL VALUE OF TEMP HERE
                newSymbolTable[lexemes[lineNumber][1]] = [tempVal[0], tempVal[1]]

         # * FOUND NO ITZ keyword 
        else:      
            newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [None, "TYPE literal"]   # * No Value but initialized
    elif(lexemes[lineNumber][lexemeIndex] == "VISIBLE"):
        visibleIndex = lexemes[lineNumber].index("VISIBLE")


        # if types[lineNumber][lexemeIndex + 1] != "string delimiter":
        #     print(newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]][0])
        # else:
        #     print(lexemes[lineNumber][lexemeIndex + 2])
    elif(lexemes[lineNumber][lexemeIndex] == "GIMMEH"):
        print(f"variable: {newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]]} = ")
        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [input(), "YARN literal"]

        print(f"variable: {lexemes[lineNumber][lexemeIndex + 1]} = {newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]]}")

    # * GO NEXT LINE
    lineNumber = nextLineNumber(lineNumber)
            
print(newSymbolTable)
        
        
