<<<<<<< Updated upstream
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT
from rest_framework.response import Response


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
  """
  Login to user
  """
  username = request.data.get('username')
  password = request.data.get('password')
  if username is None or password is None:
    return Response({'error': 'Please provide both username and password'},
      status=HTTP_400_BAD_REQUEST)
  user = authenticate(username=username, password=password)
  if not user:
    return Response({'error': 'Invalid Credentials'},
      status=HTTP_404_NOT_FOUND)
  token, _ = Token.objects.get_or_create(user=user)
  return Response({'token': token.key},
    status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
  """
  Register new user
  """
  # If username, password, and email are not all provided, return 400 - Bad Request
  username = request.data.get('username')
  password = request.data.get('password')
  email = request.data.get('email')
  if username is None or password is None or email is None:
    return Response({'error': 'Please provided username, password, and email'},
      status=HTTP_400_BAD_REQUEST)

  # If account with name already exists, return 409 - Conflict
  if User.objects.filter(username=username).exists():
    return Response({'error': 'An account with that name already exists'},
      status=HTTP_409_CONFLICT)

  # Create and save new user
  user = get_user_model().objects.create_user(username=username, password=password, email=email)
  user.save()

  # Authenticate user, if an error occurs, return 500 - Internal Server Error
  user = authenticate(username=username, password=password)
  if user is None:
    return Response({'error': 'An unexpected error has ocurred while registering account. Try again.'},
      status=HTTP_500_INTERNAL_SERVER_ERROR)

  # Get user token and return it
  token, _ = Token.objects.get_or_create(user=user)
  return Response({'token': token.key},
    status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def logout(request):
  """
  Logout of user account
  """
  # Get token to delete
  token = request.data.get('token')

  # Delete token

  try:
    instance = Token.objects.get(key=token)
    instance.delete()
    return Response(status=HTTP_200_OK)
  except:
    return Response(status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def sample_api(request):
  """
  Sample API used to test authentication
  """
  data = { 'sample_data': 123 }
  return Response(data, status=HTTP_200_OK)
=======
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT
from rest_framework.response import Response


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
  """
  Login to user
  """
  username = request.data.get('username')
  password = request.data.get('password')
  if username is None or password is None:
    return Response({'error': 'Please provide both username and password'},
      status=HTTP_400_BAD_REQUEST)
  user = authenticate(username=username, password=password)
  if not user:
    return Response({'error': 'Invalid Credentials'},
      status=HTTP_404_NOT_FOUND)
  token, _ = Token.objects.get_or_create(user=user)
  return Response({'token': token.key},
    status=HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
  """
  Register new user
  """
  # If username, password, and email are not all provided, return 400 - Bad Request
  username = request.data.get('username')
  password = request.data.get('password')
  email = request.data.get('email')
  if username is None or password is None or email is None:
    return Response({'error': 'Please provided username, password, and email'},
      status=HTTP_400_BAD_REQUEST)
  
  # If account with name already exists, return 409 - Conflict
  if User.objects.filter(username=username).exists():
    return Response({'error': 'An account with that name already exists'},
      status=HTTP_409_CONFLICT)

  # Create and save new user
  user = get_user_model().objects.create_user(username=username, password=password, email=email)
  user.save()

  # Authenticate user, if an error occurs, return 500 - Internal Server Error
  user = authenticate(username=username, password=password)
  if user is None:
    return Response({'error': 'An unexpected error has ocurred while registering account. Try again.'},
      status=HTTP_500_INTERNAL_SERVER_ERROR)
  
  # Get user token and return it
  token, _ = Token.objects.get_or_create(user=user)
  return Response({'token': token.key},
    status=HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def sample_api(request):
  """
  Sample API used to test authentication
  """
  data = { 'sample_data': 123 }
  return Response(data, status=HTTP_200_OK)
>>>>>>> Stashed changes
