import os

def saveResponse(text:str, dir:str) -> bool:
    """
        Saves file in dir, with name save.txt, if save.txt exists, saves as save1.txt, save2.txt, etc.
    """
    try:
        fileDir = dir
        file = "save"
        fileSuffix = ".txt"
        extra = 0
        if os.path.exists(fileDir + "/" + file + fileSuffix):
            extra += 1
            while os.path.exists(fileDir + "/" + file + str(extra) + fileSuffix):
                extra += 1
            file = file + str(extra)
        with open(fileDir + "/" + file + fileSuffix, 'w') as file:
            file.write(text)
    except:
        return False
    return True