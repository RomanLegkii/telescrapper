from dto.User import User as UserClass
from dto.Settings import Settings

class printDefault:
    def doPrint(User:UserClass, Settings:Settings):
        file = Settings.getOutputFile()
        try:
            # with Settings.getOutputFile() as file:
            file.write(f"Username: {User.getUsername() or 'None'}\t")
            file.write(f"Bio: {User.getBio() or 'None'}\n")
            print(f"Data for {User.getUsername()} saved to {Settings.getOutputFileName()}")
        except Exception as e:
            print(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")
            file.write(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")