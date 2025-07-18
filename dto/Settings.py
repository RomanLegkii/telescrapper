class Settings:
    from typing import ClassVar
    import os
    
    tokenIndex = 0
    botToken:str
    tokensList:list

    def __init__(self,
            apiId:int,
            apiHash:int,
            tokens:str,
            fileName:str,
            resultFile:str,
            needle:str,
            minimum:int,
            timeout:int,
            sleep:int,
            outputType:str|None):
        self.apiId = apiId
        self.apiHash = apiHash
        self.tokens = tokens
        self.fileName = fileName
        self.resultFile = resultFile
        self.needle = needle
        self.minimum = minimum
        self.timeout = timeout
        self.sleep = sleep
        self.outputType = outputType

    def getApiId(self):
        return self.apiId
