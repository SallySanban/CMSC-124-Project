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
                # * If the identifier is existing
                if(newSymbolTable.get(lexemes[lineNumber][lexemeIndex + 1])):
                    # TODO: If the identifier is existing, check if implicitly typecasted or not first before updating value
                    break
                # * 
                else:           # Check nested
                    itzIndex = lexemes[lineNumber].index("ITZ")
                    
                    for typeLiteral in ['add operator', 'subtract operator', 'multiply operator', 'divide operator']:
                        operatorCount += types[lineNumber].count(typeLiteral)
                    
                    # Flow: Start sa innermost to outermost
                        # first operator appears +n from ITZ
                    
                    # I HAS A sum ITZ SUM OF DIFF OF num AN 13 AN 21
                    # I HAS A sum ITZ SUM OF DIFF OF PRODUKT OF num AN 13 AN 21 AN 4
                        # Implicit typecasting for troof, 
                    tempVal = 0
                    tempCount = 1
                    boolNested = False
                    while operatorCount > 1:
                        boolNested = True
                        if tempCount == 1:          # Innermost operation
                            # * 1st N
                            if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])):         # Existing Identifier
                                # ! ASSUME FIRST THAT ALL VALUES ARE INTEGERS

                                tempVal = newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
                                # print(tempVal)

                                # * 2nd N
                                if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])): # Existing Identifier
                                    if (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "add operator"):
                                        tempVal += newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
                                    elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "subtract operator"):
                                        tempVal -= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
                                    elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "multiply operator"):
                                        tempVal *= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
                                    elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "divide operator"):
                                        tempVal /= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
                                else:           # Literal
                                    # ! FOR TYPECASTING
                                    # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
                                    if (types[lineNumber][itzIndex + operatorCount + tempCount + 2] in literals or types[lineNumber][itzIndex + operatorCount + tempCount + 2] in ["string delimiter"]):
                                        if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                            # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
                                            tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
                                        elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                            tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
                                        elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                            tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
                                        elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                            tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
                                        # print(tempVal)
                                    else:
                                        print(types[lineNumber][itzIndex + operatorCount + tempCount])
                                        print("Semantics Error: Invalid type for arithmetic operation")
                                        break
                                    # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
                            # * 1st N
                            else:           # Literal
                                if (types[lineNumber][itzIndex + operatorCount + tempCount] in literals or types[lineNumber][itzIndex + operatorCount + tempCount] == "string delimiter"):
                                    tempVal = lexemes[lineNumber][itzIndex + operatorCount + tempCount]
                                
                                    # ! FOR TYPECASTING
                                    # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
                                    # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
                            operatorCount -= 1
                            tempCount += 5
                            continue
                        else: # More nested 
                            if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])):     # Existing identifier
                                if (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "add operator"):
                                    tempVal += newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "subtract operator"):
                                    tempVal -= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "multiply operator"):
                                    tempVal *= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "divide operator"):
                                    tempVal /= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                            else:               # Literal or NOOB identifier
                                if (types[lineNumber][itzIndex + operatorCount + tempCount] in literals or types[lineNumber][itzIndex + operatorCount + tempCount + 2] in ["string delimiter"]):
                                    if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                        # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
                                        tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                    elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                        tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                    elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                        tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                    elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                        tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                else:
                                    print(types[lineNumber][itzIndex + operatorCount + tempCount])
                                    print("Semantics Error: Invalid type for arithmetic operation")
                                    break
                                # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                                # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                                # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                                # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
                                # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):

                        operatorCount -= 1
                        tempCount += 3
                    
                    # * ONLY REACHES HERE IF THIS IS THE OUTERMOST OPERATION
                    # I HAS A sum ITZ SUM OF num AN 13                                  # 3
                    # I HAS A sum ITZ SUM OF DIFF OF num AN 13 AN 21                        # 6
                    # I HAS A sum ITZ SUM OF DIFF OF PRODUKT OF num AN 13 AN 21 AN 4            # 9
                    # I HAS A sum ITZ SUM OF DIFF OF PRODUKT OF SUM OF num AN 13 AN 21 AN 4 AN 11   # 12

                    if (not boolNested):          # ! SINGLE OPERATION
                        # * 1ST N
                        if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + 1])):     # Existing identifier
                            tempVal = newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]

                            # * 2ND N
                            if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + 3])):     # Existing identifier
                                if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                    tempVal += newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                    tempVal -= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                    tempVal *= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]
                                elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                    tempVal /= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]
                            else:
                                if (types[lineNumber][itzIndex + operatorCount + 3] in literals or types[lineNumber][itzIndex + operatorCount + 3] in ["string delimiter"]):
                                    if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                        # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
                                        tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + 3])
                                    elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                        tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
                                    elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                        tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
                                    elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                        tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
                                else:
                                    print(types[lineNumber][itzIndex + operatorCount + tempCount])
                                    print("Semantics Error: Invalid type for arithmetic operation")
                                    break
                        else:               # Literal or NOOB identifier
                            # * 1ST N
                            if (types[lineNumber][itzIndex + operatorCount + 1] in literals or types[lineNumber][itzIndex + operatorCount + 1 + 2] in ["string delimiter"]):
                                # TYPE CAST HERE
                                tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + 1])
                                
                                # * 2ND N
                                if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + 3])):     # Existing identifier
                                    if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                        tempVal += newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 3]][0]
                                    elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                        tempVal -= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 3]][0]
                                    elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                        tempVal *= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 3]][0]
                                    elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                        tempVal /= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 3]][0]
                                else:
                                    if (types[lineNumber][itzIndex + operatorCount + 3] in literals or types[lineNumber][itzIndex + operatorCount + 3] in ["string delimiter"]):
                                        if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                            # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
                                            tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + 3])
                                        elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                            tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
                                        elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                            tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
                                        elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                            tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
                                    else:
                                        print(types[lineNumber][itzIndex + operatorCount + tempCount])
                                        print("Semantics Error: Invalid type for arithmetic operation")
                                        break
                            else:
                                print(types[lineNumber][itzIndex + operatorCount + tempCount])
                                print("Semantics Error: Invalid type for arithmetic operation")
                                break
                    else:
                        if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])):     # Existing identifier
                            if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                tempVal += newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                tempVal -= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                tempVal *= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
                            elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                tempVal /= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
                        else:               # Literal or NOOB identifier
                            if (types[lineNumber][itzIndex + operatorCount + tempCount] in literals or types[lineNumber][itzIndex + operatorCount + tempCount + 2] in ["string delimiter"]):
                                if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
                                    # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
                                    # print(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0])
                                    tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
                                    tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
                                    tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                                elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
                                    tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
                            else:
                                print(types[lineNumber][itzIndex + operatorCount + tempCount])
                                print("Semantics Error: Invalid type for arithmetic operation")
                                break
                            # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
                            # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
                            # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
                            # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
                            # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):

                    # * STORES THE FINAL VALUE OF TEMP HERE
                    print(tempVal)          # ! WORKING RIGHT NOW BUT NOT single operation
                    newSymbolTable[lexemes[lineNumber][1]] = [tempVal, "NUMBR literal"]
                        # print(lexemes[lineNumber][itzIndex + operatorCount])
                        # print(lexemes[lineNumber][itzIndex + operatorCount + tempCount])

         # * FOUND NO ITZ keyword 
        else:      
            newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [None, "TYPE literal"]
    # elif(lexemes[lineNumber][lexemeIndex] == "VISIBLE"):
        # if types[lineNumber][lexemeIndex + 1] != "string delimiter":
        #     print(newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]][0])
        # else:
        #     print(lexemes[lineNumber][lexemeIndex + 2])

    # * NO ASSIGNMENT, GO NEXT LINE
    lineNumber = nextLineNumber(lineNumber)
            
print(newSymbolTable)
        
        
