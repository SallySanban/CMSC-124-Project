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
    if(value == None):
        newSymbolTable[variable] = [None, "NOOB"]
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

def expressionSemantics(lineNumber, keywordIndex, variable):
    

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
            expressionSemantics(lineNumber, itzLexeme + 1, lexemes[lineNumber][itzLexeme - 1])
            return "Done"
    else:   #variable has no value
        iHasALexeme = lexemes[lineNumber].index("I HAS A")

        semanticsError = updateSymbolTable(lineNumber, None, lexemes[lineNumber][iHasALexeme + 1])

        if(semanticsError != "OK"):
            return semanticsError

    return "OK"

def visibleSemantics(lineNumber):
    visibleLexeme = lexemes[lineNumber].index("VISIBLE")

    #doesnt catch when more than one arity
    for i in newSymbolTable.keys():
        if(i == lexemes[lineNumber][visibleLexeme + 1]):
            print(newSymbolTable[i])
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

for i in newSymbolTable.keys():         
    print(str(i) + ": " + str(newSymbolTable[i]))
        
        
