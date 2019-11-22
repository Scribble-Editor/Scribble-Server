import datetime

def writeFile(name, target, language, content):
    time = datetime.datetime.now()

    name.strip()

    fileName = name + "_" + target + "_src_" + time.strftime("%d-%m-%y_%H%M%S") + "." + language
    file = open(fileName, "+w")

    for line in content:
        file.write(line)

    file.close()

    return fileName
