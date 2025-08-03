from dto.Settings import Settings
from typing import TextIO

class ErrorLog:

    def doLog(Settings:Settings, Error:Exception, Message:str) :
        if Settings.getPrintErrors() == True:
            Settings.getOutputFile().write(f"{Message} {str(Error)} \n")