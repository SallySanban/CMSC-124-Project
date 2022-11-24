import re

filename = "Project 3/samplecodewrong.txt"

#reads file and cleans each line in the file
def readFile(filename):
    file = open(filename)
    lines = []

    #reads the file and places each line in a list
    for line in file.readlines():
        if(line != "\n"):
            if(line[len(line)-1] == "\n"):
                lines.append(line[0:len(line)-1])
            else:
                lines.append(line)
        else:
           lines.append("")

    #gets rid of leading whitespaces in each line
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()
        
    return lines

#finds lexemes in code and groups them 
def findLexemes(lines):
    stringFound = False
    singleCommentFound = False
    multiCommentFound = False
    keywordFound = False
    isNowAKeyword = ""
    oRlyKeyword = ""
    yaRlyKeyword = ""
    noWaiKeyword = ""
    imYrKeyword = ""
    keyword = ""
    string = ""
    singleComment = ""
    multiComment = ""

    for i in range(0, len(lines)):
        splitWords = lines[i].split()
        for j in range(0, len(splitWords)):
            #catches single comments
            if(splitWords[j] == "BTW"):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("comment delimiter")
                else:
                    types[i+1].append("comment delimiter")

                singleCommentFound = True
                continue
            
            if(singleCommentFound == True):
                singleComment = singleComment + splitWords[j] + " "
                
                if(j == len(splitWords)-1):
                    singleCommentFound = False

                    if(singleComment != ""):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(singleComment.strip())
                        else:
                            lexemes[i+1].append(singleComment.strip())

                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("comment")
                        else:
                            types[i+1].append("comment")
                    
                    singleComment = ""
                
                continue
            
            #catches multi comments
            if(splitWords[j] == "OBTW"):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("comment delimiter")
                else:
                    types[i+1].append("comment delimiter")

                multiCommentFound = True
                continue
            
            if(multiCommentFound == True):
                if (splitWords[j] == "TLDR"):
                    if(multiComment != ""):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(multiComment.strip())
                        else:
                            lexemes[i+1].append(multiComment.strip())

                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("comment")
                        else:
                            types[i+1].append("comment")
                            
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(splitWords[j])
                    else:
                        lexemes[i+1].append(splitWords[j])

                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("comment delimiter")
                    else:
                        types[i+1].append("comment delimiter")

                    multiCommentFound = False
                    multiComment = ""
                    continue
                else:
                    multiComment = multiComment + splitWords[j] + " "

                if(j == len(splitWords)-1):
                    if(multiComment != ""):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(multiComment.strip())
                        else:
                            lexemes[i+1].append(multiComment.strip())

                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("comment")
                        else:
                            types[i+1].append("comment")
                    
                    multiComment = ""

                    continue
                
                continue

            #catches yarn and string delimiter
            if('\"' == splitWords[j][0]):
                stringFound = True

            if(stringFound == True):
                string = string + splitWords[j] + " "

                if('\"' == splitWords[j][len(splitWords[j])-1] or j == len(splitWords)-1):
                    stringFound = False

                    if(string != ""):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append("\"")
                            lexemes[i+1].append(string.strip()[1:len(string.strip())-1])
                            lexemes[i+1].append("\"")
                        else:
                            lexemes[i+1].append("\"")
                            lexemes[i+1].append(string.strip()[1:len(string.strip())-1])
                            lexemes[i+1].append("\"")

                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("string delimiter")
                            types[i+1].append("YARN literal")
                            types[i+1].append("string delimiter")
                        else:
                            types[i+1].append("string delimiter")
                            types[i+1].append("YARN literal")
                            types[i+1].append("string delimiter")
                    
                    string = ""

                continue

            #catches literals
            numbrLiteral = re.search("^[-]?\d+$", splitWords[j])
            if(numbrLiteral):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("NUMBR literal")
                else:
                    types[i+1].append("NUMBR literal")

                continue

            numbarLiteral = re.search("^[-]?\d+[.]\d+$", splitWords[j])
            if(numbarLiteral):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("NUMBAR literal")
                else:
                    types[i+1].append("NUMBAR literal")

                continue
            
            troofLiteralWin = re.search("^(WIN)$", splitWords[j])
            if(troofLiteralWin):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TROOF literal")
                else:
                    types[i+1].append("TROOF literal")
                
                continue

            troofLiteralFail = re.search("^(FAIL)$", splitWords[j])
            if(troofLiteralFail):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TROOF literal")
                else:
                    types[i+1].append("TROOF literal")

                continue

            typeLiteralTroof = re.search("^(TROOF)$", splitWords[j])
            if(typeLiteralTroof):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue
            
            typeLiteralNoob = re.search("^(NOOB)$", splitWords[j])
            if(typeLiteralNoob):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue

            typeLiteralNumbr = re.search("^(NUMBR)$", splitWords[j])
            if(typeLiteralNumbr):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue

            typeLiteralNumbar = re.search("^(NUMBAR)$", splitWords[j])
            if(typeLiteralNumbar):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue

            typeLiteralYarn = re.search("^(YARN)$", splitWords[j])
            if(typeLiteralYarn):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue

            typeLiteralType = re.search("^(TYPE)$", splitWords[j])
            if(typeLiteralType):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("TYPE literal")
                else:
                    types[i+1].append("TYPE literal")

                continue

            #PLACE KEYWORDS HERE (make sure identifier is last)
            haiKeyword = re.search("^(HAI)$", splitWords[j])                        # HAI
            if (haiKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("code delimiter")
                else:
                    types[i+1].append("code delimiter")

                continue

            kThxByeKeyword = re.search("^(KTHXBYE)$", splitWords[j])               # KTHXBYE
            if (kThxByeKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("code delimiter")
                else:
                    types[i+1].append("code delimiter")
                    
                continue
            
            # I HAS A KEYWORD               (ONLY KEYWORD STARTING WITH I)
            if (splitWords[j] == "I"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "I" or keyword =="I HAS")):
                if (splitWords[j] == "HAS"):
                    keyword = keyword + " " + "HAS"
                    continue
                elif (splitWords[j] == "A" and keyword == "I HAS"):
                    keyword = keyword + " " + "A"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("variable declaration")
                    else:
                        types[i+1].append("variable declaration")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            itzKeyword = re.search("^(ITZ)$", splitWords[j])                          # ITZ
            if (itzKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("variable initialization")
                else:
                    types[i+1].append("variable initialization")
                continue
            
            rKeyword = re.search("^(R)$", splitWords[j])                          # R
            if (rKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("assignment operator")
                else:
                    types[i+1].append("assignment operator")
                continue
            
            # SUM OF KEYWORD               (ONLY KEYWORD STARTING WITH SUM)
            if (splitWords[j].strip() == "SUM"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "SUM")):
                if (splitWords[j].strip() == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("add operator")
                    else:
                        types[i+1].append("add operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # DIFF OF KEYWORD
            if (splitWords[j] == "DIFF"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "DIFF")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("subtract operator")
                    else:
                        types[i+1].append("subtract operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # PRODUKT OF KEYWORD
            if (splitWords[j] == "PRODUKT"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "PRODUKT")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("multiply operator")
                    else:
                        types[i+1].append("multiply operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            # QUOSHUNT OF KEYWORD
            if (splitWords[j].strip() == "QUOSHUNT"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "QUOSHUNT")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("divide operator")
                    else:
                        types[i+1].append("divide operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # MOD OF KEYWORD
            if (splitWords[j].strip() == "MOD"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "MOD")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("modulo operator")
                    else:
                        types[i+1].append("modulo operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # BIGGR OF KEYWORD
            if (splitWords[j].strip() == "BIGGR"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "BIGGR")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("max operator")
                    else:
                        types[i+1].append("max operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # SMALLR OF KEYWORD
            if (splitWords[j].strip() == "SMALLR"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "SMALLR")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("min operator")
                    else:
                        types[i+1].append("min operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # BOTH OF KEYWORD
            if (splitWords[j].strip() == "BOTH"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "BOTH")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("and operator")
                    else:
                        types[i+1].append("and operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                elif (splitWords[j] == "SAEM"):
                    keyword = keyword + " " + "SAEM"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("is equal comparison operator")
                    else:
                        types[i+1].append("is equal comparison operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # EITHER OF KEYWORD
            if (splitWords[j].strip() == "EITHER"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "EITHER")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("or operator")
                    else:
                        types[i+1].append("or operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # WON OF KEYWORD
            if (splitWords[j].strip() == "WON"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "WON")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("xor operator")
                    else:
                        types[i+1].append("xor operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            # NOT KEYWORD
            notKeyword = re.findall("^(NOT)$", splitWords[j])                          # NOT (between)
            if (notKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
                
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("not operator")
                else:
                    types[i+1].append("not operator")
                continue
            
            # ANY OF KEYWORD
            if (splitWords[j].strip() == "ANY"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "ANY")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("infinite arity OR operator")
                    else:
                        types[i+1].append("infinite arity OR operator")
                    
                    keywordFound == False        # REINITIALIZE USED VARIABLES
                    keyword = ""
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            
            # DIFFRINT KEYWORD
            diffrintKeyword = re.search("^(DIFFRINT)$", splitWords[j])
            if(diffrintKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("not equal comparison operator")
                else:
                    types[i+1].append("not equal comparison operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #MKAY Keyword
            smooshKeyword = re.search("^(SMOOSH)$", splitWords[j])                              # SMOOSH
            if(smooshKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("concatenation delimiter")
                else:
                    types[i+1].append("concatenation delimiter")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            #MKAY Keyword
            mkayKeyword = re.search("^(MKAY)$", splitWords[j])                              # SMOOSH
            if(mkayKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("concatenation delimiter")
                else:
                    types[i+1].append("concatenation delimiter")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            #MAEK Keyword
            maekKeyword = re.search("^(MAEK)$", splitWords[j])
            if(maekKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("typecasting operator")
                else:
                    types[i+1].append("typecasting operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            #A Keyword 
            aKeyword = re.search("^(A)$", splitWords[j])
            if(aKeyword and isNowAKeyword == ""):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("type separator operator")
                else:
                    types[i+1].append("type separator operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            # IS NOW A KEYWORD
            if(splitWords[j] == "IS"):
                isNowAKeyword = isNowAKeyword + splitWords[j] + " "
                continue


            if(isNowAKeyword == "IS "):
                if(splitWords[j] == "NOW"):
                    isNowAKeyword = isNowAKeyword + splitWords[j] + " "
                    continue

            if(isNowAKeyword == "IS NOW "):
                if(splitWords[j] == "A"):
                    isNowAKeyword = isNowAKeyword + splitWords[j]

                    if(isNowAKeyword == "IS NOW A"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(isNowAKeyword)
                        else:
                            lexemes[i+1].append(isNowAKeyword)
                    
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("typecast keyword")
                        else:
                            types[i+1].append("typecast keyword")
                        
                        isNowAKeyword = ""
                        continue

            #VISIBLE Keyword
            visibleKeyword = re.search("^(VISIBLE)$", splitWords[j])
            if(visibleKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("print keyword")
                else:
                    types[i+1].append("print keyword")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #GIMMEH Keyword
            gimmehKeyword = re.search("^(GIMMEH)$", splitWords[j])
            if(gimmehKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("input keyword")
                else:
                    types[i+1].append("input keyword")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #O RLY? Keyword
            if (splitWords[j] == "O"):
                oRlyKeyword = oRlyKeyword + splitWords[j] + " " 
                continue
            if (oRlyKeyword == "O "):
                if (splitWords[j].strip() == "RLY?"):
                    oRlyKeyword = oRlyKeyword + splitWords[j] + " "
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(oRlyKeyword)
                    else:
                        lexemes[i+1].append(oRlyKeyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("ifthen demiliter")
                    else:
                        types[i+1].append("ifthen demiliter")
                    
                    oRlyKeyword = ""
                    continue

            #YA RLY? Keyword
            if (splitWords[j] == "YA"):
                yaRlyKeyword = yaRlyKeyword + splitWords[j] + " " 
                continue
            if (yaRlyKeyword == "YA "):
                if (splitWords[j].strip() == "RLY"):
                    yaRlyKeyword = yaRlyKeyword + splitWords[j] + " "
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(yaRlyKeyword)
                    else:
                        lexemes[i+1].append(yaRlyKeyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("if win then operator")
                    else:
                        types[i+1].append("if win then operator")
                    
                    yaRlyKeyword = ""
                    continue

            #MEBBE Keyword
            mebbeKeyword = re.search("^(MEBBE)$", splitWords[j])
            if(mebbeKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("then operator")
                else:
                    types[i+1].append("then operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #NO WAI Keyword
            if (splitWords[j] == "NO"):
                noWaiKeyword = noWaiKeyword + splitWords[j] + " " 
                continue
            if (noWaiKeyword == "NO "):
                if (splitWords[j].strip() == "WAI"):
                    noWaiKeyword = noWaiKeyword + splitWords[j] + " "
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(noWaiKeyword)
                    else:
                        lexemes[i+1].append(noWaiKeyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("if fail then operator")
                    else:
                        types[i+1].append("if fail then operator")
                    
                    noWaiKeyword = ""
                    continue
            
            #OIC Keyword
            oicKeyword = re.search("^(OIC)$", splitWords[j])
            if(oicKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("ifthen delimiter")
                else:
                    types[i+1].append("ifthen delimiter")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #WTF Keyword
            wtfKeyword = re.search("^(WTF\?)$", splitWords[j])
            if(wtfKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("ifthen delimiter")
                else:
                    types[i+1].append("ifthen delimiter")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            #OMG Keyword
            omgKeyword = re.search("^(OMG)$", splitWords[j])
            if(omgKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("comparison delimiter")
                else:
                    types[i+1].append("comparison delimiter")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #OMGWTF Keyword
            omgwtfKeyword = re.search("^(OMGWTF)$", splitWords[j])
            if(omgwtfKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("default case operator")
                else:
                    types[i+1].append("default case operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #UPPIN Keyword
            uppinKeyword = re.search("^(UPPIN)$", splitWords[j])
            if(uppinKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("increment operator")
                else:
                    types[i+1].append("increment operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #NERFIN Keyword
            nerfinKeyword = re.search("^(NERFIN)$", splitWords[j])
            if(nerfinKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("decrement operator")
                else:
                    types[i+1].append("decrement operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #YR Keyword
            yrKeyword = re.search("^(YR)$", splitWords[j])
            if(yrKeyword and imYrKeyword== ""):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("identifier delimiter operator")
                else:
                    types[i+1].append("identifier delimiter operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #TIL Keyword
            tilKeyword = re.search("^(TIL)$", splitWords[j])
            if(tilKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("loop fail condition operator")
                else:
                    types[i+1].append("loop fail condition operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            #WILE Keyword
            wileKeyword = re.search("^(WILE)$", splitWords[j])
            if(wileKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("loop win condition operator")
                else:
                    types[i+1].append("loop win condition operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #IM IN/OUTTA YR Keyword
            if(splitWords[j] == "IM"):
                imYrKeyword = imYrKeyword + splitWords[j] + " "
                continue

            if(imYrKeyword == "IM "):
                if(splitWords[j] == "IN"):
                    imYrKeyword = imYrKeyword + splitWords[j] + " "
                    continue
                elif(splitWords[j] == "OUTTA"):
                    imYrKeyword = imYrKeyword + splitWords[j] + " " 
                    continue
               
            if(imYrKeyword == "IM IN "):
                if(splitWords[j] == "YR"):
                    imYrKeyword = imYrKeyword + splitWords[j]
                    if(imYrKeyword == "IM IN YR"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(imYrKeyword)
                        else:
                            lexemes[i+1].append(imYrKeyword)
                    
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("loop delimiter")
                        else:
                            types[i+1].append("loop delimiter")
                        
                        imYrKeyword = ""
                        continue
                        if(splitWords[j] == "YR"):
                            imYrKeyword = imYrKeyword + splitWords[j]
            elif(imYrKeyword == "IM OUTTA "):
                if(splitWords[j] == "YR"):
                    imYrKeyword = imYrKeyword + splitWords[j]
                    if(imYrKeyword == "IM OUTTA YR"):
                        if(i+1 not in lexemes):
                            lexemes[i+1] = []
                            lexemes[i+1].append(imYrKeyword)
                        else:
                            lexemes[i+1].append(imYrKeyword)
                    
                        if(i+1 not in types):
                            types[i+1] = []
                            types[i+1].append("loop delimiter")
                        else:
                            types[i+1].append("loop delimiter")
                        
                        imYrKeyword = ""
                    else:
                        imYrKeyword = ""

            #GTFO Keyword
            gtfoKeyword = re.search("^(GTFO)$", splitWords[j])
            if(gtfoKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("break operator")
                else:
                    types[i+1].append("break operator")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #AN Keyword
            anKeyword = re.search("^(AN)$", splitWords[j])
            if(anKeyword):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])
            
                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("argument separator keyword")
                else:
                    types[i+1].append("argument separator keyword")
                continue
            else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""

            #catches identifiers
            identifier = re.search("^[a-zA-Z][a-zA-Z0-9_]*$", splitWords[j])
            if(identifier):
                if(i+1 not in lexemes):
                    lexemes[i+1] = []
                    lexemes[i+1].append(splitWords[j])
                else:
                    lexemes[i+1].append(splitWords[j])

                if(i+1 not in types):
                    types[i+1] = []
                    types[i+1].append("identifier")
                else:
                    types[i+1].append("identifier")

                continue

def printSymbolTable():
    space1 = 40
    space2 = 40
    space3 = 10

    # for typeTemp in symbolTable.keys():
    #     for lexeme in symbolTable[typeTemp].keys():
    #         print("Lexeme: " + lexeme, end=(" " * (space1 - len(lexeme))))
    #         print("Type: " + typeTemp, end=(" " * (space2 - len(typeTemp))))
    #         print("Count: " + str(symbolTable[typeTemp][lexeme][0]), end=(" " * (space3 - len(str(symbolTable[typeTemp][lexeme][0])))))
    #         print("")

    for i in lexemes.keys():
        print("Line " + str(i))
        for j in range(0, len(lexemes[i])):
            print("Lexeme: " + lexemes[i][j], end=(" " * (space1 - len(lexemes[i][j]))))
            print("Type: " + types[i][j], end=(" " * (space2 - len(types[i][j]))))
            print("")
        print("")

def getLines():
    return lines

def getLexemes():
    return lexemes

def getType():
    return types

#MAIN CODE
lexemes = {}
types = {}

lines = readFile(filename)
findLexemes(lines)

# for i in lexemes.keys():
#     print("[" + str(i) + "] " + str(lexemes[i]))
# print("")
# for i in types.keys():
#     print("[" + str(i) + "] " + str(types[i]))

#printSymbolTable()
