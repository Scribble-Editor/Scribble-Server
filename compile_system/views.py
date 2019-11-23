from compile_system.statement import constructCompileStatement, constructInterpretStatement
from compile_system.writeFile import writeFile
from compile_system.models import Scribblet

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT
from rest_framework.response import Response

import requests   
from urllib.parse import quote

def getItemsFromReq(request):
  
    name = request.data.get("name") #Scribblet name
    target = request.data.get("target") #Operating System/Architecture (e.g. Win64, Win32, Linux)
    language = request.data.get("lang") #Language in the form of file extension (e.g. cpp, c, rb, py)
    content = request.data.get("content") #Code

    return (name, target, language, content)

@api_view(['POST'])
@permission_classes((AllowAny,))
def compileScribblet(request):
    
    (name, target, language, content) = getItemsFromReq(request)
    print("I made it here!")
    if not name or not target or not language or not content:
        return Response({'error': 'Missing attribtes, did you forget to set something?'},
      status=HTTP_400_BAD_REQUEST)

    try:
      fileName = writeFile(name, target, language, content)
    except:
      return Response('Error writing file',
        status=HTTP_400_BAD_REQUEST)

    compileCommnd = constructCompileStatement(target, language, fileName)
    compileCommnd = quote(compileCommnd)

    url = requests.get("http://scribble-compiler/?command=" + compileCommnd)

    if url.status_code != 200:
      return Response('Error performing request',
        status=HTTP_400_BAD_REQUEST)

    return Response(url)

@api_view(['POST'])
@permission_classes((AllowAny,))
def interpretScribblet(request):    

    (name, target, language, content) = getItemsFromReq(request)

    if not name or not language or not content:
            return Response({'error': 'Missing attribtes, did you forget to set something?'},
      status=HTTP_400_BAD_REQUEST)

    fileName = writeFile(name, target, language, content)
    interpretCommand = constructInterpretStatement(language, fileName)

    url = requests.get("http://scribble-compiler/?command=" + interpretCommand)

    if url.status_code != 200:
      return Response('an error has occurred',
        status=HTTP_400_BAD_REQUEST)

    return Response(str(url.text))