from pydantic import BaseModel
from typing import List, TextIO
import sys
import os

class Settings(BaseModel):

    tokenIndex:int = 0 
    tokenList:List[str] = []
    botToken:str = "" 
     
    apiId:int
    apiHash:str
    tokens:str
    inputFile:str
    outputFile:str
    needle:str
    minimum:int
    timeout:int
    sleep:int
    outputType:str|None
    searchStrategy:str|None
    searchStrategyList:List[str] = []
    outputTypeList:List[str] = []

    #Singleton для работы с файлами
    IOFiles:dict = {} 

    class Config:
        arbitrary_types_allowed = True #Разрешает IO

    def __init__(self, **data):
        super().__init__(**data)

        self.tokenList = self.tokens.split(',')
        self.botToken = self.tokenList[self.tokenIndex]

        if self.outputType is not None and self.outputType != '':
            self.outputTypeList = self.outputType.split(',')
        
        if self.searchStrategy is not None and self.searchStrategy != '':
            self.searchStrategyList = self.searchStrategy.split(',')

    def getApiId(self) -> int:
        return self.apiId

    def getApiHash(self) -> str:
        return self.apiHash

    def getTokens(self) -> str:
        return self.tokens

    def getFileName(self) -> str:
        return self.inputFile

    def getResultFile(self) -> str:
        return self.outputFile

    def getNeedle(self) -> str:
        return self.needle

    def getMinimum(self) -> int:
        return self.minimum

    def getTimeout(self) -> int:
        return self.timeout

    def getSleep(self) -> int:
        return self.sleep

    def getTokensList(self) -> List[str]:
        return self.tokensList

    def getBotToken(self) -> str:
        return self.botToken

    def getSearchStrategyList(self) -> List[str]:
        return self.searchStrategyList

    def getOutputTypeList(self) -> List[str]:
        return self.outputTypeList
    
    def getNextToken(self) -> str:
        self.tokenIndex += 1

        if self.tokenIndex > len(self.tokenList):
            print("All bots have been used!")
            sys.exit()

        print(f"Switching to bot#{self.tokenIndex+1}")
        self.botToken = self.tokenList[self.tokenIndex]

        return self.botToken
    
    def getInputFile(self) -> TextIO:
        path = self.inputFile
        if path not in self.IOFiles:
            if not os.path.exists(path):
                print("Input file not found!")
                sys.exit()
            self.IOFiles[path] = open(path,'r',encoding='utf-8')
        return self.IOFiles[path]

    def getOutputFile(self) -> TextIO:
        path = self.outputFile
        if path not in self.IOFiles:
            self.IOFiles[path] = open(path,'a',encoding='utf-8')
        return self.IOFiles[path]