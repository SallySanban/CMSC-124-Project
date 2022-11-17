import re

filename = "F:\Documents\CMSC 124\Project\CMSC-124-Project\Project 3\samplecodecomments.txt"

#reads file and cleans each line in the file
def readFile(filename):
    file = open(filename)
    lines = []

    #reads the file and places each line in a list
    for line in file.readlines():
        words = line.split("\n")
        for i in words:
            lines.append(i)

    #gets rid of leading whitespaces in each line
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()

    for i in lines:
        if(i == ""):
            lines.remove(i)
        
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
                "BOTH",
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
    singleComment = ""
    multiComment = ""

    for i in range(0, len(lines)):
        #catches single comments
        singleCommentWords = lines[i].split()
        for j in range(0, len(singleCommentWords)):
            if(singleCommentWords[j] == "BTW"):
                singleCommentFound = True
                continue
            
            if(singleCommentFound == True):
                singleComment = singleComment + singleCommentWords[j] + " "
                singleCommentWords[j] = ""
                
                if(j == len(singleCommentWords)-1):
                    singleCommentFound = False

                    if(singleComment != ""):
                        if (symbolTable['comment'].get(singleComment)):
                                symbolTable['comment'][singleComment][0] += 1
                        else:
                            symbolTable['comment'][singleComment] = [1]
                    
                    singleComment = ""
        
        lines[i] = (" ").join(singleCommentWords) #[2]

        #catches multi comments
        multiCommentWords = lines[i].split()
        for j in range(0, len(multiCommentWords)):
            if(multiCommentWords[j] == "OBTW"):
                multiCommentFound = True
                continue
            
            if(multiCommentFound == True):
                if(multiCommentWords[j] == "TLDR"):
                    multiCommentFound = False

                    if(multiComment != ""):
                        if (symbolTable['comment'].get(multiComment)):
                                symbolTable['comment'][multiComment][0] += 1
                        else:
                            symbolTable['comment'][multiComment] = [1]
                    
                    multiComment = ""

                    break

                multiComment = multiComment + multiCommentWords[j] + " "
                multiCommentWords[j] = ""
        
        lines[i] = (" ").join(multiCommentWords)

        #catches identifiers
        words = lines[i].split()
        for j in range(0, len(words)):
            if('\"' in words[j]):
                stringFound = True

            if(stringFound == True):
                words[j] = ""

                if('\"' in words[j] or j == len(words)-1):
                    stringFound = False
                
        for j in range(0, len(words)):
            if(words[j] in keywords):
                words[j] = ""
        
        for k in words:
            identifier = re.search("^[a-zA-Z][a-zA-Z0-9_]*$", k)
            if(identifier):
                if (symbolTable['identifier'].get(k)):
                        symbolTable['identifier'][k][0] += 1
                else:
                    symbolTable['identifier'][k] = [1]
                    
        #catches literals
        literals = lines[i].split()
        for j in literals:
            numbrLiteral = re.findall("^[-]?\d+$", j)
            if(numbrLiteral):
                for j in numbrLiteral:
                    if (symbolTable['NUMBR literal'].get(j)):
                        symbolTable['NUMBR literal'][j][0] += 1
                    else:
                        symbolTable['NUMBR literal'][j] = [1]

            numbarLiteral = re.findall("^[-]?\d+[.]\d+$", j)
            if(numbarLiteral):
                for j in numbarLiteral:
                    if (symbolTable['NUMBAR literal'].get(j)):
                        symbolTable['NUMBAR literal'][j][0] += 1
                    else:
                        symbolTable['NUMBAR literal'][j] = [1]
            
            troofLiteral = re.findall("^(WIN)$|^(FAIL)$", j)
            troofLiteral = [tuple(l for l in k if l)[-1] for k in troofLiteral] #[1]
            if(troofLiteral):
                for j in troofLiteral:
                    if (symbolTable['TROOF literal'].get(j)):
                        symbolTable['TROOF literal'][j][0] += 1
                    else:
                        symbolTable['TROOF literal'][j] = [1]

            typeLiteral = re.findall("^(TROOF)$|^(NOOB)$|^(NUMBR)$|^(NUMBAR)$|^(YARN)$|^(TYPE)$", j)
            typeLiteral = [tuple(l for l in k if l)[-1] for k in typeLiteral]
            if(typeLiteral):
                for j in typeLiteral:
                    if (symbolTable['TYPE literal'].get(j)):
                        symbolTable['TYPE literal'][j][0] += 1
                    else:
                        symbolTable['TYPE literal'][j] = [1]

        #catches yarn and string delimiter
        yarnLiteral = re.findall("\"[^\"]*\"", lines[i])
        if(yarnLiteral):
            for j in yarnLiteral:
                if (symbolTable['YARN literal'].get(j.strip()[1:len(j.strip())-1])):
                    symbolTable['YARN literal'][j.strip()[1:len(j.strip())-1]][0] += 1
                else:
                    symbolTable['YARN literal'][j.strip()[1:len(j.strip())-1]] = [1]
                
                if (symbolTable['string delimiter'].get('\"')):
                    symbolTable['string delimiter']['\"'][0] += 2
                else:
                    symbolTable['string delimiter']['\"'] = [2]
        
        haiKeyword = re.findall("^(HAI)", lines[i])                        # HAI
        if (len(haiKeyword) != 0):
            if (symbolTable['code delimiter'].get(haiKeyword[0])):
                symbolTable['code delimiter'][haiKeyword[0]][0] += len(haiKeyword)
            else:
                symbolTable['code delimiter'][haiKeyword[0]] = [len(haiKeyword)]

        kThxByeKeyword = re.findall("^(KTHXBYE)$", lines[i])               # KTHXBYE
        if (len(kThxByeKeyword) != 0):
            if (symbolTable['code delimiter'].get(kThxByeKeyword[0])):
                symbolTable['code delimiter'][kThxByeKeyword[0]][0] += len(kThxByeKeyword)
            else:
                symbolTable['code delimiter'][kThxByeKeyword[0]] = [len(kThxByeKeyword)]

        btwKeyword = re.findall("[^O](BTW)", lines[i])                        # BTW (be able to coexist with others)
        if (len(btwKeyword) != 0):
            if (symbolTable['single comment delimiter'].get(btwKeyword[0])):
                symbolTable['single comment delimiter'][btwKeyword[0]][0] += len(btwKeyword)
            else:
                symbolTable['single comment delimiter'][btwKeyword[0]] = [len(btwKeyword)]

        obtwKeyword = re.findall("^(OBTW)", lines[i])                        # OBTW (own line & first)
        if (len(obtwKeyword) != 0):
            if (symbolTable['multi comment delimiter'].get(obtwKeyword[0])):
                symbolTable['multi comment delimiter'][obtwKeyword[0]][0] += len(obtwKeyword)
            else:
                symbolTable['multi comment delimiter'][obtwKeyword[0]] = [len(obtwKeyword)]

        tldrKeyword = re.findall("^(TLDR)", lines[i])                        # TLDR (own line & only first)
        if (len(tldrKeyword) != 0):
            if (symbolTable['multi comment delimiter'].get(tldrKeyword[0])):
                symbolTable['multi comment delimiter']["TLDR"][0] += len(tldrKeyword)
            else:
                symbolTable['multi comment delimiter'][tldrKeyword[0]] = [len(tldrKeyword)]
        
        iHasAKeyword = re.findall("^(I\ HAS\ A)", lines[i])                  # I HAS A (first)
        if (len(iHasAKeyword) != 0):
            if (symbolTable['variable declaration'].get(iHasAKeyword[0])):
                symbolTable['variable declaration']["I HAS A"][0] += len(iHasAKeyword)
            else:
                symbolTable['variable declaration'][iHasAKeyword[0]] = [len(iHasAKeyword)]

        itzKeyword = re.findall("( ITZ )", lines[i])                          # ITZ
        if (len(itzKeyword) != 0):
            if (symbolTable['variable initialization'].get(itzKeyword[0].strip())):
                symbolTable['variable initialization']["ITZ"][0] += len(itzKeyword)
            else:
                symbolTable['variable initialization'][itzKeyword[0].strip()] = [len(itzKeyword)]
        
        rKeyword = re.findall("( R )", lines[i])                          # R
        if (len(rKeyword) != 0):
            if (symbolTable['assignment operator'].get(rKeyword[0].strip())):           # Used the strip to remove leading and trailing whitespaces         (To catch only the letter)
                symbolTable['assignment operator']["R"][0] += len(rKeyword)
            else:
                symbolTable['assignment operator'][rKeyword[0].strip()] = [len(rKeyword)]

        sumOfKeyword = re.findall("(SUM\ OF)", lines[i])                          # SUM OF (between)
        if (len(sumOfKeyword) != 0):
          if (symbolTable['add operator'].get(sumOfKeyword[0])):           
              symbolTable['add operator']["SUM OF"][0] += len(sumOfKeyword)
          else:
              symbolTable['add operator'][sumOfKeyword[0]] = [len(sumOfKeyword)]

        diffOfKeyword = re.findall("(DIFF\ OF)", lines[i])                          # DIFF OF (between)
        if (len(diffOfKeyword) != 0):
            if (symbolTable['subtract operator'].get(diffOfKeyword[0])):           
                symbolTable['subtract operator']["DIFF OF"][0] += len(diffOfKeyword)
            else:
                symbolTable['subtract operator'][diffOfKeyword[0]] = [len(diffOfKeyword)]
        
        produktOfKeyword = re.findall("(PRODUKT\ OF)", lines[i])                          # PRODUKT OF (between)
        if (len(produktOfKeyword) != 0):
            if (symbolTable['multiply operator'].get(produktOfKeyword[0])):           
                symbolTable['multiply operator']["PRODUKT OF"][0] += len(produktOfKeyword)
            else:
                symbolTable['multiply operator'][produktOfKeyword[0]] = [len(produktOfKeyword)]
        
        quoshuntOfKeyword = re.findall("(QUOSHUNT\ OF)", lines[i])                          # QUOSHUNT OF (between)
        if (len(quoshuntOfKeyword) != 0):
            if (symbolTable['divide operator'].get(quoshuntOfKeyword[0])):           
                symbolTable['divide operator']["QUOSHUNT OF"][0] += len(quoshuntOfKeyword)
            else:
                symbolTable['divide operator'][quoshuntOfKeyword[0]] = [len(quoshuntOfKeyword)]

        modOfKeyword = re.findall("(MOD\ OF)", lines[i])                          # MOD OF (between)
        if (len(modOfKeyword) != 0):
            if (symbolTable['modulo operator'].get(modOfKeyword[0])):           
                symbolTable['modulo operator']["MOD OF"][0] += len(modOfKeyword)
            else:
                symbolTable['modulo operator'][modOfKeyword[0]] = [len(modOfKeyword)]
        
        biggrOfKeyword = re.findall("(BIGGR\ OF)", lines[i])                          # BIGGR OF (between)
        if (len(biggrOfKeyword) != 0):
            if (symbolTable['max operator'].get(biggrOfKeyword[0])):           
                symbolTable['max operator']["BIGGR OF"][0] += len(biggrOfKeyword)
            else:
                symbolTable['max operator'][biggrOfKeyword[0]] = [len(biggrOfKeyword)]
        
        smallrOfKeyword = re.findall("(SMALLR\ OF)", lines[i])                          # SMALLR OF (between)
        if (len(smallrOfKeyword) != 0):
            if (symbolTable['min operator'].get(smallrOfKeyword[0])):           
                symbolTable['min operator']["SMALLR OF"][0] += len(smallrOfKeyword)
            else:
                symbolTable['min operator'][smallrOfKeyword[0]] = [len(smallrOfKeyword)]
        
        bothOfKeyword = re.findall("(BOTH\ OF)", lines[i])                          # BOTH OF (between)
        if (len(bothOfKeyword) != 0):
            if (symbolTable['and operator'].get(bothOfKeyword[0])):           
                symbolTable['and operator']["BOTH OF"][0] += len(bothOfKeyword)
            else:
                symbolTable['and operator'][bothOfKeyword[0]] = [len(bothOfKeyword)]
        
        eitherOfKeyword = re.findall("(EITHER\ OF)", lines[i])                          # EITHER OF (between)
        if (len(eitherOfKeyword) != 0):
            if (symbolTable['or operator'].get(eitherOfKeyword[0])):           
                symbolTable['or operator']["EITHER OF"][0] += len(eitherOfKeyword)
            else:
                symbolTable['or operator'][eitherOfKeyword[0]] = [len(eitherOfKeyword)]
        
        wonOfKeyword = re.findall("(WON\ OF)", lines[i])                          # WON OF (between)
        if (len(wonOfKeyword) != 0):
            if (symbolTable['xor operator'].get(wonOfKeyword[0])):           
                symbolTable['xor operator']["WON OF"][0] += len(wonOfKeyword)
            else:
                symbolTable['xor operator'][wonOfKeyword[0]] = [len(wonOfKeyword)]
        
        notKeyword = re.findall("(NOT)", lines[i])                          # NOT (between)
        if (len(notKeyword) != 0):
            if (symbolTable['not operator'].get(notKeyword[0])):           
                symbolTable['not operator']["NOT"][0] += len(notKeyword)
            else:
                symbolTable['not operator'][notKeyword[0]] = [len(notKeyword)]
        
        anyOfKeyword = re.findall("^(ANY\ OF)", lines[i])                          # ANY OF (first)
        if (len(anyOfKeyword) != 0):
            if (symbolTable['infinite arity OR operator'].get(anyOfKeyword[0])):           
                symbolTable['infinite arity OR operator']["ANY OF"][0] += len(anyOfKeyword)
            else:
                symbolTable['infinite arity OR operator'][anyOfKeyword[0]] = [len(anyOfKeyword)]
        
        allOfKeyword = re.findall("^(ALL\ OF)", lines[i])                          # ALL OF (first)
        if (len(allOfKeyword) != 0):
            if (symbolTable['infinite arity AND operator'].get(allOfKeyword[0])):           
                symbolTable['infinite arity AND operator']["ALL OF"][0] += len(allOfKeyword)
            else:
                symbolTable['infinite arity AND operator'][allOfKeyword[0]] = [len(allOfKeyword)]

        bothSaemKeyword = re.findall("^(BOTH\ SAEM)", lines[i])                          # BOTH SAEM (first)
        if (len(bothSaemKeyword) != 0):
            if (symbolTable['is equal comparison'].get(bothSaemKeyword[0])):           
                symbolTable['is equal comparison']["BOTH SAEM"][0] += len(bothSaemKeyword)
            else:
                symbolTable['is equal comparison'][bothSaemKeyword[0]] = [len(bothSaemKeyword)]

        diffrintKeyword = re.findall("^(DIFFRINT)", lines[i])                          # DIFFRINT
        if (len(diffrintKeyword) != 0):
            if (symbolTable['not equal comparison'].get(diffrintKeyword[0])):           
                symbolTable['not equal comparison']["DIFFRINT"][0] += len(diffrintKeyword)
            else:
                symbolTable['not equal comparison'][diffrintKeyword[0]] = [len(diffrintKeyword)]
        
        smooshKeyword = re.findall("^(SMOOSH)", lines[i])                              # SMOOSH
        if (len(smooshKeyword) != 0):
            if (symbolTable['concatenation keyword'].get(smooshKeyword[0])):           
                symbolTable['concatenation keyword']["SMOOSH"][0] += len(smooshKeyword)
            else:
                symbolTable['concatenation keyword'][smooshKeyword[0]] = [len(smooshKeyword)]

        isNowAKeyword = re.findall("(IS\ NOW\ A)", lines[i])                          # IS NOW A (changed regex here to catch in betweens)
        if (len(isNowAKeyword) != 0):
            if (symbolTable['typecasting keyword'].get(isNowAKeyword[0])):           
                symbolTable['typecasting keyword']["IS NOW A"][0] += len(isNowAKeyword)
            else:
                symbolTable['typecasting keyword'][isNowAKeyword[0]] = [len(isNowAKeyword)]

        visibleKeyword = re.findall("^(VISIBLE)", lines[i])                          # VISIBLE
        if (len(visibleKeyword) != 0):
            if (symbolTable['print keyword'].get(visibleKeyword[0])):
                symbolTable['print keyword']["VISIBLE"][0] += len(visibleKeyword)
            else:
                symbolTable['print keyword'][visibleKeyword[0]] = [len(visibleKeyword)]

        gimmehKeyword = re.findall("^(GIMMEH)", lines[i])                            # GIMMEH
        if (len(gimmehKeyword) != 0):
            if (symbolTable['input keyword'].get(gimmehKeyword[0])):
                symbolTable['input keyword']["GIMMEH"][0] += len(gimmehKeyword)
            else:
                symbolTable['input keyword'][gimmehKeyword[0]] = [len(gimmehKeyword)]

        oRlyKeyword = re.findall("(O\ RLY\?)", lines[i])                            # O RLY?
        if (len(oRlyKeyword) != 0):
            if (symbolTable['ifthen keyword'].get(oRlyKeyword[0])):
                symbolTable['ifthen keyword']["O RLY ?"][0] += len(oRlyKeyword)
            else:
                symbolTable['ifthen keyword'][oRlyKeyword[0]] = [len(oRlyKeyword)]

        yaRlyKeyword = re.findall("^(YA\ RLY)", lines[i])                           # YA RLY
        if (len(yaRlyKeyword) != 0):
            if (symbolTable['ifthen win keyword'].get(yaRlyKeyword[0])):
                symbolTable['ifthen win keyword']["YA RLY"][0] += len(yaRlyKeyword)
            else:
                symbolTable['ifthen win keyword'][yaRlyKeyword[0]] = [len(yaRlyKeyword)]

        mebbeKeyword = re.findall("^(MEBBE)", lines[i])                             # MEBBE
        if (len(mebbeKeyword) != 0):
            if (symbolTable['elseif keyword'].get(mebbeKeyword[0])):
                symbolTable['elseif keyword']["MEBBE"][0] += len(mebbeKeyword)
            else:
                symbolTable['elseif keyword'][mebbeKeyword[0]] = [len(mebbeKeyword)]

        noWaiKeyword = re.findall("^(NO\ WAI)", lines[i])                           # NO WAI
        if (len(noWaiKeyword) != 0):
            if (symbolTable['ifthen fail keyword'].get(noWaiKeyword[0])):
                symbolTable['ifthen fail keyword']["NO WAI"][0] += len(noWaiKeyword)
            else:
                symbolTable['ifthen fail keyword'][noWaiKeyword[0]] = [len(noWaiKeyword)]

        oicKeyword = re.findall("^(OIC)", lines[i])                                  # OIC
        if (len(oicKeyword) != 0):
            if (symbolTable['ifthen exit keyword'].get(oicKeyword[0])):
                symbolTable['ifthen exit keyword']["OIC"][0] += len(oicKeyword)
            else:
                symbolTable['ifthen exit keyword'][oicKeyword[0]] = [len(oicKeyword)]
        
        wtfKeyword = re.findall("^(WTF\?)", lines[i])                                # WTF?
        if (len(wtfKeyword) != 0):
            if (symbolTable['switch case keyword'].get(wtfKeyword[0])):
                symbolTable['switch case keyword']["WTF"][0] += len(wtfKeyword)
            else:
                symbolTable['switch case keyword'][wtfKeyword[0]] = [len(wtfKeyword)]

        omgKeyword = re.findall("^(OMG)", lines[i])                                  # OMG
        if (len(omgKeyword) != 0):
            if (symbolTable['comparison start keyword'].get(omgKeyword[0])):
                symbolTable['comparison start keyword']["OMG"][0] += len(omgKeyword)
            else:
                symbolTable['comparison start keyword'][omgKeyword[0]] = [len(omgKeyword)]
        
        omgwtfKeyword = re.findall("^(OMGWTF)", lines[i])                            # OMGWTF
        if (len(omgwtfKeyword) != 0):
            if (symbolTable['default case keyword'].get(omgwtfKeyword[0])):
                symbolTable['default case keyword']["OMGWTF"][0] += len(omgwtfKeyword)
            else:
                symbolTable['default case keyword'][omgwtfKeyword[0]] = [len(omgwtfKeyword)]

        imInYrKeyword = re.findall("^(IM\ IN\ YR)", lines[i])                        # IM IN YR
        if (len(imInYrKeyword) != 0):
            if (symbolTable['loop keyword'].get(imInYrKeyword[0])):
                symbolTable['loop keyword']["IM IN YR"][0] += len(imInYrKeyword)
            else:
                symbolTable['loop keyword'][imInYrKeyword[0]] = [len(imInYrKeyword)]

        uppinKeyword = re.findall("(UPPIN)", lines[i])                        # UPPIN
        if (len( uppinKeyword) != 0):
            if (symbolTable['increment operator'].get( uppinKeyword[0])):
                symbolTable['increment operator']["UPPIN"][0] += len(uppinKeyword)
            else:
                symbolTable['increment operator'][ uppinKeyword[0]] = [len(uppinKeyword)]

        nerfinKeyword = re.findall("(NERFIN)", lines[i])                       # NERFIN
        if (len(nerfinKeyword) != 0):
            if (symbolTable['decrement operator'].get(nerfinKeyword[0])):
                symbolTable['decrement operator']["NERFIN"][0] += len(nerfinKeyword)
            else:
                symbolTable['decrement operator'][nerfinKeyword[0]] = [len(nerfinKeyword)]

        yrKeyword = re.findall("(YR)", lines[i])                                # YR
        if (len(yrKeyword) != 0):
            if (symbolTable['iterator keyword'].get(yrKeyword[0])):
                symbolTable['iterator keyword']["YR"][0] += len(yrKeyword)
            else:
                symbolTable['iterator keyword'][yrKeyword[0]] = [len(yrKeyword)]

        tilKeyword = re.findall("(TIL)", lines[i])                                # TIL
        if (len(tilKeyword) != 0):
            if (symbolTable['loop until operator'].get(tilKeyword[0])):
                symbolTable['loop until operator']["TIL"][0] += len(tilKeyword)
            else:
                symbolTable['loop until operator'][tilKeyword[0]] = [len(tilKeyword)]

        wileKeyword = re.findall("(WILE)", lines[i])                                # WILE
        if (len(wileKeyword) != 0):
            if (symbolTable['loop while operator'].get(wileKeyword[0])):
                symbolTable['loop while operator']["WILE"][0] += len(wileKeyword)
            else:
                symbolTable['loop while operator'][wileKeyword[0]] = [len(wileKeyword)]

        imOuttaYrKeyword = re.findall("^(IM\ OUTTA\ YR)", lines[i])                   # IM OUTTA YR
        if (len(imOuttaYrKeyword) != 0):
            if (symbolTable['loop exit keyword'].get(imOuttaYrKeyword[0])):
                symbolTable['loop exit keyword']["IM OUTTA YR"][0] += len(imOuttaYrKeyword)
            else:
                symbolTable['loop exit keyword'][imOuttaYrKeyword[0]] = [len(imOuttaYrKeyword)]

        gtfoKeyword = re.findall("^(GTFO)", lines[i])                               # GTFO
        if (len(gtfoKeyword) != 0):
            if (symbolTable['loop break keyword'].get(gtfoKeyword[0])):
                symbolTable['loop break keyword']["GTFO"][0] += len(gtfoKeyword)
            else:
                symbolTable['loop break keyword'][gtfoKeyword[0]] = [len(gtfoKeyword)]

        mkayKeyword = re.findall("(MKAY)", lines[i])                               # MKAY
        if (len(mkayKeyword) != 0):
            if (symbolTable['infinite arity keyword'].get(mkayKeyword[0])):
                symbolTable['infinite arity keyword']["MKAY"][0] += len(mkayKeyword)
            else:
                symbolTable['infinite arity keyword'][mkayKeyword[0]] = [len(mkayKeyword)]

        aKeyword = re.findall("(A)", lines[i])                               # A
        if (len(aKeyword) != 0):
            if (symbolTable['keyword'].get(aKeyword[0])):
                symbolTable['keyword']["A"][0] += len(aKeyword)
            else:
                symbolTable['keyword'][aKeyword[0]] = [len(aKeyword)]

        anKeyword = re.findall("(AN)", lines[i])                               # AN
        if (len(anKeyword) != 0):
            if (symbolTable['argument separator keyword'].get(anKeyword[0])):
                symbolTable['argument separator keyword']["AN"][0] += len(anKeyword)
            else:
                symbolTable['argument separator keyword'][anKeyword[0]] = [len(anKeyword)]
        
        #add other cases here

def printSymbolTable():
    space1 = 40
    space2 = 40
    space3 = 10

    for typeTemp in symbolTable.keys():
        for lexeme in symbolTable[typeTemp].keys():
            print("Lexeme: " + lexeme, end=(" " * (space1 - len(lexeme))))
            print("Type: " + typeTemp, end=(" " * (space2 - len(typeTemp))))
            print("Count: " + str(symbolTable[typeTemp][lexeme][0]), end=(" " * (space3 - len(str(symbolTable[typeTemp][lexeme][0])))))
            print("")

    
#MAIN CODE
symbolTable = {
                "comment": {},
                "identifier": {},
                "NUMBR literal": {},
                "NUMBAR literal": {},
                "YARN literal": {},
                "string delimiter": {},
                "TROOF literal": {},
                "TYPE literal": {},
                "code delimiter": {},
                "single comment delimiter": {},
                "multi comment delimiter": {},
                "variable declaration": {},
                "variable initialization": {},
                "assignment operator": {},
                "add operator": {},
                "subtract operator": {},
                "multiply operator": {},
                "divide operator": {},
                "modulo operator": {},
                "max operator": {},
                "min operator": {},
                "and operator": {},
                "or operator": {},
                "xor operator": {},
                "not operator": {},
                "infinite arity OR operator": {},
                "infinite arity AND operator": {},
                "is equal comparison": {},
                "not equal comparison": {},
                "concatenation keyword":{},
                "typecasting keyword":{},
                "print keyword":{},
                "input keyword":{},
                "ifthen keyword":{},
                "ifthen win keyword":{},
                "ifthen fail keyword": {},
                "elseif keyword": {},
                "ifthen exit keyword": {},
                "switch case keyword": {},
                "comparison start keyword": {},
                "default case keyword": {},
                "loop keyword": {},
                "increment operator": {},
                "decrement operator": {},
                "iterator keyword": {},
                "loop until operator": {},
                "loop while operator": {},
                "loop exit keyword": {},
                "loop break keyword": {},
                "infinite arity keyword": {},
                "argument separator keyword": {},
                "keyword": {},
            }

lines = readFile(filename)
findLexemes(lines)

# for i in symbolTable:
#     print(i + " = " + str(symbolTable[i]))

printSymbolTable()

#REFERENCES
# [1] https://stackoverflow.com/questions/24593824/why-does-re-findall-return-a-list-of-tuples-when-my-pattern-only-contains-one-gr
# [2] https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/