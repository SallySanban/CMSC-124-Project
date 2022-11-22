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

    commentFound = False

    return "OK"

def tldrSyntax(lineNumber):
    commentDelimiter = lexemes[lineNumber].index("TLDR")
    
    if(len(lexemes[lineNumber]) - (commentDelimiter + 1) != 0):
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
                if(tldrSyntax(lineNumber) != "OK"):
                    return tldrSyntax(lineNumber)

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









line = list(lexemes.keys())[0]
lexeme = 0

codeStarted = False
commentFound = False

while(True):
    #print("NOW CHECKING: " + lexemes[line][lexeme] + " in line " + str(line))
    if(codeStarted == False):
        if(lexemes[line][lexeme] != "HAI"):
            if(lexemes[line][lexeme] == "BTW"):
                commentFound = True
                syntaxError = singleCommentSyntax(line)

                if(syntaxError != "OK"):
                    print(syntaxError)
                    break

                line = nextLineNumber(line)
                continue
            elif(lexemes[line][lexeme] == "OBTW"):
                commentFound = True
                syntaxError = multiCommentSyntax(line)

                if(isinstance(syntaxError, int)):
                    line = syntaxError

                    continue
                elif(syntaxError == None):
                    print("[Line " + str(line) + "] SyntaxError: Missing TLDR")
                    break
                else:
                    print(syntaxError)
                    break
            else:
                print("[Line " + str(line) + "] SyntaxError: Cannot include statements before HAI")
                break
        else:
            print("OK")
            break
            
                
                

                


# for i in lexemes.keys():
#     print("[" + str(i) + "] " + str(lexemes[i]))

# for i in types.keys():
#     print("[" + str(i) + "] " + str(types[i]))

