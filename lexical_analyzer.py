# TASKS RIO (HAI -> BOTH SAEM)

import re

filename = "samplecode.txt"

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
    tempList = []
    for i in lines:
        haiKeyword = re.findall("^(HAI)", i)                        # HAI
        if (haiKeyword):
            if (symbolTable['keyword'].get(haiKeyword[0])):
                symbolTable['keyword'][haiKeyword[0]][0] += len(haiKeyword)
            else:
                symbolTable['keyword'][haiKeyword[0]] = [1]


        kThxByeKeyword = re.findall("^(KTHXBYE)$", i)               # KTHXBYE
        if (kThxByeKeyword):
            if (symbolTable['keyword'].get(kThxByeKeyword[0])):
                symbolTable['keyword'][kThxByeKeyword[0]][0] += len(kThxByeKeyword)
            else:
                symbolTable['keyword'][kThxByeKeyword[0]] = [1]


        btwKeyword = re.findall("[^O](BTW)", i)                        # BTW
        if (btwKeyword):
            if (symbolTable['keyword'].get(btwKeyword[0])):
                symbolTable['keyword'][btwKeyword[0]][0] += len(btwKeyword)
            else:
                symbolTable['keyword'][btwKeyword[0]] = [1]


        # obtwKeyword = re.findall("^(OBTW)", i)               # OBTW
        # if (obtwKeyword):
        #     for j in obtwKeyword:
        #         symbolTable['keyword'].append(j)

        # tldrKeyword = re.findall("^(TLDR)", i)               # TLDR
        # if (tldrKeyword):
        #     for j in tldrKeyword:
        #         symbolTable['keyword'].append(j)
        #add other cases here
    
#MAIN CODE
symbolTable = {
                "function identifier": {},
                "variable identifier": {},
                "loop identifier": {},
                "NUMBR literal": {},
                "NUMBAR literal": {},
                "YARN literal": {},
                "TROOF literal": {},
                "TYPE literal": {},
                "keyword": {}, #i think pwede pa iseparate yung mga keywords?
            }

lines = readFile(filename)

print(lines)
findLexemes(lines)

print(symbolTable)