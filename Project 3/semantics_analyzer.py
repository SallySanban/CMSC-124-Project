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
def updateSymbolTable(lineNumber, valueIndex, variable):
    if(valueIndex == None):
        newSymbolTable[variable] = [None, "NOOB"]
    else:
        if(types[lineNumber][valueIndex] == "NUMBR literal"):  #value is numbr
            newSymbolTable[variable] = [int(lexemes[lineNumber][valueIndex]), "NUMBR literal"]
        elif(types[lineNumber][valueIndex] == "NUMBAR literal"):   #value is numbar
            newSymbolTable[variable] = [float(lexemes[lineNumber][valueIndex]), "NUMBAR literal"]
        elif(types[lineNumber][valueIndex] == "YARN literal"): #value is yarn
            newSymbolTable[variable] = [str(lexemes[lineNumber][valueIndex]), "YARN literal"]
        elif(types[lineNumber][valueIndex] == "TROOF literal"):    #value is troof
            if(lexemes[lineNumber][valueIndex] == "WIN"):
                newSymbolTable[variable] = [True, "TROOF literal"]
            elif(lexemes[lineNumber][valueIndex] == "FAIL"):
                newSymbolTable[variable] = [False, "TROOF literal"]
        else:   #value is type
            return "[Line " + str(lineNumber) + "] SemanticError: cannot store TYPE in identifier"
    
    return "OK"

def expressionSemantics(lineNumber, variable):
    return "OK"

def iHasASemantics(lineNumber):
    if("variable initialization keyword" in types[lineNumber]): #variable has value
        itzLexeme = lexemes[lineNumber].index("ITZ")

        if(types[lineNumber][itzLexeme + 1] in literals): #checks if value is literal
            semanticsError = updateSymbolTable(lineNumber, itzLexeme + 1, lexemes[lineNumber][itzLexeme - 1])

            if(semanticsError != "OK"):
                return semanticsError

        elif(types[lineNumber][itzLexeme + 1] == "string delimiter" and types[lineNumber][itzLexeme + 2] == "YARN literal" and types[lineNumber][itzLexeme + 3] == "string delimiter"): #checks if string
            semanticsError = updateSymbolTable(lineNumber, itzLexeme + 2, lexemes[lineNumber][itzLexeme - 1])

            if(semanticsError != "OK"):
                return semanticsError

        elif(lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["arithmetic"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["boolean"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["comparison"] or lexemes[lineNumber][itzLexeme + 1] in expressionKeywords["concatenation"]): #if expression
            newSymbolTable[lexemes[lineNumber][itzLexeme - 1]] = lexemes[lineNumber][itzLexeme + 1]
            expressionSemantics(lineNumber, lexemes[lineNumber][itzLexeme - 1])
    else:   #variable has no value
        iHasALexeme = lexemes[lineNumber].index("I HAS A")

        semanticsError = updateSymbolTable(lineNumber, None, lexemes[lineNumber][iHasALexeme + 1])

        if(semanticsError != "OK"):
            return semanticsError

    return "OK"

def visibleSemantics(lineNumber):
    print("owo")

lineNumber = list(lexemes.keys())[0]
lexemeIndex = 0

while(lineNumber):
    if(lexemes[lineNumber][lexemeIndex] == "I HAS A"):
        semanticsError = iHasASemantics(lineNumber)

        if(semanticsError != "OK"):
            print(semanticsError)
            break
        
        lineNumber = nextLineNumber(lineNumber)
    elif(lexemes[lineNumber][lexemeIndex] == "VISIBLE"):
        visibleSemantics(lineNumber)
            # * OPERATIONS   
            # else:
            #     operatorCount = 0
            #     # * If the identifier is existing
            #     if(newSymbolTable.get(lexemes[lineNumber][lexemeIndex + 1])):
            #         # TODO: If the identifier is existing, check if implicitly typecasted or not first before updating value
            #         break
            #     # * 
            #     else:           # Check nested
            #         itzIndex = lexemes[lineNumber].index("ITZ")
                    
            #         for typeLiteral in ['add operator', 'subtract operator', 'multiply operator', 'divide operator']:
            #             operatorCount += types[lineNumber].count(typeLiteral)
                    
                    # Flow: Start sa innermost to outermost
                        # first operator appears +n from ITZ
                    
                    # I HAS A sum ITZ SUM OF DIFF OF num AN 13 AN 21
                    # I HAS A sum ITZ SUM OF DIFF OF PRODUKT OF num AN 13 AN 21 AN 4
                        # Implicit typecasting for troof, 
        #             tempVal = 0
        #             tempCount = 1
        #             boolNested = False
        #             while operatorCount > 1:
        #                 boolNested = True
        #                 if tempCount == 1:          # Innermost operation
        #                     # * 1st N
        #                     if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])):         # Existing Identifier
        #                         # ! ASSUME FIRST THAT ALL VALUES ARE INTEGERS

        #                         tempVal = newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
        #                         # print(tempVal)

        #                         # * 2nd N
        #                         if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])): # Existing Identifier
        #                             if (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "add operator"):
        #                                 tempVal += newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
        #                             elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "subtract operator"):
        #                                 tempVal -= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
        #                             elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "multiply operator"):
        #                                 tempVal *= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
        #                             elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "divide operator"):
        #                                 tempVal /= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
        #                         else:           # Literal
        #                             # ! FOR TYPECASTING
        #                             # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
        #                             if (types[lineNumber][itzIndex + operatorCount + tempCount + 2] in literals or types[lineNumber][itzIndex + operatorCount + tempCount + 2] in ["string delimiter"]):
        #                                 if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
        #                                     # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
        #                                     tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
        #                                 elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
        #                                     tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
        #                                 elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
        #                                     tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
        #                                 elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
        #                                     tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount + 2])
        #                                 # print(tempVal)
        #                             else:
        #                                 print(types[lineNumber][itzIndex + operatorCount + tempCount])
        #                                 print("Semantics Error: Invalid type for arithmetic operation")
        #                                 break
        #                             # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
        #                     # * 1st N
        #                     else:           # Literal
        #                         if (types[lineNumber][itzIndex + operatorCount + tempCount] in literals or types[lineNumber][itzIndex + operatorCount + tempCount] == "string delimiter"):
        #                             tempVal = lexemes[lineNumber][itzIndex + operatorCount + tempCount]
                                
        #                             # ! FOR TYPECASTING
        #                             # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
        #                             # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):
        #                     operatorCount -= 1
        #                     tempCount += 5
        #                     continue
        #                 else: # More nested 
        #                     if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])):     # Existing identifier
        #                         if (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "add operator"):
        #                             tempVal += newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                         elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "subtract operator"):
        #                             tempVal -= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                         elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "multiply operator"):
        #                             tempVal *= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                         elif (newSymbolTable[type[lineNumber][itzIndex + operatorCount]] == "divide operator"):
        #                             tempVal /= newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                     else:               # Literal or NOOB identifier
        #                         if (types[lineNumber][itzIndex + operatorCount + tempCount] in literals or types[lineNumber][itzIndex + operatorCount + tempCount + 2] in ["string delimiter"]):
        #                             if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
        #                                 # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
        #                                 tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                             elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
        #                                 tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                             elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
        #                                 tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                             elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
        #                                 tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                         else:
        #                             print(types[lineNumber][itzIndex + operatorCount + tempCount])
        #                             print("Semantics Error: Invalid type for arithmetic operation")
        #                             break
        #                         # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
        #                         # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
        #                         # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
        #                         # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
        #                         # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):

        #                 operatorCount -= 1
        #                 tempCount += 3
                    
        #             # * ONLY REACHES HERE IF THIS IS THE OUTERMOST OPERATION
        #             # I HAS A sum ITZ SUM OF num AN 13                                  # 3
        #             # I HAS A sum ITZ SUM OF DIFF OF num AN 13 AN 21                        # 6
        #             # I HAS A sum ITZ SUM OF DIFF OF PRODUKT OF num AN 13 AN 21 AN 4            # 9
        #             # I HAS A sum ITZ SUM OF DIFF OF PRODUKT OF SUM OF num AN 13 AN 21 AN 4 AN 11   # 12

        #             if (not boolNested):          # ! SINGLE OPERATION
        #                 # * 1ST N
        #                 if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + 1])):     # Existing identifier
        #                     tempVal = newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]

        #                     # * 2ND N
        #                     if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + 3])):     # Existing identifier
        #                         if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
        #                             tempVal += newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]
        #                         elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
        #                             tempVal -= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]
        #                         elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
        #                             tempVal *= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]
        #                         elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
        #                             tempVal /= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 1]][0]
        #                     else:
        #                         if (types[lineNumber][itzIndex + operatorCount + 3] in literals or types[lineNumber][itzIndex + operatorCount + 3] in ["string delimiter"]):
        #                             if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
        #                                 # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
        #                                 tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + 3])
        #                             elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
        #                                 tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
        #                             elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
        #                                 tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
        #                             elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
        #                                 tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
        #                         else:
        #                             print(types[lineNumber][itzIndex + operatorCount + tempCount])
        #                             print("Semantics Error: Invalid type for arithmetic operation")
        #                             break
        #                 else:               # Literal or NOOB identifier
        #                     # * 1ST N
        #                     if (types[lineNumber][itzIndex + operatorCount + 1] in literals or types[lineNumber][itzIndex + operatorCount + 1 + 2] in ["string delimiter"]):
        #                         # TYPE CAST HERE
        #                         tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + 1])
                                
        #                         # * 2ND N
        #                         if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + 3])):     # Existing identifier
        #                             if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
        #                                 tempVal += newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 3]][0]
        #                             elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
        #                                 tempVal -= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 3]][0]
        #                             elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
        #                                 tempVal *= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 3]][0]
        #                             elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
        #                                 tempVal /= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + 3]][0]
        #                         else:
        #                             if (types[lineNumber][itzIndex + operatorCount + 3] in literals or types[lineNumber][itzIndex + operatorCount + 3] in ["string delimiter"]):
        #                                 if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
        #                                     # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
        #                                     tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + 3])
        #                                 elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
        #                                     tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
        #                                 elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
        #                                     tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
        #                                 elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
        #                                     tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + 3])
        #                             else:
        #                                 print(types[lineNumber][itzIndex + operatorCount + tempCount])
        #                                 print("Semantics Error: Invalid type for arithmetic operation")
        #                                 break
        #                     else:
        #                         print(types[lineNumber][itzIndex + operatorCount + tempCount])
        #                         print("Semantics Error: Invalid type for arithmetic operation")
        #                         break
        #             else:
        #                 if (newSymbolTable.get(lexemes[lineNumber][itzIndex + operatorCount + tempCount])):     # Existing identifier
        #                     if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
        #                         tempVal += newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
        #                     elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
        #                         tempVal -= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
        #                     elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
        #                         tempVal *= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
        #                     elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
        #                         tempVal /= newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0]
        #                 else:               # Literal or NOOB identifier
        #                     if (types[lineNumber][itzIndex + operatorCount + tempCount] in literals or types[lineNumber][itzIndex + operatorCount + tempCount + 2] in ["string delimiter"]):
        #                         if (types[lineNumber][itzIndex + operatorCount] == "add operator"):
        #                             # ! ASSUME THEY ARE ALL INTEGERS ! REMOVE TYPECAST
        #                             # print(newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][0])
        #                             tempVal += int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                         elif (types[lineNumber][itzIndex + operatorCount] == "subtract operator"):
        #                             tempVal -= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                         elif (types[lineNumber][itzIndex + operatorCount] == "multiply operator"):
        #                             tempVal *= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                         elif (types[lineNumber][itzIndex + operatorCount] == "divide operator"):
        #                             tempVal /= int(lexemes[lineNumber][itzIndex + operatorCount + tempCount])
        #                     else:
        #                         print(types[lineNumber][itzIndex + operatorCount + tempCount])
        #                         print("Semantics Error: Invalid type for arithmetic operation")
        #                         break
        #                     # if (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBR literal"):
        #                     # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "NUMBAR literal"):
        #                     # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TROOF literal"):
        #                     # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "YARN literal"):
        #                     # elif (newSymbolTable[lexemes[lineNumber][itzIndex + operatorCount + tempCount]][1] == "TYPE literal"):

        #             # * STORES THE FINAL VALUE OF TEMP HERE
        #             print(tempVal)          # ! WORKING RIGHT NOW BUT NOT single operation
        #             newSymbolTable[lexemes[lineNumber][1]] = [tempVal, "NUMBR literal"]
        #                 # print(lexemes[lineNumber][itzIndex + operatorCount])
        #                 # print(lexemes[lineNumber][itzIndex + operatorCount + tempCount])

        #  # * FOUND NO ITZ keyword 
        # else:      
        #     newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [None, "TYPE literal"]
    # elif(lexemes[lineNumber][lexemeIndex] == "VISIBLE"):
        # if types[lineNumber][lexemeIndex + 1] != "string delimiter":
        #     print(newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]][0])
        # else:
        #     print(lexemes[lineNumber][lexemeIndex + 2])

    # * NO ASSIGNMENT, GO NEXT LINE
    lineNumber = nextLineNumber(lineNumber)

for i in newSymbolTable.keys():         
    print(str(i) + ": " + str(newSymbolTable[i]))
        
        
