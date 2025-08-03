from dto.User import User as UserClass
from dto.Settings import Settings

class printRaw:
    def doPrint(User:UserClass, Settings:Settings):
        file = Settings.getOutputFile()
        file.write(f"info: {User.getUserInfo().stringify() or 'None'}\t")
        file.write(f"full: {User.getUserFullInfo().stringify() or 'None'}\n")