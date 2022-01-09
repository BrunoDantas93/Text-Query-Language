import os
import os.path as path
import csv

class FileManipulation:

    @staticmethod
    def ValidFile(FileName, type):
        if FileName.endswith(type.upper()) or FileName.endswith(type.lower()):
            return [True]
        else:
            return [False, "The file [" + str(FileName) + "] is compatible "]

    @staticmethod
    def __FileExist(FileNmae):
        if path.exists(FileNmae) is False:
            response = [False, "THe file [" + str(FileNmae) + "] not exit"]
            return response
        else:
            return [True]


    @staticmethod
    def OpenFile(FileName, type):

        FileTest = FileManipulation.__FileExist(FileName)

        if FileTest[0] is False:
            return [False, FileTest[1]]

        validfile = FileManipulation.ValidFile(FileName, type)

        if validfile[0] is False:
            return [False, validfile[1]]

        with open(FileName, 'r', encoding='utf-8') as fh:
            contents = fh.readlines()
        fh.close()

        if not contents:
            return [False, "In the folder ["+str(FileName)+"] don't have any files"]
        else:
            return [True, contents]


    @staticmethod
    def CreateFile(Path, FileName, data):

        FileTest = FileManipulation.__FileExist(FileName)

        if FileTest[0] is True:
            return [False, "The file { " + FileName + " } already exists"]

        file = open(Path+""+FileName, "w", encoding='utf-8')

        w = csv.writer(file)

        i = 0
        position = {}
        length = len(data) - 1
        for key in data:
            position[key] = i
            if ',' in str(key):
                key = '"' + str(key) + '"'
            if i != length:
                file.write(str(key) + ",")
            else:
                file.write(str(key))
            i += 1
        file.write("\n")

        length = len(data[list(data.keys())[0]])
        for i in range(0, length):
            temp = [i]
            x = 0
            for k, v in position.items():
                v = data[k][i]
                if ',' in str(v):
                    key = '"' + str(v) + '"'
                if x != (len(data) - 1):
                    file.write(str(v) + ",")
                else:
                    file.write(str(v))
                x += 1
            file.write("\n")