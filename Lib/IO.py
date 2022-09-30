from Lib import UtilLib

ReaderType_PBD_NEW = "New"
ReaderType_PBD_OLD = "Old"


class Reader:
    def __init__(self):
        self._filePath = None
        self._fileDataList = list()
        self._Exist = True
        self._encoding = 'UTF-8'

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, value):
        #print("Reader : "+value)
        if UtilLib.isExist(value):
            self._filePath = value
            self._Exist = True
            #print("[Reader] Success - File[ {} ] is exists.".format(UtilLib.getOnlyFileName(value)))
        else :
            self._Exist = False
            print("[Reader] Error - File[ {} ] not found.".format(UtilLib.getOnlyFileName(value)))


    @property
    def fileDataList(self):
        return self._fileDataList

    @fileDataList.setter
    def fileDataList(self,value_list):
        self._fileDataList = value_list

    def running(self, type=None):
        if type is None:
            self._readFile()
        elif type is ReaderType_PBD_NEW:
            self._readFile_PBD()
        elif type is ReaderType_PBD_OLD:
            self._readFile_PBD_oldVersion()
        """
        elif type is "NVH3":
            self.__readFile_nvh3()
        """


    def _readFile(self):
        if self._Exist:
            try :
                with open(file=self.filePath, mode='rt', encoding=self._encoding) as fileObj:
                    lines = fileObj.readlines()

                    # 데이터 읽어올때 누락 시킬 부분 조건문으로 누락시키고 fileDataList에 추가
                    for line in lines:
                        # 읽어온 라인의 길이가 0 이 아닌것들은 데이터 추가
                        line = UtilLib.removeSideBlank(line)
                        if len(line) != 0:
                            # 개행문자 제거하여 읽어옴
                            self._fileDataList.append(line.replace("\n", ""))
                        else :
                            #self._fileDataList.append("EMPTY_LINE_DATA")
                            pass
                    #print("[Reader] Success - Reading File is complete. \n\t=> {}".format(self.filePath))
            except Exception as err:
                if self._encoding == 'UTF-8':
                    self._encoding = 'cp949'
                    self._readFile()
                elif self._encoding == 'cp949':
                    self._encoding = 'UTF-8'
                    self._readFile()
                else:
                    print("[Reader] - Error \n\t=> {}".format(err))
        else:
            print("[Reader] Error - File[{}] not found.".format(UtilLib.getOnlyFileName(self.filePath)))

    def _readFile_PBD(self):
        if self._Exist:
            try :
                with open(file=self.filePath, mode='rt', encoding=self._encoding) as fileObj:
                    lines = fileObj.readlines()

                    # 데이터 읽어올때 누락 시킬 부분 조건문으로 누락시키고 fileDataList에 추가
                    for line in lines:
                        # 읽어온 라인의 길이가 0 이 아닌것들은 데이터 추가, 특수 문자 제거 추가
                        line = UtilLib.removeSideBlank(line)
                        #if len(line) != 0 and (UtilLib.strContains(line, "") is not True or (UtilLib.strContains(line, ".") is not True)):
                        if len(line) != 0 and line not in ["."]:
                            # 개행문자 제거하여 읽어옴
                            #self._fileDataList.append(line.replace("\n", "").replace("/","7"))
                            self._fileDataList.append(line.replace("\n", ""))
                        else :
                            #self._fileDataList.append("EMPTY_LINE_DATA")
                            pass
                    #print("[Reader] Success - Reading File is complete. \n\t=> {}".format(self.filePath))
            except Exception as err:
                if self._encoding == 'UTF-8':
                    self._encoding = 'cp949'
                    self._readFile_PBD()
                elif self._encoding == 'cp949':
                    self._encoding = 'UTF-8'
                    self._readFile_PBD()
                else:
                    print("[Reader] - Error \n\t=> {}".format(err))
        else:
            print("[Reader] Error - File[{}] not found.".format(UtilLib.getOnlyFileName(self.filePath)))

    def _readFile_PBD_oldVersion(self):
        if self._Exist:
            try :
                with open(file=self.filePath, mode='rt', encoding=self._encoding) as fileObj:
                    lines = fileObj.readlines()

                    # 데이터 읽어올때 누락 시킬 부분 조건문으로 누락시키고 fileDataList에 추가
                    for line in lines:
                        # 읽어온 라인의 길이가 0 이 아닌것들은 데이터 추가, 특수 문자 제거 추가
                        line = UtilLib.removeSideBlank(line)
                        #if len(line) != 0 and (UtilLib.strContains(line, "") is not True or (UtilLib.strContains(line, ".") is not True)):
                        if len(line) != 0 and line not in ["."]:
                            # 개행문자 제거하여 읽어옴
                            #self._fileDataList.append(line.replace("\n", "").replace("/","7"))
                            self._fileDataList.append(line.replace("\n", ""))
                        else :
                            #self._fileDataList.append("EMPTY_LINE_DATA")
                            pass
                    #print("[Reader] Success - Reading File is complete. \n\t=> {}".format(self.filePath))
            except Exception as err:
                if self._encoding == 'UTF-8':
                    self._encoding = 'cp949'
                    self._readFile_PBD()
                elif self._encoding == 'cp949':
                    self._encoding = 'UTF-8'
                    self._readFile_PBD()
                else:
                    print("[Reader] - Error \n\t=> {}".format(err))
        else:
            print("[Reader] Error - File[{}] not found.".format(UtilLib.getOnlyFileName(self.filePath)))

    """
    def __readFile_nvh3(self):
        if self._Exist:
            try :
                with open(file=self.filePath, mode='r') as fileObj:
                    lines = fileObj.readlines()

                    # 데이터 읽어올때 누락 시킬 부분 조건문으로 누락시키고 fileDataList에 추가
                    for line in lines:
                        # 읽어온 라인의 길이가 0 이 아닌것들은 데이터 추가
                        if len(line) is not 0:
                            # 개행문자 제거하여 읽어옴
                            if UtilLib.strContains(data=line, findValue= '$'):
                                self._fileDataList.append(line.replace("\n", ""))
                            else:
                                if not UtilLib.strContains(data=line, findValue= "-CONT-"):
                                    self._fileDataList.append(line.replace("\n", ""))


                    #print("[Reader] Success - Reading File is complete. \n\t=> {}".format(self.filePath))
            except Exception as err:
                print("[Reader] - Error \n\t=> {}".format(err))
        else:
            print("[Reader] Error - File[{}] not found.".format(UtilLib.getOnlyFileName(self.filePath)))
    """

class Writer:
    def __init__(self):
        self._filePath = None
        self._fileDataList = list()

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, value):
        self._filePath = value

    @property
    def fileDataList(self):
        return self._fileDataList

    @fileDataList.setter
    def fileDataList(self, value_list):
        self._fileDataList = value_list

    def running(self):
        self._writeFile()

    def _writeFile(self):
        try:
            with open(file=self.filePath, mode='w',encoding="utf-8") as fileObj:
                for line in self.fileDataList:
                    newLine = line.rstrip("\n")
                    #newLine = UtilLib.convertToString(line).rstrip("\n")
                    fileObj.writelines(newLine + "\n")
                #print("[Writer] Success - Writing File is complete. \n\t=> {}".format(self.filePath))
        except Exception as err:
            print("[Writer] - Error \n\t=> {}".format(err))


"""
######################################
# Reader sample
fReader = Reader()
fReader.filePath = filePath
fReader.running()
for line in fReader.fileDataList:
    print(line)
######################################
# Writer sameple
fWriter = Writer()
fWriter.filePath = filePath
fWriter.fileDatalist = outputDataList
fwriter.running()
######################################
"""