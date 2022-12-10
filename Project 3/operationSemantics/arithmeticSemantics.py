import semantics_analyzer

types = semantics_analyzer.getType()
lexemes = lexical_analyzer.getLexemes()

# TODO: ADD IDENTIFIER

def arithmeticSemantics(lineNumber, variable, symbolTable):
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
      if lexemes[lineNumber][index] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]:
          operationIndices.append(index)

  # * Gets the indices of AN
  anIndices = []
  for index in range(len(lexemes[lineNumber])):
      if lexemes[lineNumber][index] == "AN":
          anIndices.append(index)

  for operator in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]:
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

  while True:
    # * Breaks the loop if lexemeExpression is equal to 1
    if (len(lexemeExpression) == 1):
      break

    # * Refreshes the operationIndices
    operationIndices.clear()
    for index in range(len(lexemeExpression)):
      if lexemeExpression[index] in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]:
          operationIndices.append(index)  

    tempVal = 0

    # * Get index of first operation to solve starting from the last
    lastIndexOperator = operationIndices[len(operationIndices) - 1]

    if typeExpression[lastIndexOperator + 1] == "identifier":   # ! identifier (1st operand)
      if symbolTable.get(lexemeExpression[lastIndexOperator + 1]):
        lexemeExpression[lastIndexOperator + 1] = symbolTable[lexemeExpression[lastIndexOperator + 1]][0]
        typeExpression[lastIndexOperator + 1] = symbolTable[lexemeExpression[lastIndexOperator + 1]][1]
      else:
        return(f"[Line {lineNumber}] SemanticsError: Uninitialized variable")
    
    if typeExpression[lastIndexOperator + 3] == "identifier":   # ! identifier (2nd operand)
      if symbolTable.get(lexemeExpression[lastIndexOperator + 1]):
        lexemeExpression[lastIndexOperator + 3] = symbolTable[lexemeExpression[lastIndexOperator + 3]][0]
        typeExpression[lastIndexOperator + 3] = symbolTable[lexemeExpression[lastIndexOperator + 3]][1]
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
    
  print(tempVal)
