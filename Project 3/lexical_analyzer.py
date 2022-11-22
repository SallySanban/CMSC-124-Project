import re

filename = "Project 3/samplecodewrong.txt"

#reads file and cleans each line in the file
def readFile(filename):
    file = open(filename)
    lines = []

    #print(file.readlines())

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
    keywords = ["HAI",
                "KTHXBYE",
                "OBTW",
                "BTW",
                "TLDR",
                "I",
                "HAS",
                "A",
                "ITZ",
                "R",
                "SUM",
                "OF",
                "DIFF",
                "PRODUKT",
                "QUOSHUNT",
                "MOD",
                "BIGGR",
                "SMALLR",
                "BOTH",
                "EITHER",
                "WON",
                "NOT",
                "ANY",
                "ALL",
                "SAEM",
                "DIFFRINT",
                "SMOOSH",
                "MAEK",
                "AN",
                "IS",
                "NOW",
                "VISIBLE",
                "GIMMEH",
                "O",
                "RLY?",
                "YA",
                "RLY",
                "MEBBE",
                "NO",
                "WAI",
                "OIC",
                "WTF?",
                "OMG",
                "OMGWTF",
                "IM",
                "IN",
                "UPPIN",
                "NERFIN",
                "OUTTA",
                "YR",
                "TIL",
                "WILE",
                "GTFO",
                "MKAY",
                "WIN",
                "FAIL",
                "TROOF",
                "NOOB",
                "NUMBR",
                "NUMBAR",
                "YARN",
                "TYPE"
                ]
    stringFound = False
    singleCommentFound = False
    multiCommentFound = False
    keywordFound = False
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
            if (splitWords[j].strip() == "I"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "I" or keyword =="I HAS")):
                # print(keyword)              # CHECKER
                # print("HEHEH")
                if (splitWords[j].strip() == "HAS"):
                    keyword = keyword + " " + "HAS"
                    continue
                elif (splitWords[j].strip() == "A"):
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
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
                    continue

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
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
                    continue
            
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
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
                    continue
            
            # PRODUKT OF KEYWORD
            if (splitWords[j].strip() == "PRODUKT" and (keyword == "PRODUKT")):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and len(keyword) != 0):
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
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # ALL OF KEYWORD
            if (splitWords[j].strip() == "ALL"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "ALL")):
                if (splitWords[j] == "OF"):
                    keyword = keyword + " " + "OF"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("infinite arity AND operator")
                    else:
                        types[i+1].append("infinite arity AND operator")
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
            
            # BOTH SAEM KEYWORD
            if (splitWords[j].strip() == "BOTH"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "BOTH")):
                if (splitWords[j] == "SAEM"):
                    keyword = keyword + " " + "OF"
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
            
            aKeyword = re.search("^(A)$", splitWords[j])
            if(aKeyword):
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

            # IS NOW A KEYWORD      CURRENTLY NOT WORKING
            if (splitWords[j].strip() == "IS"):
                keywordFound = True
                keyword = keyword + splitWords[j]
                continue

            if (keywordFound == True and (keyword == "IS" or keyword =="IS NOW")):
                print(keyword)  
                if (splitWords[j].strip() == "NOW"):
                    keyword = keyword + " " + "NOW"
                    continue
                elif (splitWords[j].strip() == "A"):
                    keyword = keyword + " " + "A"
                    if(i+1 not in lexemes):
                        lexemes[i+1] = []
                        lexemes[i+1].append(keyword)
                    else:
                        lexemes[i+1].append(keyword)
                    
                    if(i+1 not in types):
                        types[i+1] = []
                        types[i+1].append("typecasting keyword")
                    else:
                        types[i+1].append("typecasting keyword")
                    continue
                else:
                    keywordFound == False        # NOT FOUND -> WRONG SYNTAX
                    keyword = ""
                    continue
            # isNowAKeyword = re.findall("(IS\ NOW\ A)", lines[i])                          # IS NOW A (changed regex here to catch in betweens)
            # if (len(isNowAKeyword) != 0):
            #     if (symbolTable['typecasting keyword'].get(isNowAKeyword[0])):           
            #         symbolTable['typecasting keyword']["IS NOW A"][0] += len(isNowAKeyword)
            #     else:
            #         symbolTable['typecasting keyword'][isNowAKeyword[0]] = [len(isNowAKeyword)]

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
            # oRlyKeyword = re.findall("(O\ RLY\?)", lines[i])                            # O RLY?
            # if (len(oRlyKeyword) != 0):
            #     if (symbolTable['ifthen keyword'].get(oRlyKeyword[0])):
            #         symbolTable['ifthen keyword']["O RLY ?"][0] += len(oRlyKeyword)
            #     else:
            #         symbolTable['ifthen keyword'][oRlyKeyword[0]] = [len(oRlyKeyword)]

            # yaRlyKeyword = re.findall("^(YA\ RLY)", lines[i])                           # YA RLY
            # if (len(yaRlyKeyword) != 0):
            #     if (symbolTable['ifthen win keyword'].get(yaRlyKeyword[0])):
            #         symbolTable['ifthen win keyword']["YA RLY"][0] += len(yaRlyKeyword)
            #     else:
            #         symbolTable['ifthen win keyword'][yaRlyKeyword[0]] = [len(yaRlyKeyword)]

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

            # noWaiKeyword = re.findall("^(NO\ WAI)", lines[i])                           # NO WAI
            # if (len(noWaiKeyword) != 0):
            #     if (symbolTable['ifthen fail keyword'].get(noWaiKeyword[0])):
            #         symbolTable['ifthen fail keyword']["NO WAI"][0] += len(noWaiKeyword)
            #     else:
            #         symbolTable['ifthen fail keyword'][noWaiKeyword[0]] = [len(noWaiKeyword)]

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

            # imInYrKeyword = re.findall("^(IM\ IN\ YR)", lines[i])                        # IM IN YR
            # if (len(imInYrKeyword) != 0):
            #     if (symbolTable['loop keyword'].get(imInYrKeyword[0])):
            #         symbolTable['loop keyword']["IM IN YR"][0] += len(imInYrKeyword)
            #     else:
            #         symbolTable['loop keyword'][imInYrKeyword[0]] = [len(imInYrKeyword)]

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

            yrKeyword = re.search("^(YR)$", splitWords[j])
            if(yrKeyword):
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

            # imOuttaYrKeyword = re.findall("^(IM\ OUTTA\ YR)", lines[i])                   # IM OUTTA YR
            # if (len(imOuttaYrKeyword) != 0):
            #     if (symbolTable['loop exit keyword'].get(imOuttaYrKeyword[0])):
            #         symbolTable['loop exit keyword']["IM OUTTA YR"][0] += len(imOuttaYrKeyword)
            #     else:
            #         symbolTable['loop exit keyword'][imOuttaYrKeyword[0]] = [len(imOuttaYrKeyword)]

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
            if(splitWords[j] in keywords): #will delete this block when keywords are added above (not neccesary anymore)
                continue

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
#cinomment ko lang para may reference kayo sa types na iaappend niyo pero idedelete ko rin mamaya
# symbolTable = {
#                 "comment": {},
#                 "identifier": {},
#                 "NUMBR literal": {},
#                 "NUMBAR literal": {},
#                 "YARN literal": {},
#                 "string delimiter": {},
#                 "TROOF literal": {},
#                 "TYPE literal": {},
#                 "code delimiter": {},
#                 "single comment delimiter": {},
#                 "multi comment delimiter": {},
#                 "variable declaration": {},
#                 "variable initialization": {},
#                 "assignment operator": {},
#                 "add operator": {},
#                 "subtract operator": {},
#                 "multiply operator": {},
#                 "divide operator": {},
#                 "modulo operator": {},
#                 "max operator": {},
#                 "min operator": {},
#                 "and operator": {},
#                 "or operator": {},
#                 "xor operator": {},
#                 "not operator": {},
#                 "infinite arity OR operator": {},
#                 "infinite arity AND operator": {},
#                 "is equal comparison": {},
#                 "not equal comparison": {},
#                 "concatenation keyword":{},
#                 "typecasting keyword":{},
#                 "explicit cast keyword":{},
#                 "print keyword":{},
#                 "input keyword":{},
#                 "ifthen keyword":{},
#                 "ifthen win keyword":{},
#                 "ifthen fail keyword": {},
#                 "elseif keyword": {},
#                 "ifthen exit keyword": {},
#                 "switch case keyword": {},
#                 "comparison start keyword": {},
#                 "default case keyword": {},
#                 "loop keyword": {},
#                 "increment operator": {},
#                 "decrement operator": {},
#                 "iterator keyword": {},
#                 "loop until operator": {},
#                 "loop while operator": {},
#                 "loop exit keyword": {},
#                 "loop break keyword": {},
#                 "infinite arity keyword": {},
#                 "argument separator keyword": {},
#                 "type keyword": {},
#             }

lexemes = {}
types = {}

lines = readFile(filename)
findLexemes(lines)

# for i in lexemes.keys():
#     print("[" + str(i) + "] " + str(lexemes[i]))
# print("")
# for i in types.keys():
#     print("[" + str(i) + "] " + str(types[i]))

printSymbolTable()
