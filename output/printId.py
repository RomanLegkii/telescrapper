from dto.User import User as UserClass
from dto.Settings import Settings

#how to print extras
class printId:
    def doPrint(User:UserClass, Settings:Settings):
        file = Settings.getOutputFile()
        file.write(f"id: {User.getUserInfo().id or 'None'}\t")
        file.write(f"Name: {User.getUserInfo().first_name or 'None'} {User.getUserInfo().last_name or 'None'}\t")
        file.write(f"Username: {User.getUsername() or 'None'}\t")
        file.write(f"Bio: {User.getUserFullInfo().full_user.about or 'None'}\t")