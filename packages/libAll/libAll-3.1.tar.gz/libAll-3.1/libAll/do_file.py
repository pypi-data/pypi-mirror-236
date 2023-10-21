file_storage = ""

def afile(filename, mode1='r', mode2='read', mode3='', encodingf='utf-8'):
    global file_storage
    try:
        file_storage = open(filename, mode1, encoding=encodingf)
        if mode3 == '':
            return eval("file_storage." + mode2 + '(' + str(mode3) + ')')
            file_storage.close()
        else:
            return eval("file_storage." + mode2 + '("' + str(mode3) + '")')
            file_storage.close()
    except:
        return "FATAL ERROR filewere construction or library construction"