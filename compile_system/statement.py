def constructStatement(target, language, fileName):
    
    command = determineCompiler(target, language) + determineTarget(target)
    staticLinkParam = determineStaticLibraryLink(language)

    outputFileName = fileName
    outputFileName.strip(".")
    outputFileName.strip(language)

    return command + (" " + staticLinkParam if not staticLinkParam else "") + " " + fileName + " -o " + outputFileName

def determineCompiler(target, language):

    if (language is "cpp") and ("win" in target):
        return "g++-mingw-"

    elif (language is "c") and ("win" in target):
        return "gcc-mingw-"

    elif (language is "cpp") and ("linux" is target):
        return "g++"

    elif (language is "c") and ("linux" is target):
        return "gcc"
    
    else:
        return ""

def determineTarget(target):

    if target is "win64":
        return "w64-x86-64"

    elif target is "win32":
        return "w64-i686 -"

    else:
        return ""

def determineStaticLibraryLink(language):

    if language is "cpp":
        return "-static-libstdc++"
    
    elif language is "c":
        return "-static-libstdc"
    
    else:
        return ""

print (constructStatement("win64", "cpp", "hello.cpp"))