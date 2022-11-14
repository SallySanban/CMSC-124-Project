import re

filename = "Project 3/samplecode.txt"

def readFile(filename):
    file = open(filename)
    tokens = []

    for line in file.readlines():
        words = line.split()
        for i in words:
            tokens.append(i)

    return tokens

#MAIN CODE
print(readFile(filename))