from dto.User import User as UserClass
from dto.Settings import Settings

class printDefault:
    def doPrint(User:UserClass, Settings:Settings):
        file = Settings.getOutputFile()
        file.write(f"Username: {User.getUsername() or 'None'}\t")
        file.write(f"Bio: {User.getBio() or 'None'}\t")