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

# def mathOperationSyntax(lineNumber):
#     counter = 0
#     for keyword in lexemes[lineNumber]:                 # Checks the n operation keywords
#         if (keyword in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
#             counter += 1
#         else:
#             break

#     isNumber = False
#     numberCnt = 0
#     for k in range(counter, len(lexemes[lineNumber])):
#         if (numberCnt < counter + 1):
#             try:
#                 isNumber = not isNumber
#                 if isNumber:
#                     if (isinstance(int(lexemes[lineNumber][k]), int) or isinstance(float(lexemes[lineNumber][k]), float)):
#                         numberCnt += 1
#                 else:
#                     if (lexemes[lineNumber][k] != "AN"):
#                         return "[Line " + str(lineNumber) + "] SyntaxError: Expected an AN keyword between the literals"
#             except ValueError:
#                 print(lexemes[lineNumber][k])
#                 return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
#         else:
#             # print(lexemes[lineNumber][k])       # Checker
#             if(lexemes[lineNumber][k] == "BTW"):
#                 return singleCommentSyntax(lineNumber)
#             else:
#                 return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"

def sumOfSyntax(lineNumber):
    sumOfIndex = lexemes[lineNumber].index("SUM OF")

    counter = 0
    for keyword in range(sumOfIndex, len(lexemes[lineNumber])):                 # Checks the n operation keywords
        if (lexemes[lineNumber][keyword] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
            counter += 1
        else:
            break
    
    isNumber = False
    numberCnt = 0
    for k in range(sumOfIndex + counter, len(lexemes[lineNumber])):
        if (numberCnt < counter + 1):
            isNumber = not isNumber
            if isNumber:
                if (types[lineNumber][k] in ["NUMBR literal", "NUMBAR literal"]):
                    numberCnt += 1
            else:
                if (lexemes[lineNumber][k] != "AN"):
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                elif (lexemes[lineNumber][k] == "AN"):
                    continue
                else:
                    print(lexemes[lineNumber][k])
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
        else:
            if(lexemes[lineNumber][k] == "BTW"):
                return singleCommentSyntax(lineNumber)
            else:
                # print(lexemes[lineNumber][k])                 # CHECKER
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"

def diffOfSyntax(lineNumber):
    diffOfIndex = lexemes[lineNumber].index("DIFF OF")

    counter = 0
    for keyword in range(diffOfIndex, len(lexemes[lineNumber])):                 # Checks the n operation keywords
        if (lexemes[lineNumber][keyword] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
            counter += 1
        else:
            break
    
    isNumber = False
    numberCnt = 0
    for k in range(diffOfIndex + counter, len(lexemes[lineNumber])):
        if (numberCnt < counter + 1):
            isNumber = not isNumber
            if isNumber:
                if (types[lineNumber][k] in ["NUMBR literal", "NUMBAR literal"]):
                    numberCnt += 1
            else:
                if (lexemes[lineNumber][k] != "AN"):
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                elif (lexemes[lineNumber][k] == "AN"):
                    continue
                else:
                    print(lexemes[lineNumber][k])
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
        else:
            if(lexemes[lineNumber][k] == "BTW"):
                return singleCommentSyntax(lineNumber)
            else:
                # print(lexemes[lineNumber][k])                 # CHECKER
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"

def produktOfSyntax(lineNumber):
    produktOfIndex = lexemes[lineNumber].index("PRODUKT OF")

    counter = 0
    for keyword in range(produktOfIndex, len(lexemes[lineNumber])):                 # Checks the n operation keywords
        if (lexemes[lineNumber][keyword] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
            counter += 1
        else:
            break
    
    isNumber = False
    numberCnt = 0
    for k in range(produktOfIndex + counter, len(lexemes[lineNumber])):
        if (numberCnt < counter + 1):
            isNumber = not isNumber
            if isNumber:
                if (types[lineNumber][k] in ["NUMBR literal", "NUMBAR literal"]):
                    numberCnt += 1
            else:
                if (lexemes[lineNumber][k] != "AN"):
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                elif (lexemes[lineNumber][k] == "AN"):
                    continue
                else:
                    print(lexemes[lineNumber][k])
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
        else:
            if(lexemes[lineNumber][k] == "BTW"):
                return singleCommentSyntax(lineNumber)
            else:
                # print(lexemes[lineNumber][k])                 # CHECKER
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"

def quoshuntOfSyntax(lineNumber):
    quoshuntOfIndex = lexemes[lineNumber].index("QUOSHUNT OF")

    counter = 0
    for keyword in range(quoshuntOfIndex, len(lexemes[lineNumber])):                 # Checks the n operation keywords
        if (lexemes[lineNumber][keyword] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
            counter += 1
        else:
            break
    
    isNumber = False
    numberCnt = 0
    for k in range(quoshuntOfIndex + counter, len(lexemes[lineNumber])):
        if (numberCnt < counter + 1):
            isNumber = not isNumber
            if isNumber:
                if (types[lineNumber][k] in ["NUMBR literal", "NUMBAR literal"]):
                    numberCnt += 1
            else:
                if (lexemes[lineNumber][k] != "AN"):
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                elif (lexemes[lineNumber][k] == "AN"):
                    continue
                else:
                    print(lexemes[lineNumber][k])
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
        else:
            if(lexemes[lineNumber][k] == "BTW"):
                return singleCommentSyntax(lineNumber)
            else:
                # print(lexemes[lineNumber][k])                 # CHECKER
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"

def modOfSyntax(lineNumber):
    modOfIndex = lexemes[lineNumber].index("MOD OF")

    counter = 0
    for keyword in range(modOfIndex, len(lexemes[lineNumber])):                 # Checks the n operation keywords
        if (lexemes[lineNumber][keyword] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
            counter += 1
        else:
            break
    
    isNumber = False
    numberCnt = 0
    for k in range(modOfIndex + counter, len(lexemes[lineNumber])):
        if (numberCnt < counter + 1):
            isNumber = not isNumber
            if isNumber:
                if (types[lineNumber][k] in ["NUMBR literal", "NUMBAR literal"]):
                    numberCnt += 1
            else:
                if (lexemes[lineNumber][k] != "AN"):
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                elif (lexemes[lineNumber][k] == "AN"):
                    continue
                else:
                    print(lexemes[lineNumber][k])
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
        else:
            if(lexemes[lineNumber][k] == "BTW"):
                return singleCommentSyntax(lineNumber)
            else:
                # print(lexemes[lineNumber][k])                 # CHECKER
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"

def biggrOfSyntax(lineNumber):
    biggrOfIndex = lexemes[lineNumber].index("BIGGR OF")

    counter = 0
    for keyword in range(biggrOfIndex, len(lexemes[lineNumber])):                 # Checks the n operation keywords
        if (lexemes[lineNumber][keyword] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
            counter += 1
        else:
            break
    
    isNumber = False
    numberCnt = 0
    for k in range(biggrOfIndex + counter, len(lexemes[lineNumber])):
        if (numberCnt < counter + 1):
            isNumber = not isNumber
            if isNumber:
                if (types[lineNumber][k] in ["NUMBR literal", "NUMBAR literal"]):
                    numberCnt += 1
            else:
                if (lexemes[lineNumber][k] != "AN"):
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                elif (lexemes[lineNumber][k] == "AN"):
                    continue
                else:
                    print(lexemes[lineNumber][k])
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
        else:
            if(lexemes[lineNumber][k] == "BTW"):
                return singleCommentSyntax(lineNumber)
            else:
                # print(lexemes[lineNumber][k])                 # CHECKER
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"

def smallrOfSyntax(lineNumber):
    smallrOfIndex = lexemes[lineNumber].index("SMALLR OF")

    counter = 0
    for keyword in range(smallrOfIndex, len(lexemes[lineNumber])):                 # Checks the n operation keywords
        if (lexemes[lineNumber][keyword] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
            counter += 1
        else:
            break
    
    isNumber = False
    numberCnt = 0
    for k in range(smallrOfIndex + counter, len(lexemes[lineNumber])):
        if (numberCnt < counter + 1):
            isNumber = not isNumber
            if isNumber:
                if (types[lineNumber][k] in ["NUMBR literal", "NUMBAR literal"]):
                    numberCnt += 1
            else:
                if (lexemes[lineNumber][k] != "AN"):
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                elif (lexemes[lineNumber][k] == "AN"):
                    continue
                else:
                    print(lexemes[lineNumber][k])
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
        else:
            if(lexemes[lineNumber][k] == "BTW"):
                return singleCommentSyntax(lineNumber)
            else:
                # print(lexemes[lineNumber][k])                 # CHECKER
                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"

def smooshSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def notSyntax(lineNumber):
    print("")
        
def bothOfSyntax(lineNumber):
    bothOfIndex = lexemes[lineNumber].index("BOTH OF")

    if (len(lexemes[lineNumber]) < 4):
        return "[Line " + str(lineNumber) + "] SyntaxError: missing arguments"
        
    if (types[lineNumber][bothOfIndex + 1] == "TROOF literal"):
        if (types[lineNumber][bothOfIndex + 2] == "argument separator keyword"):
            if (types[lineNumber][bothOfIndex + 3] in ["TROOF literal", "identifier"]):
                if (lexemes[lineNumber][bothOfIndex + 4] == "BTW"):
                    syntaxError = singleCommentSyntax(lineNumber)

                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
            elif (lexemes[lineNumber][bothOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (types[lineNumber][bothOfIndex + 3] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (types[lineNumber][bothOfIndex + 3] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (types[lineNumber][bothOfIndex + 3] == "WON OF"):
                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: required argument separator keyword"
    else:
        if (lexemes[lineNumber][bothOfIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
            print(lexemes[lineNumber][bothOfIndex + 1])
            if (lexemes[lineNumber][bothOfIndex + 1] == "BOTH OF"):
                syntaxError = bothOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][bothOfIndex + 1] == "EITHER OF"):
                syntaxError = eitherOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][bothOfIndex + 1] == "WON OF"):
                syntaxError = wonOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            else:
                syntaxError = notSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
        
        if (types[lineNumber][bothOfIndex + 2] == "argument separator keyword"):
            if (types[lineNumber][bothOfIndex + 3] in ["TROOF literal", "identifier"]):
                if (lexemes[lineNumber][bothOfIndex + 4] == "BTW"):
                    syntaxError = singleCommentSyntax(lineNumber)

                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
            elif (lexemes[lineNumber][bothOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][bothOfIndex + 3] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (lexemes[lineNumber][bothOfIndex + 3] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (lexemes[lineNumber][bothOfIndex + 3] == "WON OF"):
                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"

def eitherOfSyntax(lineNumber):
    eitherOfIndex = lexemes[lineNumber].index("EITHER OF")

    if (len(lexemes[lineNumber]) < 4):
        return "[Line " + str(lineNumber) + "] SyntaxError: missing arguments"
        
    if (types[lineNumber][eitherOfIndex + 1] == "TROOF literal"):
        if (types[lineNumber][eitherOfIndex + 2] == "argument separator keyword"):
            if (types[lineNumber][eitherOfIndex + 3] in ["TROOF literal", "identifier"]):
                if (lexemes[lineNumber][eitherOfIndex + 4] == "BTW"):
                    syntaxError = singleCommentSyntax(lineNumber)

                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
            elif (lexemes[lineNumber][eitherOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (types[lineNumber][eitherOfIndex + 3] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (types[lineNumber][eitherOfIndex + 3] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (types[lineNumber][eitherOfIndex + 3] == "WON OF"):
                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: required argument separator keyword"
    else:
        if (lexemes[lineNumber][eitherOfIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
            if (lexemes[lineNumber][eitherOfIndex + 1] == "BOTH OF"):
                syntaxError = bothOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][eitherOfIndex + 1] == "EITHER OF"):
                syntaxError = eitherOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][eitherOfIndex + 1] == "WON OF"):
                syntaxError = wonOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            else:
                syntaxError = notSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError

        if (types[lineNumber][eitherOfIndex + 2] == "argument separator keyword"):
            if (types[lineNumber][eitherOfIndex + 3] in ["TROOF literal", "identifier"]):
                if (lexemes[lineNumber][eitherOfIndex + 4] == "BTW"):
                    syntaxError = singleCommentSyntax(lineNumber)

                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
            elif (lexemes[lineNumber][eitherOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][eitherOfIndex + 3] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (lexemes[lineNumber][eitherOfIndex + 3] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (lexemes[lineNumber][eitherOfIndex + 3] == "WON OF"):
                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"

def wonOfSyntax(lineNumber):
    wonOfIndex = lexemes[lineNumber].index("WON OF")

    if (len(lexemes[lineNumber]) < 4):
        return "[Line " + str(lineNumber) + "] SyntaxError: missing arguments"
        
    if (types[lineNumber][wonOfIndex + 1] == "TROOF literal"):
        if (types[lineNumber][wonOfIndex + 2] == "argument separator keyword"):
            if (types[lineNumber][wonOfIndex + 3] in ["TROOF literal", "identifier"]):
                if (lexemes[lineNumber][wonOfIndex + 4] == "BTW"):
                    syntaxError = singleCommentSyntax(lineNumber)

                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
            elif (lexemes[lineNumber][wonOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][wonOfIndex + 3] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (lexemes[lineNumber][wonOfIndex + 3] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (lexemes[lineNumber][wonOfIndex + 3] == "WON OF"):
                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: required argument separator keyword"
    else:
        if (lexemes[lineNumber][wonOfIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
            if (lexemes[lineNumber][wonOfIndex + 1] == "BOTH OF"):
                syntaxError = bothOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][wonOfIndex + 1] == "EITHER OF"):
                syntaxError = eitherOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][wonOfIndex + 1] == "WON OF"):
                syntaxError = wonOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            else:
                syntaxError = notSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError

        if (types[lineNumber][wonOfIndex + 2] == "argument separator keyword"):
            if (types[lineNumber][wonOfIndex + 3] in ["TROOF literal", "identifier"]):
                if (lexemes[lineNumber][wonOfIndex + 4] == "BTW"):
                    syntaxError = singleCommentSyntax(lineNumber)

                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
            elif (lexemes[lineNumber][wonOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][wonOfIndex + 3] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (lexemes[lineNumber][wonOfIndex + 3] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (lexemes[lineNumber][wonOfIndex + 3] == "WON OF"):
                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"

def allOfSyntax(lineNumber):
    allOfIndex = lexemes[lineNumber].index("ALL OF")

    if (len(lexemes[lineNumber]) < 4):
        return "[Line " + str(lineNumber) + "] SyntaxError: missing arguments"
        
    if (types[lineNumber][allOfIndex + 1] == "TROOF literal"):
        if (types[lineNumber][allOfIndex + 2] == "argument separator keyword"):
            if (types[lineNumber][allOfIndex + 3] in ["TROOF literal", "identifier"]):
                if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                    if (lexemes[lineNumber][allOfIndex + 5] == "BTW"):
                        syntaxError = singleCommentSyntax(lineNumber)

                        if (syntaxError != "OK"):
                            return syntaxError

                        return "OK"
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected infinitary arity AND operator delimiter"
            elif (lexemes[lineNumber][allOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (types[lineNumber][allOfIndex + 3] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                        if (lexemes[lineNumber][allOfIndex + 5] == "BTW"):
                            syntaxError = singleCommentSyntax(lineNumber)

                            if (syntaxError != "OK"):
                                return syntaxError

                            return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Expected infinitary arity AND operator delimiter"
                elif (types[lineNumber][allOfIndex + 3] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                        if (lexemes[lineNumber][allOfIndex + 5] == "BTW"):
                            syntaxError = singleCommentSyntax(lineNumber)

                            if (syntaxError != "OK"):
                                return syntaxError

                            return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Expected infinitary arity AND operator delimiter"
                elif (types[lineNumber][allOfIndex + 3] == "WON OF"):
                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                        if (lexemes[lineNumber][allOfIndex + 5] == "BTW"):
                            syntaxError = singleCommentSyntax(lineNumber)

                            if (syntaxError != "OK"):
                                return syntaxError

                            return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Expected infinitary arity AND operator delimiter"
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                        if (lexemes[lineNumber][allOfIndex + 5] == "BTW"):
                            syntaxError = singleCommentSyntax(lineNumber)

                            if (syntaxError != "OK"):
                                return syntaxError

                            return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Expected infinitary arity AND operator delimiter"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: required argument separator keyword"
    else:
        if (lexemes[lineNumber][allOfIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
            if (types[lineNumber][allOfIndex + 1] == "BOTH OF"):
                syntaxError = bothOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][allOfIndex + 1] == "EITHER OF"):
                syntaxError = eitherOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][allOfIndex + 1] == "WON OF"):
                syntaxError = wonOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            else:
                syntaxError = notSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError

        if (types[lineNumber][allOfIndex + 2] == "argument separator keyword"):
            if (types[lineNumber][allOfIndex + 3] in ["TROOF literal", "identifier"]):
                if (lexemes[lineNumber][allOfIndex + 4] == "BTW"):
                    syntaxError = singleCommentSyntax(lineNumber)

                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
            elif (lexemes[lineNumber][allOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][allOfIndex + 3] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (lexemes[lineNumber][allOfIndex + 3] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                elif (types[lineNumber][allOfIndex + 3] == "WON OF"):
                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError

                    return "OK"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: required argument separator keyword"

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
    # elif(lexemes[lineNumber][itzLexeme + 1] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "SMALLR OF", "BIGGR OF"]):
    #     syntaxError = mathOperationSyntax(lineNumber)

    #     if(syntaxError != "OK"):
    #         return syntaxError
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
        syntaxError = quoshuntOfSyntax(lineNumber)

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
        
        # ! START OF RIO DUCUSIN'S PART
        # elif(lexemes[lineNumber][lexemeIndex] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
        #     syntaxError = mathOperationSyntax(lineNumber)

        #     if(syntaxError != "OK"):
        #         print(syntaxError)
        #         break

        #     lineNumber = nextLineNumber(lineNumber)
        #     continue
        elif(lexemes[lineNumber][lexemeIndex] == "SUM OF"):
            syntaxError = sumOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "DIFF OF"):
            syntaxError = diffOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "PRODUKT OF"):
            syntaxError = produktOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "QUOSHUNT OF"):
            syntaxError = quoshuntOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "MOD OF"):
            syntaxError = modOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "BIGGR OF"):
            syntaxError = biggrOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "SMALLR OF"):
            syntaxError = smallrOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "BOTH OF"):
            syntaxError = bothOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "EITHER OF"):
            syntaxError = eitherOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "WON OF"):
            syntaxError = wonOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue

        # elif(lexemes[lineNumber][lexemeIndex] == "NOT"):
        #     syntaxError = notSyntax(lineNumber)

        #     if(syntaxError != "OK"):
        #         print(syntaxError)
        #         break

        #     lineNumber = nextLineNumber(lineNumber)
        #     continue

        # elif(lexemes[lineNumber][lexemeIndex] == "ANY OF"):
        #     syntaxError = anyOfSyntax(lineNumber)

        #     if(syntaxError != "OK"):
        #         print(syntaxError)
        #         break

        #     lineNumber = nextLineNumber(lineNumber)
        #     continue

        elif(lexemes[lineNumber][lexemeIndex] == "ALL OF"):
            syntaxError = allOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue

        # elif(lexemes[lineNumber][lexemeIndex] == "BOTH SAEM"):
        #     syntaxError = bothSaemSyntax(lineNumber)

        #     if(syntaxError != "OK"):
        #         print(syntaxError)
        #         break

        #     lineNumber = nextLineNumber(lineNumber)
        #     continue

        # ! END OF RIO DUCUSIN'S PART

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

