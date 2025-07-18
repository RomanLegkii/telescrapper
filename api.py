#@todo кастомный вывод 
#@todo расширить выбор данных для получения

from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from fuzzywuzzy import fuzz
from functools import wraps
import asyncio
import os
import sys
from dotenv import load_dotenv
from abc import ABC, abstractmethod

isLoaded = load_dotenv('vars.env')
if isLoaded is False:
    print('.env file not found')
    sys.exit()


api_id = int(os.getenv('API_ID'))
api_hash = str(os.getenv('API_HASH'))
tokens = os.getenv('BOT_TOKENS').split(',')
tokenIndex = 0
bot_token = tokens[tokenIndex]

fileName = str(os.getenv('SRC_FILENAME'))
resultFile = str(os.getenv('RESULT_FILENAME'))
needle = str(os.getenv('NEEDLE'))
minimum = int(os.getenv('RATIO'))
timeout = int(os.getenv('TIMEOUT_LIMIT'))
sleep = int(os.getenv('SLEEP_TIME'))
outputType = os.getenv('OUTPUT_TYPE') #legacy -> could be empty
if outputType is not None and ',' in outputType:
    outputType = outputType.split(',')
selectedStrategies = os.getenv('SEARCH_STRATEGY')
if selectedStrategies != '':
    selectedStrategies = selectedStrategies.split(',')



#null variable check
localsCopy = list(locals().keys())
hardcodedLocals = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', 
                   '__file__', '__cached__', '__builtins__', 'TelegramClient', 'GetFullUserRequest', 'fuzz',
                    'wraps', 'asyncio', 'os', 'sys', 'load_dotenv', 'ABC', 'abstractmethod', 'localVars','outputType']
settings = {}
errorVars = []
for local in localsCopy:
    if local not in hardcodedLocals:
        settings[local] = locals()[local]

for key,setting in settings.items():
    if setting is None or (isinstance(setting, (str, list)) and len(setting) == 0):
        print(f"Key: {key}, Value: {setting}")
        errorVars.append(key)

if len(errorVars) > 0:
    print(f"Following variables can't be null {errorVars}")
    sys.exit()


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


def printInfo(info,full,bio,file):#переделать бы
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

# Декораторы для проверок
def check_bio(func):
    @wraps(func)
    async def wrapper(info, full, bio, file, *args, **kwargs):
        if bio is None:
            print(f"No bio for @{info.username}")
            return
        return await func(info, full, bio, file, *args, **kwargs)
    return wrapper

def check_channel(func):
    @wraps(func)
    async def wrapper(info, full, bio, file, *args, **kwargs):
        if full.full_user.personal_channel_id is None:
            print(f"No channel for @{info.username}")
            return
        return await func(info, full, bio, file, *args, **kwargs)
    return wrapper

def check_photo(func):
    @wraps(func)
    async def wrapper(info, full, bio, file, *args, **kwargs):
        if info.photo is None:
            print(f"No photo for @{info.username}")
            return
        return await func(info, full, bio, file, *args, **kwargs)
    return wrapper

def check_bio_contains(func):
    @wraps(func)
    async def wrapper(info, full, bio, file, *args, **kwargs):
        if bio is None or needle.lower() not in bio.lower():
            print(f"Needle or bio wasn't found for @{info.username}")
            return
        return await func(info, full, bio, file, *args, **kwargs)
    return wrapper

def check_bio_fuzzy(func):
    @wraps(func)
    async def wrapper(info, full, bio, file, *args, **kwargs):
        if bio is None:
             print(f"No bio for @{info.username}")
             return
        ratio = fuzz.ratio(needle.lower(), bio.lower())
        print(f"Similarity for @{info.username}: {ratio}")
        if ratio < minimum:
            return
        return await func(info, full, bio, file, *args, **kwargs)
    return wrapper

# Базовая функция поиска
async def do_search(info, full, bio, file):
    print(f"Found match @{info.username}")
    return {"username": info.username, "bio": bio, "full":full, "info":info, "file":file}

# Функция для компоновки декораторов
def apply_filters(filters, base_func):

    decorators = [filter_decorators[f] for f in filters if f in filter_decorators]
    decorated_func = base_func
    for decorator in reversed(decorators):
        decorated_func = decorator(decorated_func)
    return decorated_func

# Регистрация декораторов
filter_decorators = {
    "bio": check_bio,
    "channel": check_channel,
    "photo": check_photo,
    "bio_contains": check_bio_contains,
    "bio_fuzzy": check_bio_fuzzy,
}

def removeSession(path='.'):
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name == 'bot.session':
                    print('Removing bot.session')
                    os.remove('bot.session')
                    return

    except FileNotFoundError:
        print(f"Directory {path} not found")
    except PermissionError:
        print(f"Permission denied for directory {path}")
    except Exception as e:
        print(f"Error scanning directory {path}: {str(e)}")

async def switchBot():
    global tokenIndex, bot, bot_token, tokens
    try:
        tokenIndex += 1

        if tokenIndex > len(tokens)-1:
            print("All bots have been used!")
            sys.exit()

        print(f"Switching to bot#{tokenIndex+1}")
     
        await bot.disconnect()
        os.remove('bot.session')
        bot =  TelegramClient('bot', api_id, api_hash)
        bot_token = tokens[tokenIndex]
        await bot.start(bot_token=bot_token)
    except Exception as e:
        print(str(e))
        if "A wait of" in str(e):
            await switchBot()



async def processUser(id,f):
    global bot
    try:
        info = await asyncio.wait_for(bot.get_entity(id), timeout=timeout)
        full = await asyncio.wait_for(bot(GetFullUserRequest(id)), timeout=timeout)

        print(f"Waiting {sleep} seconds")
        await asyncio.sleep(sleep)
        bio = full.full_user.about

        filtered_search = apply_filters(selectedStrategies, do_search)
        result = await filtered_search(info, full, bio, f)
        if result is None:
            return
        printInfo(result['info'],result['full'], result['bio'], f)

    except asyncio.TimeoutError:
        f.write(f"Timeout for {id}\n")
        print(f"Timeout for {id}")

    except Exception as e:
        if "A wait of" in str(e):
            f.write(f"Error for {id}: {str(e)}\n")
            print(f"Error for {id}: {str(e)}")

            switchBot()

            await processUser(id,f)
            return

        f.write(f"Error for {id}: {str(e)}\n")
        print(f"Error for {id}: {str(e)}")


removeSession()

bot =  TelegramClient('bot', api_id, api_hash)


async def main():
    global bot

    foundWorkingBot = False
    while(foundWorkingBot == False):
        try:
            await bot.start(bot_token=bot_token)
        except Exception as e:
            print(str(e))
            if "A wait of" in str(e):
                await switchBot()
        finally:
            foundWorkingBot = True
            

    with open(fileName, 'r', encoding='utf-8') as r:
        for line in r:

            id = line.strip()
            print(f"Processing {id}")

            if '@' not in id:
                continue

            with open(resultFile, 'a', encoding='utf-8') as f:
                await processUser(id,f)

if __name__ == '__main__':
    asyncio.run(main())
