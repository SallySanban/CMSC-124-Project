literals = ["NUMBR literal",
            "NUMBAR literal",
            "YARN literal",
            "TROOF literal",
            "TYPE literal"
            ]
expressionKeywords = {
                        "arithmetic":
                            ["SUM OF",
                            "DIFF OF",
                            "PRODUKT OF",
                            "QUOSHUNT OF",
                            "MOD OF",
                            "BIGGR OF",
                            "SMALLR OF"],
                        "boolean":
                            ["BOTH OF",
                            "EITHER OF",
                            "WON OF",
                            "NOT",
                            "ANY OF",
                            "ALL OF"],
                        "comparison":
                            ["BOTH SAEM",
                            "DIFFRINT"],
                        "concatenation":
                            ["SMOOSH"]
                    }

def arithmeticExpSemantics(lineNumber, symbolTable, lexemes, types):
  # * Gets the index of ITZ
  if("variable initialization keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("ITZ")
  #put other cases where the arithmetic expression might be
  elif("print keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("VISIBLE")
  else:
    expressionIndex = -1 

  # * Gets the indices of arithmetic operations
  operationIndices = []
  lexemeExpression = 0
  typeExpression = 0
  for index in range(len(lexemes[lineNumber])):
    if lexemes[lineNumber][index] in expressionKeywords["arithmetic"]:
      operationIndices.append(index)

  # * Gets the indices of AN
  anIndices = []
  for index in range(len(lexemes[lineNumber])):
    if lexemes[lineNumber][index] == "AN":
        anIndices.append(index)

  for operator in expressionKeywords["arithmetic"]:
    if lexemes[lineNumber][expressionIndex + 1] == operator:
      # parentOperation = operator
      lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 2)]
      typeExpression = types[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 2)]

      # * Removes the string delimiters from the list
      while True:
        try:
          lexemeExpression.remove("\"")
          typeExpression.remove("string delimiter")
        except ValueError:
          break
      break

  if len(anIndices) != len(operationIndices):
    return(f"[Line {lineNumber}] SyntaxError: Invalid expression")
  
  
  while True:
    print(lexemeExpression)
    # * Breaks the loop if lexemeExpression is equal to 1
    if (len(lexemeExpression) == 1):
      break

    # * Refreshes the operationIndices
    operationIndices.clear()
    for index in range(len(lexemeExpression)):
      if lexemeExpression[index] in expressionKeywords["arithmetic"]:
          operationIndices.append(index)  

    tempVal = 0

    # * Get index of first operation to solve starting from the last
    lastIndexOperator = operationIndices[len(operationIndices) - 1]

    if typeExpression[lastIndexOperator + 1] == "identifier":   # ! identifier (1st operand)
      if symbolTable.get(lexemeExpression[lastIndexOperator + 1]):
        identifier = symbolTable[lexemeExpression[lastIndexOperator + 1]]
        lexemeExpression[lastIndexOperator + 1] = identifier[0]
        typeExpression[lastIndexOperator + 1] = identifier[1]
      else:
        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
    elif typeExpression[lastIndexOperator + 1] not in ["NUMBR literal", "NUMBAR literal", "TROOF literal", "string delimiter", "YARN literal", "NOOB"]:
      return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"

    
    if typeExpression[lastIndexOperator + 3] == "identifier":   # ! identifier (2nd operand)
      if symbolTable.get(lexemeExpression[lastIndexOperator + 3]):
        identifier = symbolTable[lexemeExpression[lastIndexOperator + 3]]
        lexemeExpression[lastIndexOperator + 3] = identifier[0]
        typeExpression[lastIndexOperator + 3] = identifier[1]
      else:
        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
    elif typeExpression[lastIndexOperator + 3] not in ["NUMBR literal", "NUMBAR literal", "TROOF literal", "string delimiter", "YARN literal", "NOOB"]:
      return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"
    
    print(lexemeExpression)
    print(typeExpression)

    if lexemeExpression[lastIndexOperator] == "SUM OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = int(lexemeExpression[lastIndexOperator + 1]) + int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) + int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) + 1
          else:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) + 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) + float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) + 1
          else:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) + 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp + int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = temp + float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp + int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp + float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp + 1
          else:
            tempVal = temp + 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp + int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list

          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = temp + float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp + int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp + float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp + 1
          else:
            tempVal = temp + 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "DIFF OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = int(lexemeExpression[lastIndexOperator + 1]) - int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) - int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) - 1
          else:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) - 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) - float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) - 1
          else:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) - 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp - int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = temp - float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp - int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp - float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list

          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp - 1
          else:
            tempVal = temp - 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp - int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = temp - float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp - int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp - float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp - 1
          else:
            tempVal = temp - 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "PRODUKT OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = int(lexemeExpression[lastIndexOperator + 1]) * int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) * int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) * 1
          else:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) * 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) * 1
          else:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) * 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp * int(lexemeExpression[lastIndexOperator + 3])
        
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp * int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp * 1
          else:
            tempVal = temp * 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp * int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp * int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp * 1
          else:
            tempVal = temp * 0
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      else:     # ! NOOB literal (2st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "QUOSHUNT OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = int(lexemeExpression[lastIndexOperator + 1]) / int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) / int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) / 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) / 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
        
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = temp / int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = temp * int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp / 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = temp / int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = temp / float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = temp / int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp / float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp / 1
          else:
            return(f"[Line {lineNumber}] SemanticError: Divison by zero")
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      else:     # ! NOOB literal (2st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "MOD OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = int(lexemeExpression[lastIndexOperator + 1]) % int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) % int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) % 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) % 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = temp % int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = temp * int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp * float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list

          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp * 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = temp % int(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          tempVal = temp % float(lexemeExpression[lastIndexOperator + 3])
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          if lexemeExpression[lastIndexOperator + 3] == "0" or lexemeExpression[lastIndexOperator + 3] == "0.0":
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          try:
            tempVal = temp % int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp % float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = temp % 1
          else:
            return "[Line " + str(lineNumber) + "] SemanticError: Division by zero" 
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "BIGGR OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = max(int(lexemeExpression[lastIndexOperator + 1]),int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(int(lexemeExpression[lastIndexOperator + 1]), int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(lexemeExpression[lastIndexOperator + 1], 1)
          else:
            tempVal = max(lexemeExpression[lastIndexOperator + 1], 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), 1)
          else:
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = max(temp, int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(temp, int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(temp, 1)
          else:
            tempVal = max(temp, 0)

          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = max(temp, int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(temp, int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(temp, 1)
          else:
            tempVal = max(temp, 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
    elif lexemeExpression[lastIndexOperator] == "SMALLR OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = min(int(lexemeExpression[lastIndexOperator + 1]),int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = min(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = min(int(lexemeExpression[lastIndexOperator + 1]), int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = min(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = min(lexemeExpression[lastIndexOperator + 1], 1)
          else:
            tempVal = min(lexemeExpression[lastIndexOperator + 1], 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = min(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), 1)
          else:
            tempVal = max(float(lexemeExpression[lastIndexOperator + 1]), 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = min(temp, int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = min(temp, float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = min(temp, int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = min(temp, float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = min(temp, 1)
          else:
            tempVal = min(temp, 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 1])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 1])
          except ValueError:
            return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
          tempVal = min(temp, int(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list

          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBR literal")
        elif typeExpression[lastIndexOperator + 3] == "NUMBAR literal":
          tempVal = min(temp, float(lexemeExpression[lastIndexOperator + 3]))
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "YARN literal":
          try:
            tempVal = min(temp, int(lexemeExpression[lastIndexOperator + 3]))
          except ValueError:
            try:
              tempVal = max(temp, float(lexemeExpression[lastIndexOperator + 3]))
            except ValueError:
              return "[Line " + str(lineNumber) + "] SemanticError: YARN literal cannot be converted to NUMBR of NUMBAR literal"
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        elif typeExpression[lastIndexOperator + 3] == "TROOF literal":
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = min(temp, 1)
          else:
            tempVal = min(temp, 0)
          
          # * Popping the elements from the lexeme and type list
          counter = 0
          while counter != 4:
            lexemeExpression.pop(lastIndexOperator)
            typeExpression.pop(lastIndexOperator)
            counter += 1

          # * Appending the new elements from the lexeme and type list
          lexemeExpression.insert(lastIndexOperator, str(tempVal))
          typeExpression.insert(lastIndexOperator, "NUMBAR literal")
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"
      else:     # ! NOOB literal (1st operand)
        return "[Line " + str(lineNumber) + "] SemanticError: NOOB literal cannot be converted to NUMBR of NUMBAR literal"

  if typeExpression[0] == "NUMBR literal":
    tempVal = [int(lexemeExpression[0]), typeExpression[0]]
  else:
    tempVal = [float(lexemeExpression[0]), typeExpression[0]]
    
  return tempVal

def booleanExpSemantics(lineNumber, symbolTable, lexemes, types):
  # * Gets the index of ITZ
  if("variable initialization keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("ITZ")
  #put other cases where the arithmetic expression might be
  elif("print keyword" in types[lineNumber]):
    expressionIndex = lexemes[lineNumber].index("VISIBLE")
  else:
    expressionIndex = -1 
  
  if lexemes[lineNumber].count("ANY OF") > 1:
    return "[Line " + str(lineNumber) + "] SyntaxError: ANY OF cannot be nested"
  
  if lexemes[lineNumber].count("ANY OF") == 1:
    if lexemes[lineNumber].count("MKAY") > 1:
      return "[Line " + str(lineNumber) + "] SyntaxError: Have too many ANY OF delimiter MKAY "
    if lexemes[lineNumber].count("MKAY") == 0:
      return "[Line " + str(lineNumber) + "] SyntaxError: ANY OF delimiter MKAY not found"
    
  if lexemes[lineNumber].count("ALL OF") > 1:
    return "[Line " + str(lineNumber) + "] SyntaxError: ANY OF cannot be nested"
  if lexemes[lineNumber].count("ALL OF") == 1:
    if lexemes[lineNumber].count("MKAY") > 1:
      return "[Line " + str(lineNumber) + "] SyntaxError: Have too many ANY OF delimiter MKAY "
    if lexemes[lineNumber].count("MKAY") == 0:
      return "[Line " + str(lineNumber) + "] SyntaxError: ANY OF delimiter MKAY not found"
  
  try:
    if lexemes[lineNumber][lexemes[lineNumber].index("MKAY") + 1]:
      print("",end="")
  except IndexError:
    return "[Line " + str(lineNumber) + "] SyntaxError: No statements allowed after ALL OF or ANY OF delimiter"

      

  # * Gets the indices of boolean operations
  operationIndices = []
  lexemeExpression = 0
  typeExpression = 0
  for index in range(len(lexemes[lineNumber])):
    if lexemes[lineNumber][index] in expressionKeywords["boolean"]:
      operationIndices.append(index)

  # * Gets the indices of AN
  anIndices = []
  for index in range(len(lexemes[lineNumber])):
    if lexemes[lineNumber][index] == "AN":
        anIndices.append(index)

  for operator in expressionKeywords["boolean"]:
    if lexemes[lineNumber][expressionIndex + 1] in ["BOTH OF", "EITHER OF", "WON OF"]:
      lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 3)]
      typeExpression = types[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 3)]

      # * Removes the string delimiters from the list
      while True:
        try:
          lexemeExpression.remove("\"")
          typeExpression.remove("string delimiter")
        except ValueError:
          break
      
    elif lexemes[lineNumber][expressionIndex + 1] == "NOT":
      # print(anIndices)
      if len(anIndices) == 0:   # single operand
        lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(expressionIndex + 2)]
        typeExpression = types[lineNumber][(expressionIndex + 1):(expressionIndex + 2)]
      elif lexemes[lineNumber][anIndices[len(anIndices) - 1] + 1] == "NOT":
        lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 2)]
        typeExpression = types[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 2)]
      else:
        lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 3)]
        typeExpression = types[lineNumber][(expressionIndex + 1):(anIndices[len(anIndices) - 1] + 3)]
    elif lexemes[lineNumber][expressionIndex + 1] in ["ANY OF", "ALL OF"]:
      mkayIndex = lexemes[lineNumber].index("MKAY")
      
      lexemeExpression = lexemes[lineNumber][(expressionIndex + 1):(mkayIndex)]
      typeExpression = types[lineNumber][(expressionIndex + 1):(mkayIndex)]
        
      
      # * Removes the string delimiters from the list
      while True:
        try:
          lexemeExpression.remove("\"")
          typeExpression.remove("string delimiter")
        except ValueError:
          break
      break
  
  # CHECKER
  # print(lexemeExpression)
  # print(typeExpression)
  # print(operationIndices)
  # print(anIndices)
  print(lexemeExpression)
  
  while True:
    # * Breaks the loop if lexemeExpression is equal to 1
    if (len(lexemeExpression) == 1):
      break

    # * Refreshes the operationIndices
    operationIndices.clear()
    for index in range(len(lexemeExpression)):
      if lexemeExpression[index] in expressionKeywords["boolean"]:
          operationIndices.append(index)  

    tempVal = 0

    # * Get index of first operation to solve starting from the last
    lastIndexOperator = operationIndices[len(operationIndices) - 1]

    # * Breaks the lexeme expression and replaces the values
    if lexemeExpression[lastIndexOperator] in ["BOTH OF", "EITHER OF", "WON OF"]:
      if typeExpression[lastIndexOperator + 1] == "identifier":   # ! identifier (1st operand)
        if symbolTable.get(lexemeExpression[lastIndexOperator + 1]):
          identifier = symbolTable[lexemeExpression[lastIndexOperator + 1]]
          lexemeExpression[lastIndexOperator + 1] = identifier[0]
          typeExpression[lastIndexOperator + 1] = identifier[1]
          
          # * Checks if TROOF or NOOB type
          if typeExpression[lastIndexOperator] in ["TROOF literal", "NOOB"]:
            if lexemeExpression[lastIndexOperator + 1] == "NOOB":
              lexemeExpression[lastIndexOperator + 1] == False
              typeExpression[lastIndexOperator + 1] == "TROOF literal"
            else:
              return "[Line " + str(lineNumber) + "] SyntaxError: Value can not be typecasted to TROOF literal"
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
        
        if symbolTable.get(lexemeExpression[lastIndexOperator + 3]):
          identifier = symbolTable[lexemeExpression[lastIndexOperator + 3]]
          lexemeExpression[lastIndexOperator + 3] = identifier[0]
          typeExpression[lastIndexOperator + 3] = identifier[1]
          
          # * Checks if TROOF or NOOB type
          if typeExpression[lastIndexOperator] in ["TROOF literal", "NOOB"]:
            if lexemeExpression[lastIndexOperator + 3] == "NOOB":
              lexemeExpression[lastIndexOperator + 3] == False
              typeExpression[lastIndexOperator + 3] == "TROOF literal"
            else:
              return "[Line " + str(lineNumber) + "] SyntaxError: Value can not be typecasted to TROOF literal"
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
      elif lexemeExpression[lastIndexOperator + 1] not in ["WIN", "FAIL", "NOOB"]:
        # print(f"[Line {lineNumber}] SyntaxError: Invalid statement")
        return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"
    elif lexemeExpression[lastIndexOperator] == "NOT":
      if typeExpression[lastIndexOperator + 1] == "identifier":   # ! identifier (1st operand)
        if symbolTable.get(lexemeExpression[lastIndexOperator + 1]):
          identifier = symbolTable[lexemeExpression[lastIndexOperator + 1]]
          lexemeExpression[lastIndexOperator + 1] = identifier[0]
          typeExpression[lastIndexOperator + 1] = identifier[1]
          
          # * Checks if TROOF or NOOB type
          if typeExpression[lastIndexOperator] in ["TROOF literal", "NOOB"]:
            if lexemeExpression[lastIndexOperator + 1] == "NOOB":
              lexemeExpression[lastIndexOperator + 1] == False
              typeExpression[lastIndexOperator + 1] == "TROOF literal"
            else:
              return "[Line " + str(lineNumber) + "] SyntaxError: Value can not be typecasted to TROOF literal"
        else:
          return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized variable"
      elif lexemeExpression[lastIndexOperator + 1] not in ["WIN", "FAIL", "NOOB"]:
        # print(f"[Line {lineNumber}] SyntaxError: Invalid statement")
        return "[Line " + str(lineNumber) + "] SyntaxError: Invalid expression"
      

    print(lexemeExpression)
    # * Checks the current operator
    if lexemeExpression[lastIndexOperator] == "BOTH OF":    # * AND
      if lexemeExpression[lastIndexOperator + 1] == "WIN":    # ! WIN (1st operand)
        if lexemeExpression[lastIndexOperator + 3] == "WIN":
          tempVal = "WIN"
        else:
          tempVal = "FAIL"
      else:                                                  
        if lexemeExpression[lastIndexOperator + 1] == "FAIL": # ! FAIL (1st operand)
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = "FAIL"
          else:
            tempVal = "FAIL"
      
      # * Popping the elements from the lexeme and type list
      counter = 0
      while counter != 4:
        lexemeExpression.pop(lastIndexOperator)
        typeExpression.pop(lastIndexOperator)
        counter += 1

      # * Appending the new elements from the lexeme and type list
      lexemeExpression.insert(lastIndexOperator, str(tempVal))
      typeExpression.insert(lastIndexOperator, "TROOF literal")
    elif lexemeExpression[lastIndexOperator] == "EITHER OF":  # * OR
      if lexemeExpression[lastIndexOperator + 1] == "WIN":    # ! WIN (1st operand)
        if lexemeExpression[lastIndexOperator + 3] == "WIN":
          tempVal = "WIN"
        else:
          tempVal = "WIN"
      else:                                                  
        if lexemeExpression[lastIndexOperator + 1] == "FAIL": # ! FAIL (1st operand)
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = "WIN"
          else:
            tempVal = "FAIL"
      
      # * Popping the elements from the lexeme and type list
      counter = 0
      while counter != 4:
        lexemeExpression.pop(lastIndexOperator)
        typeExpression.pop(lastIndexOperator)
        counter += 1

      # * Appending the new elements from the lexeme and type list
      lexemeExpression.insert(lastIndexOperator, str(tempVal))
      typeExpression.insert(lastIndexOperator, "TROOF literal")
    elif lexemeExpression[lastIndexOperator] == "WON OF":   # * XOR
      if lexemeExpression[lastIndexOperator + 1] == "WIN":    # ! WIN (1st operand)
        if lexemeExpression[lastIndexOperator + 3] == "WIN":
          tempVal = "FAIL"
        else:
          tempVal = "WIN"
      else:                                                  
        if lexemeExpression[lastIndexOperator + 1] == "FAIL": # ! FAIL (1st operand)
          if lexemeExpression[lastIndexOperator + 3] == "WIN":
            tempVal = "WIN"
          else:
            tempVal = "FAIL"
    elif lexemeExpression[lastIndexOperator] == "NOT":   # * NOT
      if lexemeExpression[lastIndexOperator + 1] == "WIN":    # ! WIN operand
        tempVal = "FAIL"
      else:                                                  
        tempVal = "WIN"
    
    # * Popping the elements from the lexeme and type list
      counter = 0
      while counter != 2:
        lexemeExpression.pop(lastIndexOperator)
        typeExpression.pop(lastIndexOperator)
        counter += 1

      # * Appending the new elements from the lexeme and type list
      lexemeExpression.insert(lastIndexOperator, str(tempVal))
      typeExpression.insert(lastIndexOperator, "TROOF literal")
    elif lexemeExpression[lastIndexOperator] == "ALL OF":   # * ALL OF (infinite arity)
      literalCount = typeExpression.count("TROOF literal")
      if lexemeExpression.count("WIN") > 0 and lexemeExpression.count("FAIL") > 0:
        lexemeExpression = ["FAIL"]
        typeExpression = ["TROOF literal"]
      elif lexemeExpression.count("WIN") == literalCount:
        lexemeExpression = ["WIN"]
        typeExpression = ["TROOF literal"]
      elif lexemeExpression.count("FAIL") == literalCount:
        lexemeExpression = ["FAIL"]
        typeExpression = ["TROOF literal"]
      
      break
    elif lexemeExpression[lastIndexOperator] == "ANY OF":   # * ANY OF (infinite arity)
      literalCount = typeExpression.count("TROOF literal")
      if lexemeExpression.count("WIN") > 0 and lexemeExpression.count("FAIL") > 0:
        lexemeExpression = ["WIN"]
        typeExpression = ["TROOF literal"]
      elif lexemeExpression.count("WIN") == literalCount:
        lexemeExpression = ["WIN"]
        typeExpression = ["TROOF literal"]
      elif lexemeExpression.count("FAIL") == literalCount:
        lexemeExpression = ["FAIL"]
        typeExpression = ["TROOF literal"]
        
      break
  
  
  if lexemeExpression[0] == "WIN":
    tempVal = [True, typeExpression[0]]
  else:
    tempVal = [False, typeExpression[0]]
    
  print(lexemeExpression)
  print(typeExpression)
  print(tempVal)
  
  return tempVal

def comparisonExpSemantics(lineNumber, symbolTable, lexemes, types):
   # * Gets the index of ITZ
    if("variable initialization keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("ITZ")
    #put other cases where the arithmetic expression might be
    elif("print keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("VISIBLE")
    else:
        expressionIndex = -1    
    
    # print(lexemes[lineNumber][expressionIndex])
    anIndices = []
    for index in range(len(lexemes[lineNumber])):
        if lexemes[lineNumber][index] == "AN":
            anIndices.append(index)
    
    
    if (len(anIndices) == 1):      # (x == y OR x != y)
        if lexemes[lineNumber][expressionIndex + 1] == "BOTH SAEM": # x == y
            if types[lineNumber][expressionIndex + 2] == "identifier":  # x = identifier
                if symbolTable.get(lexemes[lineNumber][expressionIndex + 2]):
                    if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][0] == symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                        if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBR literal"):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][0] == int(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                        if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBAR literal"):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 4]][0] == float(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif types[lineNumber][expressionIndex + 2] == "NUMBR literal": # x = NUMBR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (int(lexemes[lineNumber][expressionIndex + 2]) == symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) == int(lexemes[lineNumber][expressionIndex + 4])):
                        temp = ["WIN", "TROOF literal"]
                    else:
                        temp = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) == float(lexemes[lineNumber][expressionIndex + 4])):
                        temp = ["WIN", "TROOF literal"]
                    else:
                        temp = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            elif types[lineNumber][expressionIndex + 2] == "NUMBAR literal":    # x = NUMBAR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (float(lexemes[lineNumber][expressionIndex + 2]) == symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) == int(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) == float(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:
                return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
        else:   # DIFFRINT      x != y
            if types[lineNumber][expressionIndex + 2] == "identifier":  # x = identifier
                if symbolTable.get(lexemes[lineNumber][expressionIndex + 2]):
                    if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][0] != symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                        if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBR literal"):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][0] != int(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                        if (symbolTable[lexemes[lineNumber][expressionIndex + 2]][1] == "NUMBAR literal"):
                            if (symbolTable[lexemes[lineNumber][expressionIndex + 4]][0] != float(lexemes[lineNumber][expressionIndex + 4])):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif types[lineNumber][expressionIndex + 2] == "NUMBR literal": # x = NUMBR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (int(lexemes[lineNumber][expressionIndex + 2]) != symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) != int(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (int(lexemes[lineNumber][expressionIndex + 2]) != float(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            elif types[lineNumber][expressionIndex + 2] == "NUMBAR literal":    # x = NUMBAR
                if types[lineNumber][expressionIndex + 4] == "identifier":      # y
                    if symbolTable.get(lexemes[lineNumber][expressionIndex + 4]):
                        if (float(lexemes[lineNumber][expressionIndex + 2]) != symbolTable[lexemes[lineNumber][expressionIndex + 4]][0]):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][expressionIndex + 4] == "NUMBR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) != int(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                elif types[lineNumber][expressionIndex + 4] == "NUMBAR literal":
                    if (float(lexemes[lineNumber][expressionIndex + 2]) != float(lexemes[lineNumber][expressionIndex + 4])):
                        tempVal = ["WIN", "TROOF literal"]
                    else:
                        tempVal = ["FAIL", "TROOF literal"]
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:
                return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"

    else:       # (x <= y, x >= y, x < y, x > y)
        bigCnt = lexemes[lineNumber].count("BIGGR OF")
        try:
            sizeIndex = lexemes[lineNumber].index("BIGGR OF")
        except ValueError:
            sizeIndex = lexemes[lineNumber].index("SMALLR OF")


        if lexemes[lineNumber][expressionIndex + 1] == "BOTH SAEM": # x <= y, x >= y
            if (bigCnt == 0):       # x <= y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if symbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] <= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] <= int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 3]][0] <= float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) <= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) <= int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) <= float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) <= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) <= int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) <= float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:       # x >= y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if symbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] >= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] >= int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 3]][0] >= float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) >= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) >= int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) >= float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) >= symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) >= int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) >= float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
        else: # DIFFRINT (x < y, x > y)
            if (bigCnt == 0):       # x > y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if symbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] > symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] > int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 3]][0] > float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) > symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) > int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) > float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) > symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) > int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) > float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
            else:       # x < y
                if types[lineNumber][sizeIndex + 1] == "identifier":  # x = identifier
                    if symbolTable.get(lexemes[lineNumber][sizeIndex + 1]):
                        if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                            if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] < symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][0] < int(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                            if (symbolTable[lexemes[lineNumber][sizeIndex + 1]][1] == "NUMBAR literal"):
                                if (symbolTable[lexemes[lineNumber][sizeIndex + 3]][0] < float(lexemes[lineNumber][sizeIndex + 3])):
                                    tempVal = ["WIN", "TROOF literal"]
                                else:
                                    tempVal = ["FAIL", "TROOF literal"]
                            else:
                                return "[Line " + str(lineNumber) + "] SemanticError: Cannot implicitly typecast in comparison operation"
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                elif types[lineNumber][sizeIndex + 1] == "NUMBR literal": # x = NUMBR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (int(lexemes[lineNumber][sizeIndex + 1]) < symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                temp = ["WIN", "TROOF literal"]
                            else:
                                temp = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) < int(lexemes[lineNumber][sizeIndex + 1])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (int(lexemes[lineNumber][sizeIndex + 1]) < float(lexemes[lineNumber][sizeIndex + 3])):
                            temp = ["WIN", "TROOF literal"]
                        else:
                            temp = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                elif types[lineNumber][sizeIndex + 1] == "NUMBAR literal":    # x = NUMBAR
                    if types[lineNumber][sizeIndex + 3] == "identifier":      # y
                        if symbolTable.get(lexemes[lineNumber][sizeIndex + 3]):
                            if (float(lexemes[lineNumber][sizeIndex + 1]) < symbolTable[lexemes[lineNumber][sizeIndex + 3]][0]):
                                tempVal = ["WIN", "TROOF literal"]
                            else:
                                tempVal = ["FAIL", "TROOF literal"]
                        else:
                            return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
                    elif types[lineNumber][sizeIndex + 3] == "NUMBR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) < int(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    elif types[lineNumber][sizeIndex + 3] == "NUMBAR literal":
                        if (float(lexemes[lineNumber][sizeIndex + 1]) < float(lexemes[lineNumber][sizeIndex + 3])):
                            tempVal = ["WIN", "TROOF literal"]
                        else:
                            tempVal = ["FAIL", "TROOF literal"]
                    else:
                        return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Invalid operands for comparison operation"

def concatenationExpSemantics(lineNumber, symbolTable, lexemes, types):
    # ! NO OPERATIONS AS OPERANDS YET
   # * Gets the index of ITZ
    if("variable initialization keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("ITZ")
    #put other cases where the arithmetic expression might be
    elif("print keyword" in types[lineNumber]):
        expressionIndex = lexemes[lineNumber].index("VISIBLE")
    else:
        expressionIndex = -1    
    
    #print(lexemes[lineNumber][expressionIndex])
    anIndices = []
    for index in range(len(lexemes[lineNumber])):
        if lexemes[lineNumber][index] == "AN":
            anIndices.append(index)
    
    counter = 0
    tempVal = ''
    while True:
        if (counter == len(anIndices) - 1):
            if (types[lineNumber][anIndices[counter] - 1] == "identifier"):
                if (symbolTable.get(lexemes[lineNumber][anIndices[counter] - 1])):
                    tempVal += str(symbolTable[lexemes[lineNumber][anIndices[counter] - 1]][0])
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif (types[lineNumber][anIndices[counter] - 1] == "string delimiter"):     # YARN literal
                if (types[lineNumber][anIndices[counter] - 3] == "string delimiter"):   # another delimiter
                    tempVal += lexemes[lineNumber][anIndices[counter] - 2]
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Invalid syntax of YARN literal"     # ! TAKE NOTE
            else:
                tempVal += str(lexemes[lineNumber][anIndices[counter] - 1])
            
            if (types[lineNumber][anIndices[counter] + 1] == "identifier"):
                if (symbolTable.get(lexemes[lineNumber][anIndices[counter] + 1])):
                    tempVal += str(symbolTable[lexemes[lineNumber][anIndices[counter] + 1]][0])
                else:
                    return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
            elif (types[lineNumber][anIndices[counter] + 1] == "string delimiter"):     # YARN literal
                if (types[lineNumber][anIndices[counter] + 3] == "string delimiter"):   # another delimiter
                    tempVal += lexemes[lineNumber][anIndices[counter] + 2]
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Invalid syntax of YARN literal"     # ! TAKE NOTE
            else:
                tempVal += str(lexemes[lineNumber][anIndices[counter] + 1])

            break
        
        if (types[lineNumber][anIndices[counter] - 1] == "identifier"):
            if (symbolTable.get(lexemes[lineNumber][anIndices[counter] - 1])):
                tempVal += str(symbolTable[lexemes[lineNumber][anIndices[counter] - 1]][0])
            else:
                return "[Line " + str(lineNumber) + "] SemanticError: Uninitialized identifier"
        elif (types[lineNumber][anIndices[counter] - 1] == "string delimiter"):     # YARN literal
                if (types[lineNumber][anIndices[counter] - 3] == "string delimiter"):   # another delimiter
                    tempVal += lexemes[lineNumber][anIndices[counter] - 2]
                else:
                    return "[Line " + str(lineNumber) + "] SyntaxError: Invalid syntax of YARN literal"     # ! TAKE NOTE
        else:
            tempVal += str(lexemes[lineNumber][anIndices[counter] - 1])


        counter += 1

