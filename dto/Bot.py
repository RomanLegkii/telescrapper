from pydantic import BaseModel
from telethon import TelegramClient
from telethon.tl.types import User as UserInfo
from telethon.tl.types import UserFull as UserFullInfo
from telethon.tl.functions.users import GetFullUserRequest
from dto.User import User
from dto.Settings import Settings
import asyncio
import os


class Bot(BaseModel):
    bot:TelegramClient|None = None
    botToken:str
    apiId:int
    apiHash:str

    class Config:
        arbitrary_types_allowed = True  # Разрешает TelegramClient

    def __init__(self, **data):
        super().__init__(**data)

    def setToken(self,token:str):
        self.botToken = token
        #check for incorrect type

    def sessionStart(self) -> TelegramClient:
        if os.path.exists('bot.session'):
            self.removeSession()
        self.bot = TelegramClient('bot', self.apiId, self.apiHash)
    
    async def setBot(self):
        await self.bot.start(bot_token = self.botToken)
    
    async def disconnectBot(self):
        await self.bot.disconnect()

    async def deleteBot(self):
        await self.bot.disconnect()
        os.remove('bot.session')
    
    def removeSession(self):
        os.remove('bot.session')
    
    async def getUser(self, User:User, Settings:Settings)-> UserInfo:
        return await asyncio.wait_for(self.bot.get_entity(User.getUsername()), timeout=Settings.getTimeout())

    async def getUserFull(self, User:User, Settings:Settings)-> UserFullInfo:
        return await asyncio.wait_for(self.bot(GetFullUserRequest(User.getUsername())), timeout=Settings.getTimeout())