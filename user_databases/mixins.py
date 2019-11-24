from enum import Enum
from json import loads
from uuid import uuid4

class Comparison(Enum):
  IS_EQUAL_TO = 0
  IS_NOT_EQUAL_TO = 1
  IS_LESS_THAN = 2
  IS_LESS_THAN_OR_EQUAL_TO = 3
  IS_GREATER_THAN = 4
  IS_GREATER_THAN_OR_EQUAL_TO = 5

def findRow(database, columns, comparisonColumn=None, comparison=None, operand=None):
  # Check if database was passed
  if database is None:
    raise Exception('database is required')

  # Check if columns was passed
  if columns is None:
    raise Exception('columns is required')

  # Get columns from stored database
  try:
    database_columns = loads(database.columns)
  except:
    raise Exception('error parsing database columns')

  # Confirm selected columns are present in stored database
  for column in columns:
    if column not in database_columns:
      raise Exception('selected columns not in database')

  # Confirm comparison column is present in stored database
  if comparisonColumn is not None and comparisonColumn not in database_columns:
    raise Exception('comparison column is not in database')

  try:
    # Get data from stored database
    data = loads(database.rows)

    # Filter database rows to match selection
    filteredData = []
    if comparison is not None and comparisonColumn is not None:
      if comparison is Comparison.IS_EQUAL_TO:
        for row in data:
          if str(row[comparisonColumn]) == str(operand):
            filteredData.append(row)

      elif comparison is Comparison.IS_NOT_EQUAL_TO:
        for row in data:
          if str(row[comparisonColumn]) != str(operand):
            filteredData.append(row)

      elif comparison is Comparison.IS_LESS_THAN:
        for row in data:
          if str(row[comparisonColumn]) < str(operand):
            filteredData.append(row)

      elif comparison is Comparison.IS_LESS_THAN_OR_EQUAL_TO:
        for row in data:
          if str(row[comparisonColumn]) <= str(operand):
            filteredData.append(row)

      elif comparison is Comparison.IS_GREATER_THAN:
        for row in data:
          if str(row[comparisonColumn]) > str(operand):
            filteredData.append(row)
      
      elif comparison is Comparison.IS_GREATER_THAN_OR_EQUAL_TO:
        for row in data:
          if str(row[comparisonColumn]) >= str(operand):
            filteredData.append(row)
    else:
      return data
    
    # From filtered rows, compile only desired columns
    output = []
    for row in filteredData:
      output_row = dict.fromkeys(columns)
      for key in columns:
        output_row[key] = row[key]
      output.append(output_row)
    
    return output

  except:
    raise Exception('error performing request')

def generateSecret():
  return uuid4().hex