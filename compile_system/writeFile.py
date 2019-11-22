import datetime
from os import getcwd
import json

def writeFile(name, target, language, content):
    time = datetime.datetime.now()

    name = name.strip() #This should protect the compiler container from 

    fileName =  name + "_" + target + "_src_" + time.strftime("%d-%m-%y_%H%M%S") + "." + language

    file = open(getInputPath(fileName), "+w")

    try:
        content = json.loads(content)
    except:
        raise

    for line in content:
        file.write(line + '\n')

    file.close()

    return fileName

def getInputPath(fileName):
    path = getcwd() + '/src/'
    return str(path + fileName).strip()    


def getOutputPath(fileName):
    path = getcwd() + '/build/'
    return str(path + fileName).strip()