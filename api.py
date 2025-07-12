#фото хуево подгружает из-за настроек безопасности
#personal_channel vs messaging_channel
#@todo сделать декоратор фильтров, добавить туда bio
#@todo кастомный вывод 
#@todo расширить выбор данных для получения

from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from fuzzywuzzy import fuzz
import asyncio
import os
import sys
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv('vars.env')

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

def printInfo(info,full,bio,file,extra):
    keys = extra.keys()
    try:
        file.write(f"ID: {info.id}\t")
        file.write(f"Name: {info.first_name or 'None'} {info.last_name or 'None'}\t")
        file.write(f"Username: @{info.username or 'None'}\t")
        file.write(f"Bio: {bio or 'None'}\t")
        for key in keys:
            file.write(f"{key}: {extra[key]}\n")
        if keys is None:
            file.write("\n")
        print(f"Data for @{info.username or info.id} saved to {resultFile}")

    except Exception as e:
        file.write(f"Error for @{info.username or info.id}: {str(e)}\n")
        print(f"Error for @{info.username or info.id}: {str(e)}")

class Search(ABC):  #нах он нужен тут
    @abstractmethod
    async def doSearch(self, info, full, bio, file):
        pass

class FuzzySearch(Search):
    async def doSearch(self, info, full, bio, file):

        if bio is None:
            print(f"No bio for @{info.username}")
            return

        ratio = fuzz.ratio(needle.lower(), bio.lower())
        print(f"Similarity for @{info.username or info.id}: {ratio}")
        if ratio >= minimum:
            printInfo(info,full,bio,file,{'ratio':ratio})

class TextContainsSearch(Search):
    async def doSearch(self, info, full, bio, file):

        if bio is None:
            print(f"No bio for @{info.username}")
            return

        if needle.lower() in bio.lower():
            printInfo(info,full,bio,file,{'needle':needle})

class NoSearch(Search):
    async def doSearch(self, info, full, bio, file):
        printInfo(info,full,bio,file,{})

class ChannelAndPhotoSearch(Search):
    async def doSearch(self, info, full, bio, file):

        if bio is None:
            print(f"No bio for @{info.username}")
            return

        if (info.photo is not None) and (full.full_user.personal_channel_id is not None):
            printInfo(info,full,bio,file,{})

class ChannelSearch(Search):
    async def doSearch(self, info, full, bio, file):

        if bio is None:
            print(f"No bio for @{info.username}")
            return

        if full.full_user.personal_channel_id is None:
            print(f"No channel for @{info.username}")
            return
        printInfo(info,full,bio,file,{'channel_id': full.full_user.personal_channel_id})

search_strategies = {}
search_strategies['fuzzy'] = FuzzySearch()
search_strategies['contains'] = TextContainsSearch()
search_strategies['no'] = NoSearch()
search_strategies['channelAndPhoto'] = ChannelAndPhotoSearch()
search_strategies['channel'] = ChannelSearch()

search_strategy = search_strategies[str(os.getenv('SEARCH_STRATEGY'))]

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

async def processUser(id,f):
    global bot
    try:
        info = await asyncio.wait_for(bot.get_entity(id), timeout=timeout)
        full = await asyncio.wait_for(bot(GetFullUserRequest(id)), timeout=timeout)

        print(f"Waiting {sleep} seconds")
        await asyncio.sleep(sleep)
        bio = full.full_user.about

        await search_strategy.doSearch(info, full, bio, f)

    except asyncio.TimeoutError:
         f.write(f"Timeout for {id}\n")
         print(f"Timeout for {id}")

    except Exception as e:
        if "A wait of" in str(e):
            f.write(f"Error for {id}: {str(e)}\n")
            print(f"Error for {id}: {str(e)}")

            global tokenIndex, tokens, bot_token
            tokenIndex+=1

            if tokenIndex > len(tokens)-1:
                print("All bots have been used!")
                sys.exit()

            print(f"Switching to bot#{tokenIndex+1}")

            await bot.disconnect()
            os.remove('bot.session')
            bot =  TelegramClient('bot', api_id, api_hash)
            bot_token = tokens[tokenIndex]
            await bot.start(bot_token=bot_token)

            await processUser(id,f)
            return

        f.write(f"Error for {id}: {str(e)}\n")
        print(f"Error for {id}: {str(e)}")


removeSession()

bot =  TelegramClient('bot', api_id, api_hash)


async def main():
    global bot
    await bot.start(bot_token=bot_token)

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
