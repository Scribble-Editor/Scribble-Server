from .writeFile import getInputPath, getOutputPath

def constructCompileStatement(target, language, fileName):
    
    command = determineTarget(target) + determineCompiler(target, language)
    staticLinkParam = determineStaticLibraryLink(target, language)

    inputPath = getInputPath(fileName)

    outputFileName = fileName
    outputFileName = outputFileName.strip("." + language)

    outputPath = getOutputPath(outputFileName)

    removeCommand = "rm -rf " + inputPath

    return (str(command + " " + inputPath + " -o " + outputPath).strip(), removeCommand.strip())

def constructInterpretStatement(language, fileName):

    command = determineInterpreter(language);

    inputPath = getInputPath(fileName)
    removeCommand = "rm " + inputPath

    #Not sure if we should be using the booleanity (?) of python. 
    #But if the language isnt on the approved list, this should prevent that from happening.
    #Ignore the lisp-like nature of the tuple below. It doesn't exist if you can't see it, right?
    return (str(determineInterpreter(language) + " " + inputPath).strip(), removeCommand.strip())

def determineCompiler(target, language):

    if (language == "cpp") and ("win" in target):
        return "mingw32-g++"

    elif (language == "c") and ("win" in target):
        return "mingw32-gcc"

    elif (language == "cpp") and ("linux" in target):
        return "g++"

    elif (language == "c") and ("linux" in target):
        return "gcc"
    
    else:
        return ""

def determineInterpreter(language):
    if language == "python":
        return "python3 -u"

    elif language == "ruby":
        return "ruby"

    elif language == "js":
        return "node"

    else: 
        return ""

def determineTarget(target):

    if target == "win64":
        return "x86_64-w64-"

    elif target == "win32":
        return "i686-w64-"

    else:
        return ""

def determineStaticLibraryLink(target, language):
    if target == "linux":
        return ""

    if language == "cpp":
        return " -static-libstdc++"
    
    elif language == "c":
        return " -static-libgcc"
    
    else:
        return ""