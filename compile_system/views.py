import datetime
import compile_system.statement

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT
from rest_framework.response import Response

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def compileScribblet(request):
    name = request.get("name")
    target = request.get("target")
    language = request.get("lang")
    content = request.get("content")

    time = datetime.datetime.now()

    fileName = name + "_" + target + "_src_" + time.strftime("%d-%m-%y_%H%M%S") + "." + language
    file = open(fileName, "+w")

    for line in content:
        file.write(line)

    file.close()

    compileCommnd = determineCompiler(target, language, fileName)

    

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def getWebhook(request):
    return ""