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
    sumOfIndex = lexemes[lineNumber].index("SUM OF")

    # print(lexemes[lineNumber])
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
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal"
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
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal"
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
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal"
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
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal"
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
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal"
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

# BIGGR OF (removed by Rio)
# SMALLR OF (removed by Rio)

def smooshSyntax(lineNumber):
    print("")
    #INSERT CODE HERE

def notSyntax(lineNumber):
    # NOT <x>
    global startBoolOperator
    global sameBoolOperator

    if (startBoolOperator == ""):
        startBoolOperator = "NOT"
        sameBoolOperator += 1                   # Incrementing the count

        notIndex = lexemes[lineNumber].index("NOT")

        if (types[lineNumber][notIndex + 1] in ["TROOF literal", "identifier"]):
            try:
                if (lexemes[lineNumber][notIndex + 2] == "BTW"):
                    syntaxError = singleCommentSyntax(lineNumber)

                    if (syntaxError != "OK"):
                        return syntaxError

                    startBoolOperator = ""
                    sameBoolOperator = 0
                    return "OK"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
            except IndexError:
                startBoolOperator = ""
                sameBoolOperator = 0
                return "OK"         # When there is no comment
        elif (lexemes[lineNumber][notIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
            if (lexemes[lineNumber][notIndex + 1] == "BOTH OF"):
                syntaxError = bothOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][notIndex + 1] == "EITHER OF"):
                syntaxError = eitherOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][notIndex + 1] == "WON OF"):
                syntaxError = wonOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            else:
                sameBoolOperator += 1

                syntaxError = notSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            
            try:
                btwIndex = lexemes[lineNumber].index("BTW")
                if (lexemes[lineNumber][btwIndex] == "BTW"):
                    syntaxError = singleCommentSyntax(lineNumber)

                    if (syntaxError != "OK"):
                        return syntaxError

                    startBoolOperator = ""
                    sameBoolOperator = 0
                    return "OK"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
            except IndexError:
                startBoolOperator = ""
                sameBoolOperator = 0
                return "OK"         # When there is no comment
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
    else:
        notIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'NOT'][sameBoolOperator - 1]

        if (types[lineNumber][notIndex + 1] in ["TROOF literal", "identifier"]):
                return "OK"         
        elif (lexemes[lineNumber][notIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
            if (lexemes[lineNumber][notIndex + 1] == "BOTH OF"):
                syntaxError = bothOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][notIndex + 1] == "EITHER OF"):
                syntaxError = eitherOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            elif (lexemes[lineNumber][notIndex + 1] == "WON OF"):
                syntaxError = wonOfSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError
            else:
                sameBoolOperator += 1
                syntaxError = notSyntax(lineNumber)
                if (syntaxError != "OK"):
                    return syntaxError

            return "OK"         # When there is no comment
        else:
            return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"

def bothOfSyntax(lineNumber):
    # BOTH OF <x> AN <y>
    # print(lineNumber)
    # for k in range(len(lexemes[lineNumber])):
    #     print(types[lineNumber][k])

    global startBoolOperator
    global sameBoolOperator
    
    try: 
        if (startBoolOperator == ""):
            startBoolOperator = "BOTH OF"
            sameBoolOperator += 1                   # Incrementing the count

            bothOfIndex = lexemes[lineNumber].index("BOTH OF")
            if (types[lineNumber][bothOfIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][bothOfIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][bothOfIndex + 3] in ["TROOF literal", "identifier"]):
                        try:
                            if (lexemes[lineNumber][bothOfIndex + 4] == "BTW"):
                                syntaxError = singleCommentSyntax(lineNumber)

                                if (syntaxError != "OK"):
                                    return syntaxError

                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                        except IndexError:
                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"         # When there is no comment
                    elif (lexemes[lineNumber][bothOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][bothOfIndex + 1] == "BOTH OF"):
                            sameBoolOperator += 1
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
                        
                        try:
                            if (lexemes[lineNumber][bothOfIndex + 4] == "BTW"):
                                syntaxError = singleCommentSyntax(lineNumber)

                                if (syntaxError != "OK"):
                                    return syntaxError

                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                        except IndexError:
                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"         # When there is no comment
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][bothOfIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][bothOfIndex + 1] == "BOTH OF"):
                    sameBoolOperator += 1

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
                
                try:
                    anIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]
                except IndexError:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"

                if (lexemes[lineNumber][anIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                    if (lexemes[lineNumber][bothOfIndex + 1] == "BOTH OF"):
                        sameBoolOperator += 1

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
                    
                    try:
                        btwIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
                        if (lexemes[lineNumber][btwIndex] == "BTW"):
                            syntaxError = singleCommentSyntax(lineNumber)

                            if (syntaxError != "OK"):
                                return syntaxError

                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                    except IndexError:
                        startBoolOperator = ""
                        sameBoolOperator = 0
                        return "OK"         # When there is no comment
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            # BOTH OF <x> AN <y>
            sameBoolIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'BOTH OF'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
            if (types[lineNumber][sameBoolIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][sameBoolIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][sameBoolIndex + 3] in ["TROOF literal", "identifier"]):
                        return "OK"         # When there is no comment
                    elif (lexemes[lineNumber][sameBoolIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][sameBoolIndex + 3] == "BOTH OF"):
                            sameBoolOperator += 1

                            syntaxError = bothOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "EITHER OF"):
                            syntaxError = eitherOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "WON OF"):
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
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][sameBoolIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][sameBoolIndex + 1] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    sameBoolOperator += 1

                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "WON OF"):
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
    except IndexError:
        return "[Line " + str(lineNumber) + "] SyntaxError: invalid syntax"

def eitherOfSyntax(lineNumber):
    # EITHER OF <x> AN <y>
    # print(lineNumber)
    # for k in range(len(lexemes[lineNumber])):
    #     print(types[lineNumber][k])

    global startBoolOperator
    global sameBoolOperator
    try:
        if (startBoolOperator == ""):
            startBoolOperator = "EITHER OF"
            sameBoolOperator += 1                   # Incrementing the count

            eitherOfIndex = lexemes[lineNumber].index("EITHER OF")

            if (types[lineNumber][eitherOfIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][eitherOfIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][eitherOfIndex + 3] in ["TROOF literal", "identifier"]):
                        try:
                            if (lexemes[lineNumber][eitherOfIndex + 4] == "BTW"):
                                syntaxError = singleCommentSyntax(lineNumber)

                                if (syntaxError != "OK"):
                                    return syntaxError

                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                        except IndexError:
                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"         # When there is no comment
                    elif (lexemes[lineNumber][eitherOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][eitherOfIndex + 1] == "BOTH OF"):
                            syntaxError = bothOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                        elif (lexemes[lineNumber][eitherOfIndex + 1] == "EITHER OF"):
                            sameBoolOperator += 1

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
                        
                        try:
                            if (lexemes[lineNumber][eitherOfIndex + 4] == "BTW"):
                                syntaxError = singleCommentSyntax(lineNumber)

                                if (syntaxError != "OK"):
                                    return syntaxError

                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                        except IndexError:
                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"         # When there is no comment
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][eitherOfIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][eitherOfIndex + 1] == "BOTH OF"):

                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                elif (lexemes[lineNumber][eitherOfIndex + 1] == "EITHER OF"):
                    sameBoolOperator += 1

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
                
                try:
                    anIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]
                except IndexError:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"

                if (lexemes[lineNumber][anIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                    if (lexemes[lineNumber][eitherOfIndex + 1] == "BOTH OF"):
                        syntaxError = bothOfSyntax(lineNumber)
                        if (syntaxError != "OK"):
                            return syntaxError
                    elif (lexemes[lineNumber][eitherOfIndex + 1] == "EITHER OF"):
                        sameBoolOperator += 1

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
                    
                    try:
                        btwIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
                        if (lexemes[lineNumber][btwIndex] == "BTW"):
                            syntaxError = singleCommentSyntax(lineNumber)

                            if (syntaxError != "OK"):
                                return syntaxError

                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                    except IndexError:
                        startBoolOperator = ""
                        sameBoolOperator = 0
                        return "OK"         # When there is no comment
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            # EITHER OF <x> AN <y>
            sameBoolIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'EITHER OF'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
            if (types[lineNumber][sameBoolIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][sameBoolIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][sameBoolIndex + 3] in ["TROOF literal", "identifier"]):
                        return "OK"         # When there is no comment
                    elif (lexemes[lineNumber][sameBoolIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][sameBoolIndex + 3] == "BOTH OF"):
                            syntaxError = bothOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "EITHER OF"):
                            sameBoolOperator += 1
                            syntaxError = eitherOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "WON OF"):
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
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][sameBoolIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][sameBoolIndex + 1] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "EITHER OF"):
                    sameBoolOperator += 1

                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "WON OF"):
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
    except IndexError:
        return "[Line " + str(lineNumber) + "] SyntaxError: invalid syntax" 

def wonOfSyntax(lineNumber):
    # WON OF <x> AN <y>
    # print(lineNumber)
    # for k in range(len(lexemes[lineNumber])):
    #     print(types[lineNumber][k])

    global startBoolOperator
    global sameBoolOperator
    try:
        if (startBoolOperator == ""):
            startBoolOperator = "WON OF"
            sameBoolOperator += 1                   # Incrementing the count

            bothOfIndex = lexemes[lineNumber].index("WON OF")

            if (types[lineNumber][bothOfIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][bothOfIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][bothOfIndex + 3] in ["TROOF literal", "identifier"]):
                        try:
                            if (lexemes[lineNumber][bothOfIndex + 4] == "BTW"):
                                syntaxError = singleCommentSyntax(lineNumber)

                                if (syntaxError != "OK"):
                                    return syntaxError

                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                        except IndexError:
                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"         # When there is no comment
                    elif (lexemes[lineNumber][bothOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][bothOfIndex + 1] == "BOTH OF"):
                            syntaxError = bothOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                        elif (lexemes[lineNumber][bothOfIndex + 1] == "EITHER OF"):
                            syntaxError = eitherOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                        elif (lexemes[lineNumber][bothOfIndex + 1] == "WON OF"):
                            sameBoolOperator += 1
                            syntaxError = wonOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                        else:
                            syntaxError = notSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                        
                        try:
                            if (lexemes[lineNumber][bothOfIndex + 4] == "BTW"):
                                syntaxError = singleCommentSyntax(lineNumber)

                                if (syntaxError != "OK"):
                                    return syntaxError

                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                        except IndexError:
                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"         # When there is no comment
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][bothOfIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][bothOfIndex + 1] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                elif (lexemes[lineNumber][bothOfIndex + 1] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                elif (lexemes[lineNumber][bothOfIndex + 1] == "WON OF"):
                    sameBoolOperator += 1

                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                
                try:
                    anIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]
                except IndexError:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"

                if (lexemes[lineNumber][anIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                    if (lexemes[lineNumber][bothOfIndex + 1] == "BOTH OF"):
                        syntaxError = bothOfSyntax(lineNumber)
                        if (syntaxError != "OK"):
                            return syntaxError
                    elif (lexemes[lineNumber][bothOfIndex + 1] == "EITHER OF"):
                        syntaxError = eitherOfSyntax(lineNumber)
                        if (syntaxError != "OK"):
                            return syntaxError
                    elif (lexemes[lineNumber][bothOfIndex + 1] == "WON OF"):
                        sameBoolOperator += 1
                        syntaxError = wonOfSyntax(lineNumber)
                        if (syntaxError != "OK"):
                            return syntaxError
                    else:
                        syntaxError = notSyntax(lineNumber)
                        if (syntaxError != "OK"):
                            return syntaxError
                    
                    try:
                        btwIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
                        if (lexemes[lineNumber][btwIndex] == "BTW"):
                            syntaxError = singleCommentSyntax(lineNumber)

                            if (syntaxError != "OK"):
                                return syntaxError

                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                    except IndexError:
                        startBoolOperator = ""
                        sameBoolOperator = 0
                        return "OK"         # When there is no comment
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            # BOTH OF <x> AN <y>
            sameBoolIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'BOTH OF'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
            if (types[lineNumber][sameBoolIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][sameBoolIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][sameBoolIndex + 3] in ["TROOF literal", "identifier"]):
                        return "OK"         # When there is no comment
                    elif (lexemes[lineNumber][sameBoolIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][sameBoolIndex + 3] == "BOTH OF"):
                            syntaxError = bothOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "EITHER OF"):
                            syntaxError = eitherOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "WON OF"):
                            sameBoolOperator += 1
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
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][sameBoolIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][sameBoolIndex + 1] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "WON OF"):
                    sameBoolOperator += 1

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
    except IndexError:
        return "[Line " + str(lineNumber) + "] SyntaxError: invalid syntax"

def allOfSyntax(lineNumber):
    # ALL OF <x> AN <y> AN <z>
    # print(lineNumber)
    # for k in range(len(lexemes[lineNumber])):
    #     print(types[lineNumber][k])

    global startBoolOperator
    global sameBoolOperator

    try:
        if (lexemes[lineNumber].count("ANY OF") >= 1):
            return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have nested infinite arity OR operator inside this statement"
        if (lexemes[lineNumber].count("ALL OF") > 1):
            return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have nested infinite arity AND operator"

        if (startBoolOperator == ""):
            startBoolOperator = "ALL OF"
            sameBoolOperator += 1                   # Incrementing the count

            allOfIndex = lexemes[lineNumber].index("ALL OF")

            if (types[lineNumber][allOfIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][allOfIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][allOfIndex + 3] in ["TROOF literal", "identifier"]):
                        if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                            try:
                                # if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                                if (lexemes[lineNumber][allOfIndex + 5] == "BTW"):
                                    syntaxError = singleCommentSyntax(lineNumber)

                                    if (syntaxError != "OK"):
                                        return syntaxError

                                    startBoolOperator = ""
                                    sameBoolOperator = 0
                                    return "OK"
                                else:
                                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                            except IndexError:
                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"         # When there is no comment
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: missing infinite arity AND operator delimiter"
                    elif (lexemes[lineNumber][allOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][allOfIndex + 1] == "BOTH OF"):
                            sameBoolOperator += 1
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
                        if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                            try:
                                # if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                                if (lexemes[lineNumber][allOfIndex + 5] == "BTW"):
                                    syntaxError = singleCommentSyntax(lineNumber)

                                    if (syntaxError != "OK"):
                                        return syntaxError

                                    startBoolOperator = ""
                                    sameBoolOperator = 0
                                    return "OK"
                                else:
                                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                            except IndexError:
                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"         # When there is no comment
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: missing infinite arity AND operator delimiter"
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][allOfIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][allOfIndex + 1] == "BOTH OF"):
                    sameBoolOperator += 1

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
                
                try:
                    anIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]
                except IndexError:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"

                if (lexemes[lineNumber][anIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                    if (lexemes[lineNumber][allOfIndex + 1] == "BOTH OF"):
                        sameBoolOperator += 1

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
                    
                    try:
                        btwIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
                        if (lexemes[lineNumber][btwIndex] == "BTW"):
                            syntaxError = singleCommentSyntax(lineNumber)

                            if (syntaxError != "OK"):
                                return syntaxError

                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                    except IndexError:
                        startBoolOperator = ""
                        sameBoolOperator = 0
                        return "OK"         # When there is no comment
                elif (lexemes[lineNumber][anIndex + 1] in ["TROOF literal, identifer"]):
                    if (lexemes[lineNumber][anIndex + 2] == "MKAY"):
                            try:
                                # if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                                if (lexemes[lineNumber][allOfIndex + 5] == "BTW"):
                                    syntaxError = singleCommentSyntax(lineNumber)

                                    if (syntaxError != "OK"):
                                        return syntaxError

                                    startBoolOperator = ""
                                    sameBoolOperator = 0
                                    return "OK"
                                else:
                                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                            except IndexError:
                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"         # When there is no comment
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: missing infinite arity AND operator delimiter"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            # ALL OF <x> AN <y>
            sameBoolIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'ALL OF'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
            if (types[lineNumber][sameBoolIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][sameBoolIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][sameBoolIndex + 3] in ["TROOF literal", "identifier"]):
                        return "OK"         # When there is no comment
                    elif (lexemes[lineNumber][sameBoolIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][sameBoolIndex + 3] == "BOTH OF"):
                            syntaxError = bothOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "EITHER OF"):
                            syntaxError = eitherOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "WON OF"):
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
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][sameBoolIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][sameBoolIndex + 1] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "WON OF"):
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
    except IndexError:
        return "[Line " + str(lineNumber) + "] SyntaxError: invalid syntax"

def anyOfSyntax(lineNumber):
    # ANY OF <x> AN <y> AN <z>
    # print(lineNumber)
    # for k in range(len(lexemes[lineNumber])):
    #     print(types[lineNumber][k])

    global startBoolOperator
    global sameBoolOperator
    try:
        if (lexemes[lineNumber].count("ALL OF") >= 1):
            return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have nested infinite arity OR operator inside this statement"
        if (lexemes[lineNumber].count("ANY OF") > 1):
            return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have nested infinite arity AND operator"

        if (startBoolOperator == ""):
            startBoolOperator = "ANY OF"
            sameBoolOperator += 1                   # Incrementing the count

            anyOfIndex = lexemes[lineNumber].index("ANY OF")

            if (types[lineNumber][anyOfIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][anyOfIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][anyOfIndex + 3] in ["TROOF literal", "identifier"]):
                        if (lexemes[lineNumber][anyOfIndex + 4] == "MKAY"):
                            try:
                                if (lexemes[lineNumber][anyOfIndex + 5] == "BTW"):
                                    syntaxError = singleCommentSyntax(lineNumber)

                                    if (syntaxError != "OK"):
                                        return syntaxError

                                    startBoolOperator = ""
                                    sameBoolOperator = 0
                                    return "OK"
                                else:
                                    return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                            except IndexError:
                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"         # When there is no comment
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: missing infinite arity OR operator delimiter"
                    elif (lexemes[lineNumber][anyOfIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][anyOfIndex + 1] == "BOTH OF"):
                            sameBoolOperator += 1
                            syntaxError = bothOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                        elif (lexemes[lineNumber][anyOfIndex + 1] == "EITHER OF"):
                            syntaxError = eitherOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                        elif (lexemes[lineNumber][anyOfIndex + 1] == "WON OF"):
                            syntaxError = wonOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                        else:
                            syntaxError = notSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                        
                        try:
                            if (lexemes[lineNumber][anyOfIndex + 4] == "BTW"):
                                syntaxError = singleCommentSyntax(lineNumber)

                                if (syntaxError != "OK"):
                                    return syntaxError

                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                        except IndexError:
                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"         # When there is no comment
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][anyOfIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][anyOfIndex + 1] == "BOTH OF"):
                    sameBoolOperator += 1

                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                elif (lexemes[lineNumber][anyOfIndex + 1] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                elif (lexemes[lineNumber][anyOfIndex + 1] == "WON OF"):
                    syntaxError = wonOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                else:
                    syntaxError = notSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                
                try:
                    anIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]
                except IndexError:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"

                if (lexemes[lineNumber][anIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                    if (lexemes[lineNumber][anyOfIndex + 1] == "BOTH OF"):
                        sameBoolOperator += 1

                        syntaxError = bothOfSyntax(lineNumber)
                        if (syntaxError != "OK"):
                            return syntaxError
                    elif (lexemes[lineNumber][anyOfIndex + 1] == "EITHER OF"):
                        syntaxError = eitherOfSyntax(lineNumber)
                        if (syntaxError != "OK"):
                            return syntaxError
                    elif (lexemes[lineNumber][anyOfIndex + 1] == "WON OF"):
                        syntaxError = wonOfSyntax(lineNumber)
                        if (syntaxError != "OK"):
                            return syntaxError
                    else:
                        syntaxError = notSyntax(lineNumber)
                        if (syntaxError != "OK"):
                            return syntaxError
                    
                    try:
                        btwIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'AN'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
                        if (lexemes[lineNumber][btwIndex] == "BTW"):
                            syntaxError = singleCommentSyntax(lineNumber)

                            if (syntaxError != "OK"):
                                return syntaxError

                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                    except IndexError:
                        startBoolOperator = ""
                        sameBoolOperator = 0
                        return "OK"         # When there is no comment
                elif (lexemes[lineNumber][anIndex + 1] in ["TROOF literal", "identifier"]):
                    if (lexemes[lineNumber][anIndex + 2] == "MKAY"):
                        try:
                            # if (lexemes[lineNumber][allOfIndex + 4] == "MKAY"):
                            if (lexemes[lineNumber][anIndex + 3] == "BTW"):
                                syntaxError = singleCommentSyntax(lineNumber)

                                if (syntaxError != "OK"):
                                    return syntaxError

                                startBoolOperator = ""
                                sameBoolOperator = 0
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after boolean operation"
                        except IndexError:
                            startBoolOperator = ""
                            sameBoolOperator = 0
                            return "OK"         # When there is no comment
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: missing infinite arity AND operator delimiter"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: invalid identifier"
        else:
            # ALL OF <x> AN <y>
            sameBoolIndex = [i for i, n in enumerate(lexemes[lineNumber]) if n == 'ANY OF'][sameBoolOperator - 1]       # Index of ith instance of EITHER OF
            if (types[lineNumber][sameBoolIndex + 1] in ["TROOF literal", "identifier"]):
                if (types[lineNumber][sameBoolIndex + 2] == "argument separator keyword"):
                    if (types[lineNumber][sameBoolIndex + 3] in ["TROOF literal", "identifier"]):
                        return "OK"         # When there is no comment
                    elif (lexemes[lineNumber][sameBoolIndex + 3] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                        if (lexemes[lineNumber][sameBoolIndex + 3] == "BOTH OF"):
                            syntaxError = bothOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "EITHER OF"):
                            syntaxError = eitherOfSyntax(lineNumber)
                            if (syntaxError != "OK"):
                                return syntaxError
                            
                            return "OK"
                        elif (lexemes[lineNumber][sameBoolIndex + 3] == "WON OF"):
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
                        return "[Line " + str(lineNumber) + "] SyntaxError: Missing arguments"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Missing argument separator keyword"
            elif (lexemes[lineNumber][sameBoolIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF", "NOT"]):
                if (lexemes[lineNumber][sameBoolIndex + 1] == "BOTH OF"):
                    syntaxError = bothOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "EITHER OF"):
                    syntaxError = eitherOfSyntax(lineNumber)
                    if (syntaxError != "OK"):
                        return syntaxError
                    
                    return "OK"
                elif (lexemes[lineNumber][sameBoolIndex + 1] == "WON OF"):
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
    except IndexError:
        return "[Line " + str(lineNumber) + "] SyntaxError: invalid syntax"

def bothSaemSyntax(lineNumber):
    bothSaemIndex = lexemes[lineNumber].index("BOTH SAEM")

    # Based on the documentation, "Comparisons are done using integer math if the operands are NUMBRs, and floating point math if the operands are NUMBARs"

    if (types[lineNumber][bothSaemIndex + 1] not in ["identifier", "NUMBR literal", "NUMBAR literal", "min operator", "max operator"]):
        return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier, literal, or operator"
    else:
        if (types[lineNumber][bothSaemIndex + 1] in ["identifier", "NUMBR literal", "NUMBAR literal"]):
            if types[lineNumber][bothSaemIndex + 2] == "argument separator keyword":
                if types[lineNumber][bothSaemIndex + 3] in ["identifier", "NUMBR literal", "NUMBAR literal", "min operator", "max operator"]:
                    if types[lineNumber][bothSaemIndex + 3] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                        try:
                            if lexemes[lineNumber][bothSaemIndex + 4] == "BTW":
                                syntaxError = singleCommentSyntax(lineNumber)

                                if syntaxError != "OK":
                                    return syntaxError
                                
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have statements after operation"
                        except IndexError:
                            return "OK"
                    else:
                        if types[lineNumber][bothSaemIndex + 4] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                            if types[lineNumber][bothSaemIndex + 5] == "argument separator keyword":
                                if types[lineNumber][bothSaemIndex + 6] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                                    try:
                                        if lexemes[lineNumber][bothSaemIndex + 7] == "BTW":
                                            syntaxError = singleCommentSyntax(lineNumber)

                                            if syntaxError != "OK":
                                                return syntaxError
                                            
                                            return "OK"
                                        else:
                                            return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have statements after operation"
                                    except IndexError:
                                        return "OK"
                                else:
                                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier or literal"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier or literal"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a literal or comparison operator"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
        else: #lexemes[lineNumber][bothSaemIndex + 1] in ["BIGGR OF", "SMALLR OF"]
            if types[lineNumber][bothSaemIndex + 2] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                if types[lineNumber][bothSaemIndex + 3] == "argument separator keyword":
                    if types[lineNumber][bothSaemIndex + 4] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                        if types[lineNumber][bothSaemIndex + 5] == "argument separator keyword":
                            if types[lineNumber][bothSaemIndex + 6] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                                try:
                                    if lexemes[lineNumber][bothSaemIndex + 7] == "BTW":
                                        syntaxError = singleCommentSyntax

                                        if syntaxError != "OK":
                                            return syntaxError
                                        
                                        return "OK"
                                    else:
                                        return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have statements after operation"
                                except IndexError:
                                    return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier or literal"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier or literal"

def diffrintSyntax(lineNumber):
    diffrintIndex = lexemes[lineNumber].index("DIFFRINT")


    # Based on the documentation, "Comparisons are done using integer math if the operands are NUMBRs, and floating point math if the operands are NUMBARs"

    if (types[lineNumber][diffrintIndex + 1] not in ["identifier", "NUMBR literal", "NUMBAR literal", "min operator", "max operator"]):
        return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier, literal, or operator"
    else:
        if (types[lineNumber][diffrintIndex + 1] in ["identifier", "NUMBR literal", "NUMBAR literal"]):
            if types[lineNumber][diffrintIndex + 2] == "argument separator keyword":
                if types[lineNumber][diffrintIndex + 3] in ["identifier", "NUMBR literal", "NUMBAR literal", "min operator", "max operator"]:
                    if types[lineNumber][diffrintIndex + 3] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                        try:
                            if lexemes[lineNumber][diffrintIndex + 4] == "BTW":
                                syntaxError = singleCommentSyntax(lineNumber)

                                if syntaxError != "OK":
                                    return syntaxError
                                
                                return "OK"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have statements after operation"
                        except IndexError:
                            return "OK"
                    else:
                        if types[lineNumber][diffrintIndex + 4] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                            if types[lineNumber][diffrintIndex + 5] == "argument separator keyword":
                                if types[lineNumber][diffrintIndex + 6] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                                    try:
                                        if lexemes[lineNumber][diffrintIndex + 7] == "BTW":
                                            syntaxError = singleCommentSyntax(lineNumber)

                                            if syntaxError != "OK":
                                                return syntaxError
                                            
                                            return "OK"
                                        else:
                                            return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have statements after operation"
                                    except IndexError:
                                        return "OK"
                                else:
                                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier or literal"
                            else:
                                return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier or literal"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected a literal or comparison operator"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
        else: #lexemes[lineNumber][bothSaemIndex + 1] in ["BIGGR OF", "SMALLR OF"]
            if types[lineNumber][diffrintIndex + 2] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                if types[lineNumber][diffrintIndex + 3] == "argument separator keyword":
                    if types[lineNumber][diffrintIndex + 4] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                        if types[lineNumber][diffrintIndex + 5] == "argument separator keyword":
                            if types[lineNumber][diffrintIndex + 6] in ["identifier", "NUMBR literal", "NUMBAR literal"]:
                                try:
                                    if lexemes[lineNumber][diffrintIndex + 7] == "BTW":
                                        syntaxError = singleCommentSyntax

                                        if syntaxError != "OK":
                                            return syntaxError
                                        
                                        return "OK"
                                    else:
                                        return "[Line " + str(lineNumber) + "] SyntaxError: Cannot have statements after operation"
                                except IndexError:
                                    return "OK"
                        else:
                            return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
                    else:
                        return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier or literal"
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
            else:
                return "[Line " + str(lineNumber) + "] SyntaxError: Expected an identifier or literal"

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
    # elif(lexemes[lineNumber][itzLexeme + 1] == "BIGGR OF"):
    #     syntaxError = biggrOfSyntax(lineNumber)

    #     if(syntaxError != "OK"):
    #         return syntaxError
    # elif(lexemes[lineNumber][itzLexeme + 1] == "SMALLR OF"):
    #     syntaxError = smallrOfSyntax(lineNumber)

    #     if(syntaxError != "OK"):
    #         return syntaxError
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
    elif(lexemes[lineNumber][itzLexeme + 1] == "BOTH SAEM"):
        syntaxError = allOfSyntax(lineNumber)

        if(syntaxError != "OK"):
            return syntaxError
    elif(lexemes[lineNumber][itzLexeme + 1] == "DIFFRINT"):
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
startBoolOperator = ""
sameBoolOperator = 0

while(True):
    #toPrint = lexemes[lineNumber][lexemeIndex]
    print("NOW CHECKING: " + lexemes[lineNumber][lexemeIndex] + " in line " + str(lineNumber))
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
        elif(lexemes[lineNumber][lexemeIndex] == "NOT"):
            syntaxError = notSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "ANY OF"):
            syntaxError = anyOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "ALL OF"):
            syntaxError = allOfSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "BOTH SAEM"):
            syntaxError = bothSaemSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
        elif(lexemes[lineNumber][lexemeIndex] == "DIFFRINT"):
            syntaxError = diffrintSyntax(lineNumber)

            if(syntaxError != "OK"):
                print(syntaxError)
                break

            lineNumber = nextLineNumber(lineNumber)
            continue
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

