#di
from pydantic import BaseModel
from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from fuzzywuzzy import fuzz
from functools import wraps
import asyncio
import os
import sys
from decorators.checkBio import check_bio as checkBio 
from decorators.checkBioFuzzy import  checkBioFuzzy 
from decorators.checkBioContains import  checkBioContains 
from decorators.checkPhoto import  checkPhoto 
from decorators.checkChannel import  checkChannel 
from dotenv import load_dotenv
from dto.Settings import Settings
from dto.Bot import Bot
from dto.User import User
from typing import TextIO

isLoaded = load_dotenv('vars.env')
if isLoaded is False:
    print('.env file not found')
    sys.exit()

SETTINGS = Settings(
    apiId=os.getenv('API_ID'),
    apiHash = os.getenv('API_HASH'),
    tokens = os.getenv('BOT_TOKENS'),
    inputFile = os.getenv('SRC_FILENAME'),
    outputFile = os.getenv('RESULT_FILENAME'),
    needle = os.getenv('NEEDLE'),
    minimum = os.getenv('RATIO'),
    timeout = os.getenv('TIMEOUT_LIMIT'),
    sleep = os.getenv('SLEEP_TIME'),
    outputType = os.getenv('OUTPUT_TYPE'),
    searchStrategy = os.getenv('SEARCH_STRATEGY')
)
BOT =  Bot(
    botToken = SETTINGS.getBotToken(), 
    apiId = SETTINGS.getApiId(), 
    apiHash = SETTINGS.getApiHash()
)

print(SETTINGS.getOutputTypeList())


def printCustomInfo(info,full,bio,file):
    global outputType

    if type(outputType) == str:
        outputType = [outputType]

    for string in outputType:
        cl, obj = string.split(':')

        target_obj = locals().get(cl)
        if target_obj is None:
            raise ValueError(f"Объект {cl} не найден")

        objects = obj.split('.')
        for objec in objects:
            target_obj = getattr(target_obj,objec)

        if type(target_obj) == str or type(target_obj) == int:
            file.write(f"{obj}: {target_obj}\t")
        else: 
            file.write(f"{obj}: {target_obj.stringify()}\t")
    file.write("\n")
    print(f"Custom data for @{info.username or info.id} saved to {resultFile}")


def printInfo(User:User):#переделать бы
    info = User.getUserInfo()
    full = User.getUserFullInfo()
    bio = User.getBio()
    file = SETTINGS.getOutputFile()
    print(User.stringify())
    file.write('oop hustla')
    sys.exit()
    global outputType
    if outputType == 'id_name_username_bio':
        extra = {}
        if hasattr(full.full_user,'personal_channel_id') and full.full_user.personal_channel_id is not None:
            extra['channel_id'] = full.full_user.personal_channel_id
        if hasattr(info,'photo') and info.photo is not None:
            extra['photo'] = info.photo

        if extra is not None:
            keys = extra.keys()
        try:
            file.write(f"ID: {info.id}\t")
            file.write(f"Name: {info.first_name or 'None'} {info.last_name or 'None'}\t")
            file.write(f"Username: @{info.username or 'None'}\t")
            file.write(f"Bio: {bio or 'None'}\t")
            if 'keys' in locals():
                for key in keys:
                    file.write(f"{key}: {extra[key]}\t")
            file.write("\n")
            print(f"Data for @{info.username or info.id} saved to {resultFile}")
      
        except Exception as e:
            file.write(f"Error for @{info.username or info.id}: {str(e)}\n")
            print(f"Error for @{info.username or info.id}: {str(e)}")
    elif outputType == 'raw':
        try:
            file.write(f"info: {info.stringify()}\n")
            file.write(f"full: {full.stringify()}\n")
        except Exception as e:
            file.write(f"Error for @{info.username or info.id}: {str(e)}\n")
            print(f"Error for @{info.username or info.id}: {str(e)}")
    elif outputType == '' or outputType is None:
        try:
            file.write(f"Username: @{info.username or 'None'}\t")
            file.write(f"Bio: {bio or 'None'}\n")
            print(f"Data for @{info.username or info.id} saved to {resultFile}")
        except Exception as e:
            file.write(f"Error for @{info.username or info.id}: {str(e)}\n")
            print(f"Error for @{info.username or info.id}: {str(e)}")
    else:
        printCustomInfo(info,full,bio,file)

# Base
async def do_search(User):
    print(f"Found match @{User.getUsername()}")
    return User

# Функция для компоновки декораторов
def apply_filters(filters, base_func):

    decorators = [filter_decorators[f] for f in filters if f in filter_decorators]
    decorated_func = base_func
    for decorator in reversed(decorators):
        decorated_func = decorator(decorated_func)
    return decorated_func

# Регистрация декораторов
filter_decorators = {
    "bio": checkBio,
    "channel": checkChannel,
    "photo": checkPhoto,
    "bio_contains": checkBioContains,
    "bio_fuzzy": checkBioFuzzy,
}





# async def processUser(id,f):
#     global bot
#     try:
#         info = await asyncio.wait_for(bot.get_entity(id), timeout=timeout)
#         full = await asyncio.wait_for(bot(GetFullUserRequest(id)), timeout=timeout)

#         print(f"Waiting {sleep} seconds") #move to the end
#         await asyncio.sleep(sleep)
#         bio = full.full_user.about

#         filtered_search = apply_filters(selectedStrategies, do_search)
#         result = await filtered_search(info, full, bio, f)
#         if result is None:
#             return
#         printInfo(result['info'],result['full'], result['bio'], f)

#     except asyncio.TimeoutError:
#          f.write(f"Timeout for {id}\n")
#          print(f"Timeout for {id}")

#     except Exception as e:
#         if "A wait of" in str(e):
#             f.write(f"Error for {id}: {str(e)}\n")
#             print(f"Error for {id}: {str(e)}")

#             switchBot()

#             await processUser(id,f)
#             return

#         f.write(f"Error for {id}: {str(e)}\n")
#         print(f"Error for {id}: {str(e)}")


class Main(BaseModel):

    inputFile:TextIO = SETTINGS.getInputFile()
    outputFile:TextIO = SETTINGS.getOutputFile()

    class Config:
        arbitrary_types_allowed = True #Разрешает IO

    def __init__(self,**data):
        super().__init__(**data)

    async def main(self):
        
        BOT.removeSession()
        BOT.sessionStart()
        foundWorkingBot = False
        while(foundWorkingBot == False):
            try:
                await BOT.setBot()
            except Exception as e:
                print(str(e))
                if "A wait of" in str(e):
                    await self.switchBot()
            finally:
                foundWorkingBot = True
                
        for line in self.inputFile:
            await self.processLine(line)
    
    
    async def processLine(self, line):
        username = line.strip()
        print(f"Processing {username}")
    
        if '@' not in username:
            return

        USER = User(username = username)

        USER.setUserInfo(await BOT.getUser(USER,SETTINGS),) #so tight step bro
        USER.setUserFullInfo(await BOT.getUserFull(USER,SETTINGS)) #i want to see your big biautiful interface

        await asyncio.sleep(SETTINGS.getSleep())

        filtered_search = apply_filters(SETTINGS.getSearchStrategyList(), do_search)
        result = await filtered_search(USER,SETTINGS)
        if result is not None:
            printInfo(result)

    async def switchBot(self):
        try:
            await BOT.deleteBot()
            BOT.sessionStart()
            BOT.setToken(SETTINGS.getNextToken())
            await BOT.setBot()
        except Exception as e:
            print(str(e))
            if "A wait of" in str(e):
                await self.switchBot()
    

if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main())
