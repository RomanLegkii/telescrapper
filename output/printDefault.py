from dto import User as UserClass
from dto import Settings

class printDefault:
    @staticmethod
    def doPrint(User:UserClass, Settings:Settings):
        try:
            file = Settings.getOutputFile()
            file.write(f"Username: {User.getUsername() or 'None'}\t")
            Settings.getOutputFile().write(f"Bio: {User.getBio() or 'None'}\n")
            Settings.getOutputFile().write('123')
            print(f"Data for {User.getUsername()} saved to {Settings.getOutputFileName()}")
        except Exception as e:
            print(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")
            Settings.getOutputFile().write(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")