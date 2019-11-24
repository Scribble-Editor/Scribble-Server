from django.utils import timezone
import json

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response

from .models import Database
from .mixins import Comparison, findRow, generateSecret

@csrf_exempt
@api_view(['POST'])
def create(request):
  # Get data from POST body
  user = request.user.username
  now = timezone.now()
  columns = request.data.get('columns')

  # Verify json is valid
  try:
    columns = json.loads(columns)

    # Convert items in list to string
    for i in range(len(columns)):
      columns[i] = str(columns[i])
    
    columns = str(columns)
  except:
    return Response('A valid field \'columns\' not provided',
      status=HTTP_400_BAD_REQUEST)

  # Create new database instance and save it to database
  newDatabase = Database(
    user=user,
    created_on=now,
    last_modified=now,
    columns=str(columns).replace('\'', '"'),
    rows='[]'
  )
  newDatabase.save()

  # Return new database id
  return Response(newDatabase.id, status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def delete(request):
  # Get data from POST body
  user = request.user.username
  database_id = request.data.get('database_id')

  # Validate database_id
  if database_id is None:
    return Response('database_id field not provided.',
      status=HTTP_400_BAD_REQUEST)

  # Validate database_id exists under authenticated user
  try:
    database = Database.objects.get(id=database_id)
  except:
    return Response('database_id does not correspond to any database owned by this user',
      status=HTTP_400_BAD_REQUEST)
  if database.user != user:
    return Response('database_id does not correspond to any database owned by this user',
      status=HTTP_400_BAD_REQUEST)

  # Delete database
  try:
    database.delete()
  except:
    return Response('unable to delete database',
      status=HTTP_500_INTERNAL_SERVER_ERROR)
  
  return Response(status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def insert(request):
  # Get data from POST body
  user = request.user.username
  database_id = request.data.get('database_id')
  row = request.data.get('row')
  secret = request.data.get('secret')

  # Validate database_id
  if database_id is None:
    return Response('database_id field not provided.',
      status=HTTP_400_BAD_REQUEST)

  # Validate row
  try:
    row = str(row)
    row = json.loads(row)
  except:
    return Response('A valid field \'row\' not provided',
      status=HTTP_400_BAD_REQUEST)

  # Validate database_id exists under authenticated user
  try:
    database = Database.objects.get(id=database_id)
  except:
    return Response('database_id does not correspond to any database owned by this user',
      status=HTTP_400_BAD_REQUEST)
  if database.user != user and database.secret != secret:
    if database.user != user:
      return Response('database_id does not correspond to any database owned by this user',
        status=HTTP_400_BAD_REQUEST)
    else:
      return Response('secret does not correspond to database')
  
  # Validate new row follows database table columns
  try:
    for column in json.loads(database.columns):
      if str(column) not in row.keys():
        return Response(column)
        raise
  except:
    return Response('provided row does not abide by set columns',
      status=HTTP_400_BAD_REQUEST)

  # Append new values to table
  rows = json.loads(database.rows)
  rows.append(row)
  rows = str(rows).replace('\'', '"')

  # Update last_modified
  database.last_modified = timezone.now()

  # Commit changes to database
  database.rows = rows
  database.save()

  return Response(status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def remove(request):
  # Get data from POST body
  user = request.user.username
  database_id = request.data.get('database_id')
  comparisonColumn = request.data.get('comparisonColumn')
  comparison = request.data.get('comparison')
  operand = request.data.get('operand')

  # Validate database_id
  if database_id is None:
    return Response('database_id field not provided.',
      status=HTTP_400_BAD_REQUEST)

  # Validate database_id exists under authenticated user
  try:
    database = Database.objects.get(id=database_id)
  except:
    return Response('database_id does not correspond to any database owned by this user',
      status=HTTP_400_BAD_REQUEST)
  if database.user != user:
    return Response('database_id does not correspond to any database owned by this user',
      status=HTTP_400_BAD_REQUEST)

  # Validate comparison column
  if comparisonColumn is None:
    return Response('comparisonColumn field not provided',
      status=HTTP_400_BAD_REQUEST)
  
  # Validate comparison
  if comparison is None:
    return Response('comparison field not provided',
      status=HTTP_400_BAD_REQUEST)
  
  # Valideate operand
  if operand is None:
    return Response('operand field not provided',
      status=HTTP_400_BAD_REQUEST)
  
  # Get all columns from database
  columns = json.loads(database.columns)

  # Convert comparison input to enum
  try:
    if comparison == 'IS_EQUAL_TO':
      comparison = 'IS_NOT_EQUAL_TO'
    elif comparison == 'IS_NOT_EQUAL_TO':
      comparison = 'IS_EQUAL_TO'
    elif comparison == 'IS_LESS_THAN':
      comparison = 'IS_GREATER_THAN_OR_EQUAL_TO'
    elif comparison == 'IS_LESS_THAN_OR_EQUAL_TO':
      comparison = 'IS_GREATER_THAN'
    elif comparison == 'IS_GREATER_THAN':
      comparison = 'IS_LESS_THAN_OR_EQUAL_TO'
    elif comparison == 'IS_GREATER_THAN_OR_EQUAL_TO':
      comparison = 'IS_LESS_THAN'
    comparison = Comparison[comparison]
  except:
    return Response('invalid comparison provided')

  # Get rows of database after delete
  rows = findRow(database, columns, comparisonColumn, comparison, operand)

  return Response(rows)

  # Commit changes to saved database
  database.rows = str(rows).replace('\'', '"')
  database.save()

  return Response(status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def find(request):
  # Get data from POST body
  user = request.user.username
  database_id = request.data.get('database_id')
  columns = request.data.get('columns')
  comparisonColumn = request.data.get('comparisonColumn')
  comparison = request.data.get('comparison')
  operand = request.data.get('operand')

  # Validate database_id
  if database_id is None:
    return Response('database_id field not provided.',
      status=HTTP_400_BAD_REQUEST)

  # Validate database_id exists under authenticated user
  try:
    database = Database.objects.get(id=database_id)
  except:
    return Response('database_id does not correspond to any database owned by this user',
      status=HTTP_400_BAD_REQUEST)
  if database.user != user:
    return Response('database_id does not correspond to any database owned by this user',
      status=HTTP_400_BAD_REQUEST)
  
  # Validate columns
  if columns is None:
    return Response('columns field not provided',
      status=HTTP_400_BAD_REQUEST)
  
  # Validate columns is proper json
  try:
    selectedColumns = []
    if columns != '*':
      selectedColumns = json.loads(columns)
    else:
      selectedColumns = json.loads(database.columns)
  except:
    return Response('columns is not valid json',
      status=HTTP_400_BAD_REQUEST)

  # Convert comparison input to enum
  if comparison is not None:
    try:
      comparison = Comparison[comparison]
    except:
      return Response('invalid comparison provided')

  rows = findRow(database, selectedColumns, comparisonColumn, comparison, operand)

  return Response(rows, status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET', 'POST'])
def listAll(request):
  user = request.user.username

  databases = Database.objects.filter(user=user).all()
  databases_json = serializers.serialize('json', databases)
  return Response(databases_json, content_type='application/json', status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def changeSecret(request):
  # Get data from POST body
  user = request.user.username
  database_id = request.data.get('database_id')

  # Validate database_id
  if database_id is None:
    return Response('database_id field not provided.',
      status=HTTP_400_BAD_REQUEST)

  # Validate database_id exists under authenticated user
  try:
    database = Database.objects.get(id=database_id)
  except:
    return Response('database_id does not correspond to any database owned by this user',
      status=HTTP_400_BAD_REQUEST)
  
  # Change secret
  database.secret = generateSecret()
  database.save()

  return Response(database.secret, status=HTTP_200_OK)
