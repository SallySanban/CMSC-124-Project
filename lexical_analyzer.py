import re

filename = "Project 3/samplecode.txt"

def readFile(filename):
    file = open(filename)
    tokens = []

    #reads the file and places each line in a list
    for line in file.readlines():
        words = line.split("\n")
        for i in words:
            tokens.append(i)

    #gets rid of leading whitespaces in each line
    for i in range(0, len(tokens)):
        tokens[i] = tokens[i].strip()

    for i in tokens:
        if(i == ""):
            tokens.remove(i)
        
    return tokens

#MAIN CODE
print(readFile(filename))