#di
import asyncio
import os
import sys
from output.PrintStrategy import Output
from dotenv import load_dotenv
from dto.Settings import Settings
from dto.Bot import Bot
from dto.User import User
from typing import TextIO
from decorators.FilterDecoratos import Filter
from output.printCustom import printCustom

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

# Base
async def do_search(User:User, Settings:Settings):
    print(f"Found match {User.getUsername()}")
    return User

# Функция для компоновки декораторов
def apply_filters(filters, base_func):
    filter_decorators=Filter().getFilters(SETTINGS.getSearchStrategyList())
    decorators = [filter_decorators[f] for f in filters if f in filter_decorators]
    decorated_func = base_func
    for decorator in reversed(decorators):
        decorated_func = decorator(decorated_func)
    return decorated_func


class Main():

    inputFile:TextIO = SETTINGS.getInputFile()

    Output = Output()
    printTypes = Output.getOutput(SETTINGS.getOutputType())
    if len(printTypes) < 1:
        printTypes[SETTINGS.getOutputType()] = printCustom

    async def main(self):
        global BOT
        
        try:
            BOT.sessionStart()
            await BOT.setBot()
        except Exception as e:
            print(str(e))
            if "A wait of" in str(e):
                await self.switchBot()
                
        for line in self.inputFile:
            await self.processLine(line)
    
    
    async def processLine(self, line:str):
        try:
            username = line.strip()
            print(f"\nProcessing {username}")
         
            if '@' not in username:
                return
         
            USER = User(username = username)
         
            USER.setUserInfo(await BOT.getUser(USER,SETTINGS)) #so tight step bro
            USER.setUserFullInfo(await BOT.getUserFull(USER,SETTINGS)) #i want to see your big biautiful interface
         
            await asyncio.sleep(SETTINGS.getSleep())
         
            filtered_search = apply_filters(SETTINGS.getSearchStrategyList(), do_search)
            result = await filtered_search(USER,SETTINGS)

            if result is not None:

                try:
                    self.printTypes[SETTINGS.getOutputType()].doPrint(result, SETTINGS)
                    print(f"Data for {result.getUsername()} saved to {SETTINGS.getOutputFileName()}")
                except Exception as e:
                    SETTINGS.getOutputFile().write(f"Error for: {result.getUsername() or 'None'}: {str(e)} \t")
                    print(f"Error for: {result.getUsername() or 'None'}: {str(e)} \n")
                SETTINGS.getOutputFile().write('\n')

        except asyncio.TimeoutError:
            SETTINGS.getOutputFile().write(f"Timeout for {USER.getUsername()}\n")
            print(f"Timeout for {USER.getUsername()}")

        except Exception as e:
            SETTINGS.getOutputFile().write(f"Error for {USER.getUsername()}: {str(e)}\n")
            print(f"Error for {USER.getUsername()}: {str(e)}")

            if "A wait of" in str(e):
                await self.switchBot()
                await self.processLine(line)


        SETTINGS.closeOutputFile() #Если не закрыть - запись не произойдет 


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
    asyncio.run(Main().main())
