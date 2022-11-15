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
    for i in lines:
        print(i)
        #catches NUMBR literal
        numbrLiteral = re.findall("[^.][-]?\d+$", i)
        if(numbrLiteral):
            for j in numbrLiteral:
                symbolTable['NUMBR literal'].append(j.strip())

        #catches NUMBAR literal
        numbarLiteral = re.findall("[-]?\d+[.]\d+$", i)
        if(numbarLiteral):
            for j in numbarLiteral:
                symbolTable['NUMBAR literal'].append(j)
        #add other cases here
    
#MAIN CODE
symbolTable = {"function identifier": [],
                "variable identifier": [],
                "loop identifier": [],
                "NUMBR literal": [],
                "NUMBAR literal": [],
                "YARN literal": [],
                "TROOF literal": [],
                "TYPE literal": [],
                "keyword": [] #i think pwede pa iseparate yung mga keywords?
                }

lines = readFile(filename)

print(lines)
findLexemes(lines)

print(symbolTable)