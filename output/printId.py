from dto.User import User as UserClass
from dto.Settings import Settings

#how to print extras
class printId:
    def doPrint(User:UserClass, Settings:Settings):
        file = Settings.getOutputFile()
        try:
            file.write(f"id: {User.getUserInfo().id or 'None'}\t")
            file.write(f"Name: {User.getUserInfo().first_name or 'None'} {User.getUserInfo().last_name or 'None'}\t")
            file.write(f"Username: {User.getUsername() or 'None'}\t")
            file.write(f"Bio: {User.getUserFullInfo().full_user.about or 'None'}\n")
            print(f"Data for {User.getUsername()} saved to {Settings.getOutputFileName()}")
        except Exception as e:
            print(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")
            file.write(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")