from dto import User as UserClass
from dto import Settings

class printRaw:
    def doPrint(User:UserClass, Settings:Settings):
        try:
            Settings.getOutputFile().write(f"info: {User.getUserInfo() or 'None'}\t")
            Settings.getOutputFile().write(f"full: {User.getUserFullInfo() or 'None'}\n")
            print(f"Data for {User.getUsername()} saved to {Settings.getOutputFileName()}")
        except Exception as e:
            print(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")
            Settings.getOutputFile().write(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")