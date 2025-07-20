from dto.User import User as UserClass
from dto.Settings import Settings

class printRaw:
    def doPrint(User:UserClass, Settings:Settings):
        file = Settings.getOutputFile()
        try:
            file.write(f"info: {User.getUserInfo().stringify() or 'None'}\t")
            file.write(f"full: {User.getUserFullInfo().stringify() or 'None'}\n")
            print(f"Data for {User.getUsername()} saved to {Settings.getOutputFileName()}")
        except Exception as e:
            print(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")
            file.write(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")