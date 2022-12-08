# def smallrOfSyntax(lineNumber):
#     smallrOfIndex = lexemes[lineNumber].index("SMALLR OF")

    

#     counter = 0
#     for keyword in range(smallrOfIndex, len(lexemes[lineNumber])):                 # Checks the n operation keywords
#         if (lexemes[lineNumber][keyword] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
#             counter += 1
#         else:
#             break

#     isNumber = False
#     numberCnt = 0
#     for k in range(smallrOfIndex + counter, len(lexemes[lineNumber])):
#         if (numberCnt < counter + 1):
#             isNumber = not isNumber
#             if isNumber:
#                 if (types[lineNumber][k] in ["NUMBR literal", "NUMBAR literal"]):
#                     numberCnt += 1
#                 else:
#                     return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal"
#             else:
#                 if (lexemes[lineNumber][k] != "AN"):
#                     return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
#                 elif (lexemes[lineNumber][k] == "AN"):
#                     continue
#                 else:
#                     print(lexemes[lineNumber][k])
#                     return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
#         else:
#             if(lexemes[lineNumber][k] == "BTW"):
#                 return singleCommentSyntax(lineNumber)
#             else:
#                 # print(lexemes[lineNumber][k])                 # CHECKER
#                 return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"

# def biggrOfSyntax(lineNumber):
#     biggrOfIndex = lexemes[lineNumber].index("BIGGR OF")

#     counter = 0
#     for keyword in range(biggrOfIndex, len(lexemes[lineNumber])):                 # Checks the n operation keywords
#         if (lexemes[lineNumber][keyword] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]):
#             counter += 1
#         else:
#             break
    
#     isNumber = False
#     numberCnt = 0
#     for k in range(biggrOfIndex + counter, len(lexemes[lineNumber])):
#         if (numberCnt < counter + 1):
#             isNumber = not isNumber
#             if isNumber:
#                 if (types[lineNumber][k] in ["NUMBR literal", "NUMBAR literal"]):
#                     numberCnt += 1
#                 else:
#                     return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal"
#             else:
#                 if (lexemes[lineNumber][k] != "AN"):
#                     return "[Line " + str(lineNumber) + "] SyntaxError: Expected an argument separator keyword"
#                 elif (lexemes[lineNumber][k] == "AN"):
#                     continue
#                 else:
#                     print(lexemes[lineNumber][k])
#                     return "[Line " + str(lineNumber) + "] SyntaxError: Expected a numbr or numbar literal after arithmetic operator"
#         else:
#             if(lexemes[lineNumber][k] == "BTW"):
#                 return singleCommentSyntax(lineNumber)
#             else:
#                 # print(lexemes[lineNumber][k])                 # CHECKER
#                 return "[Line " + str(lineNumber) + "] SyntaxError: cannot have statements after arithmetic operation"
