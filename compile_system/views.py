from compile_system.statement import constructCompileStatement, constructInterpretStatement
from compile_system.writeFile import writeFile

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT
from rest_framework.response import Response

import requests

def getItemsFromReq(request):
    name = request.get("name") #Scribblet name
    target = request.get("target") #Operating System/Architecture (e.g. Win64, Win32, Linux)
    language = request.get("lang") #Language in the form of file extension (e.g. cpp, c, rb, py)
    content = request.get("content") #Code

    return (name, target, language, content)

@api_view(['POST', 'GET'])
@permission_classes((AllowAny,))
def compileScribblet(request):
    
    (name, target, language, content) = getItemsFromReq(request)
    print("I made it here!")
    if not name or not target or not language or not content:
        return Response({'error': 'Missing attribtes, did you forget to set something?'},
      status=HTTP_400_BAD_REQUEST)

    fileName = writeFile(name, target, language, content)
    compileCommnd = constructCompileStatement(target, language, fileName)

    url = "hi"
    #url = requests.get("http://scribble-compiler/?command=" + compileCommnd)

    return Response(url)

@api_view(['POST', 'GET'])
@permission_classes((AllowAny,))
def interpretScribblet(request):    

    (name, target, language, content) = getItemsFromReq(request)

    if not name or not language or not content:
            return Response({'error': 'Missing attribtes, did you forget to set something?'},
      status=HTTP_400_BAD_REQUEST)

    fileName = writeFile(name, target, language, content)
    compileCommnd = constructInterpretStatement(language, fileName)

    url = requests.get("http://scribble-compiler/?command=" + compileCommnd)

    return Response(url)