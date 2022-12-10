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
        return(f"[Line {lineNumber}] SemanticsError: Uninitialized variable")
    
    if typeExpression[lastIndexOperator + 3] == "identifier":   # ! identifier (2nd operand)
      if symbolTable.get(lexemeExpression[lastIndexOperator + 3]):
        identifier = symbolTable[lexemeExpression[lastIndexOperator + 3]]
        lexemeExpression[lastIndexOperator + 3] = identifier[0]
        typeExpression[lastIndexOperator + 3] = identifier[1]
      else:
        return(f"[Line {lineNumber}] SemanticsError: Uninitialized variable")

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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 3])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")

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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      else:     # ! NOOB literal (1st operand)
        return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")

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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 3])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")

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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      else:     # ! NOOB literal (1st operand)
        return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 3])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")

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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      else:     # ! NOOB literal (1st operand)
        return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
    elif lexemeExpression[lastIndexOperator] == "QUOSHUNT OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
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
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) / int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) / float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
            return(f"[Line {lineNumber}] SemanticsError: Division by zero")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 3])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")

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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
            return(f"[Line {lineNumber}] SemanticsError: Divison by zero")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      else:     # ! NOOB literal (1st operand)
        return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
    elif lexemeExpression[lastIndexOperator] == "MOD OF":
      if typeExpression[lastIndexOperator + 1] == "NUMBR literal":    # ! NUMBR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
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
          try:
            tempVal = int(lexemeExpression[lastIndexOperator + 1]) % int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
            return(f"[Line {lineNumber}] SemanticsError: Division by zero")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "NUMBAR literal":   # ! NUMBAR Literal (1st operand)
        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
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
          try:
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = float(lexemeExpression[lastIndexOperator + 1]) % float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
            tempVal = float(lexemeExpression[lastIndexOperator + 1]) % 0
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "TROOF literal":         # ! TROOF LITERAL (1st operand)
        temp = 0
        if typeExpression[lastIndexOperator + 1] == "WIN":
          temp = 1

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 3])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")

        if typeExpression[lastIndexOperator + 3] == "NUMBR literal":
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
          try:
            tempVal = temp % int(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            try:
              tempVal = temp % float(lexemeExpression[lastIndexOperator + 3])
            except ValueError:
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
            return(f"[Line {lineNumber}] SemanticsError: Divison by zero")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      else:     # ! NOOB literal (1st operand)
        return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")

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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 3])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")

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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      else:     # ! NOOB literal (1st operand)
        return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      elif typeExpression[lastIndexOperator + 1] == "YARN literal":         # ! YARN LITERAL (1st operand)
        try:
          temp = int(lexemeExpression[lastIndexOperator + 3])
        except ValueError:
          try:
            temp = float(lexemeExpression[lastIndexOperator + 3])
          except ValueError:
            return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")

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
              return(f"[Line {lineNumber}] SemanticsError: YARN literal cannot be converted to NUMBR of NUMBAR literal")
          
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
          return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")
      else:     # ! NOOB literal (1st operand)
        return(f"[Line {lineNumber}] SemanticsError: NOOB literal cannot be converted to NUMBR of NUMBAR literal")

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

  # * Gets the indices of arithmetic operations
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
              return(f"[Line {lineNumber}] SemanticsError: Value can not be typecasted to TROOF literal")
        else:
          return(f"[Line {lineNumber}] SemanticsError: Uninitialized variable")
        
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
              return(f"[Line {lineNumber}] SemanticsError: Value can not be typecasted to TROOF literal")
        else:
          return(f"[Line {lineNumber}] SemanticsError: Uninitialized variable")
      elif lexemeExpression[lastIndexOperator + 1] not in ["WIN", "FAIL", "NOOB"]:
        # print(f"[Line {lineNumber}] SyntaxError: Invalid statement")
        return(f"[Line {lineNumber}] SyntaxError: Invalid statement")
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
              return(f"[Line {lineNumber}] SemanticsError: Value can not be typecasted to TROOF literal")
        else:
          return(f"[Line {lineNumber}] SemanticsError: Uninitialized variable")
      elif lexemeExpression[lastIndexOperator + 1] not in ["WIN", "FAIL", "NOOB"]:
        return(f"[Line {lineNumber}] SyntaxError: Invalid statement")
      

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
      print(lexemeExpression)
    elif lexemeExpression[lastIndexOperator] == "ANY OF":   # * ALL OF (infinite arity)
      print(lexemeExpression)
  
  
  if lexemeExpression[0] == "WIN":
    tempVal = [True, typeExpression[0]]
  else:
    tempVal = [False, typeExpression[0]]
    
  print(lexemeExpression)
  print(typeExpression)
  print(tempVal)
  
  return tempVal