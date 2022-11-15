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
        identifier = re.findall("\s[a-zA-Z][a-zA-Z0-9_]*\s", i)
        print(identifier)
        # if(identifier):
        #     for j in identifier:
        #         symbolTable['identifier'].append(j.strip())

        #catches NUMBR literal
        # numbrLiteral = re.findall("[^\.][-]?\d+$", i)
        # if(numbrLiteral):
        #     for j in numbrLiteral:
        #         symbolTable['NUMBR literal'].append(j.strip())

        # numbarLiteral = re.findall("[-]?\d+[.]\d+$", i)
        # if(numbarLiteral):
        #     for j in numbarLiteral:
        #         symbolTable['NUMBAR literal'].append(j.strip())

        # yarnLiteral = re.findall("\".*\"$", i)
        # if(yarnLiteral):
        #     for j in yarnLiteral:
        #         symbolTable['YARN literal'].append(j.strip())
        
        # troofLiteral = re.findall("(WIN)$|(FAIL)$", i)
        # troofLiteral = [tuple(k for k in j if k)[-1] for j in troofLiteral] #[1]
        # if(troofLiteral):
        #     for j in troofLiteral:
        #         symbolTable['TROOF literal'].append(j.strip())
        
        # typeLiteral = re.findall("(TROOF)$|(NOOB)$|(NUMBR)$|(NUMBAR)$|(YARN)$|(TYPE)$", i)
        # typeLiteral = [tuple(k for k in j if k)[-1] for j in typeLiteral]
        # if(typeLiteral):
        #     for j in typeLiteral:
        #         symbolTable['TYPE literal'].append(j.strip())

        #add other cases here

def printSymbolTable(symbolTable):
    space = 5
    
#MAIN CODE
symbolTable = {"identifier": [],
                "NUMBR literal": [],
                "NUMBAR literal": [],
                "YARN literal": [],
                "TROOF literal": [],
                "TYPE literal": [],
                "keyword": [] #i think pwede pa iseparate yung mga keywords?
                }

lines = readFile(filename)

#print(lines)
findLexemes(lines)

for i in symbolTable:
    print(i + " = " + str(symbolTable[i]))

#REFERENCES
# [1] https://stackoverflow.com/questions/24593824/why-does-re-findall-return-a-list-of-tuples-when-my-pattern-only-contains-one-gr