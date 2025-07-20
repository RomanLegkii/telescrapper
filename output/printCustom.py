from dto.User import User as UserClass
from dto.Settings import Settings

#how to print extras
class printCustom:
    def doPrint(User:UserClass, Settings:Settings):
        try:

            outputType = Settings.getOutputTypeList()
            info = User.getUserInfo()   #нужны для locals().get(cl)
            full = User.getUserFullInfo()

            for string in outputType:
                cl, obj = string.split(':')

                target_obj = locals().get(cl)
                if target_obj is None:
                    raise ValueError(f"Объект {cl} не найден")

                objects = obj.split('.')
                for objec in objects:
                    target_obj = getattr(target_obj,objec)

                stringTypes = [int,str]
                if type(target_obj) in stringTypes or target_obj is None:
                    Settings.getOutputFile().write(f"{obj}: {target_obj}\t")
                else: 
                    Settings.getOutputFile().write(f"{obj}: {target_obj.stringify()}\t")

            Settings.getOutputFile().write("\n")
            print(f"Custom data for {User.getUsername()} saved to {Settings.getOutputFileName()}")

        except Exception as e:
            print(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")
            Settings.getOutputFile().write(f"Error for: {User.getUsername() or 'None'}: {str(e)} \n")