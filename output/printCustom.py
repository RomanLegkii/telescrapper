from dto.User import User as UserClass
from dto.Settings import Settings
from output.PrintStrategy import Output

#how to print extras
class printCustom:
    def doPrint(User:UserClass, Settings:Settings):

        outputType = Settings.getOutputTypeList()
        
        info = User.getUserInfo()   #нужны для locals().get(cl)
        full = User.getUserFullInfo()

        for string in outputType:
            
            if ':' not in string:
                nativeOutput = Output().getOutput(string)
                if len(nativeOutput) > 0:
                    nativeOutput[string].doPrint(User,Settings)
                continue

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