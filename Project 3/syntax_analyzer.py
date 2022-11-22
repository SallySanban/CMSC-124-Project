import lexical_analyzer

types = lexical_analyzer.getType()
lexemes = lexical_analyzer.getLexemes()
keywords = ["HAI",
            "KTHXBYE",
            "OBTW",
            "BTW",
            "TLDR",
            "I HAS A",
            "ITZ",
            "R",
            "SUM OF",
            "DIFF OF",
            "PRODUKT OF",
            "QUOSHUNT OF",
            "MOD OF",
            "BIGGR OF",
            "SMALLR OF",
            "BOTH OF",
            "EITHER OF",
            "WON OF",
            "NOT",
            "ANY OF",
            "ALL OF",
            "BOTH SAEM",
            "DIFFRINT",
            "SMOOSH",
            "MAEK",
            "A",
            "IS NOW A",
            "VISIBLE",
            "GIMMEH",
            "O RLY?",
            "YA RLY",
            "MEBBE",
            "NO WAI",
            "OIC",
            "WTF?",
            "OMG",
            "OMGWTF",
            "IM IN YR",
            "UPPIN",
            "NERFIN",
            "YR",
            "TIL",
            "WILE",
            "IM OUTTA YR",
            "GTFO",
            "AN",
            "MKAY"
            ]
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

def singleCommentSyntax(lineNumber):
    commentDelimiter = lexemes[lineNumber].index("BTW")

    if(commentDelimiter + 1 == len(types[lineNumber])):
        return "[Line " + str(lineNumber) + "] SyntaxError: no comment indicated"

    for i in range(commentDelimiter + 1, len(types[lineNumber])):
        if(types[lineNumber][i] != "comment"):
            return "[Line " + str(lineNumber) + "] SyntaxError: not a comment"

    return "OK"

def tldrSyntax(lineNumber):
    commentDelimiter = lexemes[lineNumber].index("TLDR")
    
    if(commentDelimiter != len(lexemes[lineNumber])-1):
        return "[Line " + str(lineNumber) + "] SyntaxError: TLDR cannot be together with other statements"

    return "OK"
        
def multiCommentSyntax(lineNumber):
    global commentFound
    start = 1
    comments = []

    if(lexemes[lineNumber][0] == "OBTW" and lexemes[lineNumber][len(lexemes[lineNumber])-1] == "TLDR"):
        return "[Line " + str(lineNumber) + "] SyntaxError: OBTW and TLDR must have their own lines"

    while(commentFound == True):
        for i in range(start, len(types[lineNumber])):
            if(lexemes[lineNumber][i] == "TLDR"):
                syntaxError = tldrSyntax(lineNumber)

                if(syntaxError != "OK"):
                    return syntaxError

                commentFound = False
                break

            if(types[lineNumber][i] != "comment"):
                return "[Line " + str(lineNumber) + "] SyntaxError: not a comment"
            
            comments.append(lexemes[lineNumber][i])

        if(commentFound == False):
            break

        start = 0
        lineNumber = nextLineNumber(lineNumber)
        
        if(lineNumber == None):
            return "[Line " + str(lineNumber) + "] SyntaxError: missing TLDR"

    if(len(comments) == 0):
        return "[Line " + str(lineNumber) + "] SyntaxError: no comment indicated"

    return nextLineNumber(lineNumber)

def sumOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def diffOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def produktOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def quoshuntOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def modOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def biggrOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def smallrOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def smooshSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def notSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def bothOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def eitherOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def wonOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def allOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def anyOfSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def itzSyntax(lineNumber):
    itzLexeme = lexemes[lineNumber].index("ITZ")

    if(len(lexemes[lineNumber]) == 3):
        return "[Line " + str(lineNumber) + "] SyntaxError: required identifier, literal, or expression"
    
    if(types[lineNumber][itzLexeme + 1] in literals):
        if(itzLexeme + 1 != len(lexemes[lineNumber])-1):
            if(lexemes[lineNumber][itzLexeme + 2] == "BTW"):
                singleCommentSyntax(lineNumber)
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after variable declaration"
    elif(types[lineNumber][itzLexeme + 1] == "string delimiter" and types[lineNumber][itzLexeme + 2] == "YARN literal" and types[lineNumber][itzLexeme + 3] == "string delimiter"):
        if(itzLexeme + 3 != len(lexemes[lineNumber])-1):
            if(lexemes[lineNumber][itzLexeme + 4] == "BTW"):
                singleCommentSyntax(lineNumber)
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after variable declaration"
    elif(types[lineNumber][itzLexeme + 1] == "identifier"):
        if(itzLexeme + 1 != len(lexemes[lineNumber])-1):
            if(lexemes[lineNumber][itzLexeme + 2] == "BTW"):
                singleCommentSyntax(lineNumber)
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after variable declaration"
    elif(lexemes[lineNumber][itzLexeme + 1] == "SUM OF"):
        syntaxError = sumOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "DIFF OF"):
        syntaxError = diffOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "PRODUKT OF"):
        syntaxError = produktOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "QUOSHUNT OF"):
        syntaxError = quoshuntOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "MOD OF"):
        syntaxError = modOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "BIGGR OF"):
        syntaxError = biggrOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "SMALLR OF"):
        syntaxError = smallrOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "SMOOSH"):
        syntaxError = smooshSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "NOT"):
        syntaxError = notSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "BOTH OF"):
        syntaxError = bothOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "EITHER OF"):
        syntaxError = eitherOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "WON OF"):
        syntaxError = wonOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "ALL OF"):
        syntaxError = allOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "ANY OF"):
        syntaxError = anyOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    
    return "OK"
    

def iHasASyntax(lineNumber):
    if(len(lexemes[lineNumber]) == 1):
        return "[Line " + str(lineNumber) + "] SyntaxError: required identifier"

    if(len(lexemes[lineNumber]) >= 2):
        if(types[lineNumber][1] != "identifier"):
            return "[Line " + str(lineNumber) + "] SyntaxError: required identifier"

        if(len(lexemes[lineNumber]) > 2):
            if(lexemes[lineNumber][2] == "ITZ"):
                syntaxError = itzSyntax(lineNumber)

                if(syntaxError != "OK"):
                    return syntaxError

    return "OK"

def haiSyntax(lineNumber):
    if(len(lexemes[lineNumber]) != 1):
        if(lexemes[lineNumber][1] == "BTW"):
            singleCommentSyntax(lineNumber)
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: HAI must have its own line"
    
    return "OK"

def kthxbyeSyntax(lineNumber):
    if(len(lexemes[lineNumber]) != 1):
        if(lexemes[lineNumber][1] == "BTW"):
            singleCommentSyntax(lineNumber)
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: KTHXBYE must have its own line"
    
    return "OK"

lineNumber = list(lexemes.keys())[0]
lexemeIndex = 0

codeStarted = False
codeEnded = False
commentFound = False

while(True):
    #toPrint = lexemes[lineNumber][lexemeIndex]
    #print("NOW CHECKING: " + lexemes[lineNumber][lexemeIndex] + " in line " + str(lineNumber))
    if(codeStarted == False):
        if(lexemes[lineNumber][lexemeIndex] != "HAI"):
            if(lexemes[lineNumber][lexemeIndex] == "BTW"):
                syntaxError = singleCommentSyntax(lineNumber)

                if(syntaxError != "OK"):
                    print(syntaxError)
                    break

                lineNumber = nextLineNumber(lineNumber)
                continue
            elif(lexemes[lineNumber][lexemeIndex] == "OBTW"):
                commentFound = True
                syntaxError = multiCommentSyntax(lineNumber)

                if(isinstance(syntaxError, int)):
                    lineNumber = syntaxError
                    continue
                else:
                    print(syntaxError)
                    break
            else:
                print("[Line " + str(lineNumber) + "] SyntaxError: Cannot include statements before HAI")
                break
        else:
            codeStarted = True
            syntaxError = haiSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
    elif(codeEnded):
        if(lexemes[lineNumber][lexemeIndex] == "BTW"):
            syntaxError = singleCommentSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break
            
            lineNumber = nextLineNumber(lineNumber)

            if(lineNumber != None):
                continue
            else:
                break
        elif(lexemes[lineNumber][lexemeIndex] == "OBTW"):
            commentFound = True
            syntaxError = multiCommentSyntax(lineNumber)

            if(isinstance(syntaxError, int)):
                lineNumber = syntaxError
                continue
            elif(syntaxError == None):
                break
            else:
                print(syntaxError)
                break
        else:
            print("[Line " + str(lineNumber) + "] SyntaxError: Cannot include statements after KTHXBYE")
            break
    else:
        if(lexemes[lineNumber][lexemeIndex] == "BTW"):
            syntaxError = singleCommentSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "OBTW"):
            commentFound = True
            syntaxError = multiCommentSyntax(lineNumber)

            if(isinstance(syntaxError, int)):
                lineNumber = syntaxError
                continue
            else:
                print(syntaxError)
                break
        elif(lexemes[lineNumber][lexemeIndex] == "I HAS A"):
            syntaxError = iHasASyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "KTHXBYE"):
            codeEnded = True
            syntaxError = kthxbyeSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break
            
            lineNumber = nextLineNumber(lineNumber)

            if(lineNumber != None):
                continue
            else:
                break

     
                
                

                


# for i in lexemes.keys():
#     print("[" + str(i) + "] " + str(lexemes[i]))

# for i in types.keys():
#     print("[" + str(i) + "] " + str(types[i]))

