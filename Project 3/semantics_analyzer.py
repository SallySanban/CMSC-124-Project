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
            if(types[lineNumber][lexemeIndex + 3] in literals or ["string delimiter"]):
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
                        # Change this 
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [lexemes[lineNumber][lexemeIndex + 3], types[lineNumber][lexemeIndex + 3]]
                    
            else:
                if(newSymbolTable.get(lexemes[lineNumber][lexemeIndex + 1])):
                    # TODO: If the identifier is existing, check if implicitly typecasted or not first before updating value
                    break
                else:           # Check nested
                    if (types[lineNumber][lexemeIndex + 3] == "NUMBR literal"):
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [int(lexemes[lineNumber][lexemeIndex + 3]), types[lineNumber][lexemeIndex + 3]]
                    elif (types[lineNumber][lexemeIndex + 3] == "NUMBAR literal"):
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [float(lexemes[lineNumber][lexemeIndex + 3]), types[lineNumber][lexemeIndex + 3]]
                    elif (types[lineNumber][lexemeIndex + 3] == "YARN literal"):
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [lexemes[lineNumber][lexemeIndex + 4], types[lineNumber][lexemeIndex + 4]]
                    elif (types[lineNumber][lexemeIndex + 3] == "TROOF literal"):
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [True if lexemes[lineNumber][lexemeIndex + 3] == "WIN" else False, types[lineNumber][lexemeIndex + 3]]
                    else:
                        newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [lexemes[lineNumber][lexemeIndex + 3], types[lineNumber][lexemeIndex + 3]]
        else:
            newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = [None, "NOOB"]
    lineNumber = nextLineNumber(lineNumber)
            
print(newSymbolTable)
        
        
