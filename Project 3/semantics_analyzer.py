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

while(True):
    #print(lexemes[i])
    if(lexemes[lineNumber][lexemeIndex] == "I HAS A"):
        if("ITZ" in lexemes[lineNumber]):
            if(types[lineNumber][lexemeIndex + 3] in literals):
                if(newSymbolTable.get(lexemes[lineNumber][lexemeIndex + 1])):
                    break
                else: #check first if numbr
                    newSymbolTable[lexemes[lineNumber][lexemeIndex + 1]] = int(lexemes[lineNumber][lexemeIndex + 3])
                    break
            else:
                break
    lineNumber = nextLineNumber(lineNumber)
            
print(newSymbolTable)
        
        
