import re

filename = "Project 3/samplecode.txt"

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
    for i in lines:
        # identifier = re.findall("\ [a-zA-Z][a-zA-Z0-9_]*\ ", i)
        # print(identifier)
        # if(identifier):
        #     for j in identifier:
        #         if (symbolTable['identifier'].get(j.strip())):
        #             symbolTable['identifier'][j.strip()][0] += 1
        #         else:
        #             symbolTable['identifier'][j.strip()] = [1]

        #catches NUMBR literal
        numbrLiteral = re.findall("[^\.][-]?\d+$", i)
        if(numbrLiteral):
            for j in numbrLiteral:
                if (symbolTable['NUMBR literal'].get(j.strip())):
                    symbolTable['NUMBR literal'][j.strip()][0] += 1
                else:
                    symbolTable['NUMBR literal'][j.strip()] = [1]

        numbarLiteral = re.findall("[-]?\d+[.]\d+$", i)
        if(numbarLiteral):
            for j in numbarLiteral:
                if (symbolTable['NUMBAR literal'].get(j.strip())):
                    symbolTable['NUMBAR literal'][j.strip()][0] += 1
                else:
                    symbolTable['NUMBAR literal'][j.strip()] = [1]

        yarnLiteral = re.findall("\".*\"$", i)
        if(yarnLiteral):
            for j in yarnLiteral:
                if (symbolTable['YARN literal'].get(j.strip())):
                    symbolTable['YARN literal'][j.strip()][0] += 1
                else:
                    symbolTable['YARN literal'][j.strip()] = [1]
        
        troofLiteral = re.findall("(WIN)$|(FAIL)$", i)
        troofLiteral = [tuple(k for k in j if k)[-1] for j in troofLiteral] #[1]
        if(troofLiteral):
            for j in troofLiteral:
                if (symbolTable['TROOF literal'].get(j.strip())):
                    symbolTable['TROOF literal'][j.strip()][0] += 1
                else:
                    symbolTable['TROOF literal'][j.strip()] = [1]
        
        typeLiteral = re.findall("(TROOF)$|(NOOB)$|(NUMBR)$|(NUMBAR)$|(YARN)$|(TYPE)$", i)
        typeLiteral = [tuple(k for k in j if k)[-1] for j in typeLiteral]
        if(typeLiteral):
            for j in typeLiteral:
                if (symbolTable['TYPE literal'].get(j.strip())):
                    symbolTable['TYPE literal'][j.strip()][0] += 1
                else:
                    symbolTable['TYPE literal'][j.strip()] = [1]

        haiKeyword = re.findall("^(HAI)", i)                        # HAI
        if (len(haiKeyword) != 0):
            if (symbolTable['keyword'].get(haiKeyword[0])):
                symbolTable['keyword'][haiKeyword[0]][0] += len(haiKeyword)
            else:
                symbolTable['keyword'][haiKeyword[0]] = [1]

        kThxByeKeyword = re.findall("^(KTHXBYE)$", i)               # KTHXBYE
        if (len(kThxByeKeyword) != 0):
            if (symbolTable['keyword'].get(kThxByeKeyword[0])):
                symbolTable['keyword'][kThxByeKeyword[0]][0] += len(kThxByeKeyword)
            else:
                symbolTable['keyword'][kThxByeKeyword[0]] = [1]

        btwKeyword = re.findall("[^O](BTW)", i)                        # BTW
        if (len(btwKeyword) != 0):
            if (symbolTable['keyword'].get(btwKeyword[0])):
                symbolTable['keyword'][btwKeyword[0]][0] += len(btwKeyword)
            else:
                symbolTable['keyword'][btwKeyword[0]] = [1]

        obtwKeyword = re.findall("^(OBTW)", i)                        # OBTW
        if (len(obtwKeyword) != 0):
            if (symbolTable['keyword'].get(obtwKeyword[0])):
                symbolTable['keyword'][obtwKeyword[0]][0] += len(btwKeyword)
            else:
                symbolTable['keyword'][obtwKeyword[0]] = [1]

        tldrKeyword = re.findall("^(TLDR)", i)                        # TLDR
        if (len(tldrKeyword) != 0):
            if (symbolTable['keyword'].get(tldrKeyword[0])):
                symbolTable['keyword']["TLDR"][0] += len(tldrKeyword)
            else:
                symbolTable['keyword'][tldrKeyword[0]] = [1]
        
        iHasAKeyword = re.findall("^(I\ HAS\ A)", i)                  # I HAS A
        if (len(iHasAKeyword) != 0):
            if (symbolTable['keyword'].get(iHasAKeyword[0])):
                symbolTable['keyword']["I HAS A"][0] += len(iHasAKeyword)
            else:
                symbolTable['keyword'][iHasAKeyword[0]] = [1]

        itzKeyword = re.findall("^(ITZ)", i)                          # ITZ
        if (len(itzKeyword) != 0):
            if (symbolTable['keyword'].get(itzKeyword[0])):
                symbolTable['keyword']["ITZ"][0] += len(itzKeyword)
            else:
                symbolTable['keyword'][itzKeyword[0]] = [1]
        
        rKeyword = re.findall("( R )", i)                          # R
        if (len(rKeyword) != 0):
            if (symbolTable['keyword'].get(rKeyword[0].strip())):           # Used the strip to remove leading and trailing whitespaces         (To catch only the letter)
                symbolTable['keyword']["R"][0] += len(rKeyword)
            else:
                symbolTable['keyword'][rKeyword[0].strip()] = [1]

        sumOfKeyword = re.findall("^(SUM\ OF)", i)                          # SUM OF
        if (len(sumOfKeyword) != 0):
            if (symbolTable['keyword'].get(sumOfKeyword[0])):           
                symbolTable['keyword']["SUM OF"][0] += len(sumOfKeyword)
            else:
                symbolTable['keyword'][sumOfKeyword[0]] = [1]

        diffOfKeyword = re.findall("^(DIFF\ OF)", i)                          # DIFF OF
        if (len(diffOfKeyword) != 0):
            if (symbolTable['keyword'].get(diffOfKeyword[0])):           
                symbolTable['keyword']["DIFF OF"][0] += len(diffOfKeyword)
            else:
                symbolTable['keyword'][diffOfKeyword[0]] = [1]
        
        produktOfKeyword = re.findall("^(PRODUKT\ OF)", i)                          # PRODUKT OF
        if (len(produktOfKeyword) != 0):
            if (symbolTable['keyword'].get(produktOfKeyword[0])):           
                symbolTable['keyword']["PRODUKT OF"][0] += len(produktOfKeyword)
            else:
                symbolTable['keyword'][produktOfKeyword[0]] = [1]
        
        quoshuntOfKeyword = re.findall("^(QUOSHUNT\ OF)", i)                          # QUOSHUNT OF
        if (len(quoshuntOfKeyword) != 0):
            if (symbolTable['keyword'].get(quoshuntOfKeyword[0])):           
                symbolTable['keyword']["QUOSHUNT OF"][0] += len(quoshuntOfKeyword)
            else:
                symbolTable['keyword'][quoshuntOfKeyword[0]] = [1]

        modOfKeyword = re.findall("^(MOD\ OF)", i)                          # MOD OF
        if (len(modOfKeyword) != 0):
            if (symbolTable['keyword'].get(modOfKeyword[0])):           
                symbolTable['keyword']["MOD OF"][0] += len(modOfKeyword)
            else:
                symbolTable['keyword'][modOfKeyword[0]] = [1]
        
        biggrOfKeyword = re.findall("^(BIGGR\ OF)", i)                          # BIGGR OF
        if (len(biggrOfKeyword) != 0):
            if (symbolTable['keyword'].get(biggrOfKeyword[0])):           
                symbolTable['keyword']["BIGGR OF"][0] += len(biggrOfKeyword)
            else:
                symbolTable['keyword'][biggrOfKeyword[0]] = [1]
        
        smallrOfKeyword = re.findall("^(SMALLR\ OF)", i)                          # SMALLR OF
        if (len(smallrOfKeyword) != 0):
            if (symbolTable['keyword'].get(smallrOfKeyword[0])):           
                symbolTable['keyword']["SMALLR OF"][0] += len(smallrOfKeyword)
            else:
                symbolTable['keyword'][smallrOfKeyword[0]] = [1]
        
        bothOfKeyword = re.findall("^(BOTH\ OF)", i)                          # BOTH OF
        if (len(bothOfKeyword) != 0):
            if (symbolTable['keyword'].get(bothOfKeyword[0])):           
                symbolTable['keyword']["BOTH OF"][0] += len(bothOfKeyword)
            else:
                symbolTable['keyword'][bothOfKeyword[0]] = [1]
        
        eitherOfKeyword = re.findall("^(EITHER\ OF)", i)                          # EITHER OF
        if (len(eitherOfKeyword) != 0):
            if (symbolTable['keyword'].get(eitherOfKeyword[0])):           
                symbolTable['keyword']["EITHER OF"][0] += len(eitherOfKeyword)
            else:
                symbolTable['keyword'][eitherOfKeyword[0]] = [1]
        
        wonOfKeyword = re.findall("^(WON\ OF)", i)                          # WON OF
        if (len(wonOfKeyword) != 0):
            if (symbolTable['keyword'].get(wonOfKeyword[0])):           
                symbolTable['keyword']["WON OF"][0] += len(wonOfKeyword)
            else:
                symbolTable['keyword'][wonOfKeyword[0]] = [1]
        
        notKeyword = re.findall("^(NOT)", i)                          # NOT
        if (len(notKeyword) != 0):
            if (symbolTable['keyword'].get(notKeyword[0])):           
                symbolTable['keyword']["NOT"][0] += len(notKeyword)
            else:
                symbolTable['keyword'][notKeyword[0]] = [1]
        
        anyOfKeyword = re.findall("^(ANY\ OF)", i)                          # ANY OF
        if (len(anyOfKeyword) != 0):
            if (symbolTable['keyword'].get(anyOfKeyword[0])):           
                symbolTable['keyword']["ANY OF"][0] += len(anyOfKeyword)
            else:
                symbolTable['keyword'][anyOfKeyword[0]] = [1]
        
        allOfKeyword = re.findall("^(ALL\ OF)", i)                          # ALL OF
        if (len(allOfKeyword) != 0):
            if (symbolTable['keyword'].get(allOfKeyword[0])):           
                symbolTable['keyword']["ALL OF"][0] += len(allOfKeyword)
            else:
                symbolTable['keyword'][allOfKeyword[0]] = [1]

        bothSaemKeyword = re.findall("^(BOTH\ SAEM)", i)                          # BOTH SAEM
        if (len(bothSaemKeyword) != 0):
            if (symbolTable['keyword'].get(bothSaemKeyword[0])):           
                symbolTable['keyword']["ALL OF"][0] += len(bothSaemKeyword)
            else:
                symbolTable['keyword'][bothSaemKeyword[0]] = [1]

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
                "identifier": {},
                "NUMBR literal": {},
                "NUMBAR literal": {},
                "YARN literal": {},
                "TROOF literal": {},
                "TYPE literal": {},
                "keyword": {},
            }

lines = readFile(filename)
findLexemes(lines)

# for i in symbolTable:
#     print(i + " = " + str(symbolTable[i]))

printSymbolTable()

#REFERENCES
# [1] https://stackoverflow.com/questions/24593824/why-does-re-findall-return-a-list-of-tuples-when-my-pattern-only-contains-one-gr