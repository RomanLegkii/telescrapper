from pydantic import BaseModel
from telethon.tl.types import User as UserInfo
from telethon.tl.types import UserFull as UserFullInfo

class User(BaseModel):
    username:str
    bio:str = ''
    info:UserInfo|None = None
    full:UserFullInfo|None = None

    class Config:
        arbitrary_types_allowed = True  # Разрешает UserInfo

    def __init__(self,**data):
        super().__init__(**data)

    def getUsername(self):
        return self.username
    
    def getBio(self):
        return self.bio
    
    def getUserInfo(self):
        return self.info
    
    def getUserFullInfo(self):
        return self.full

    def setUserInfo(self, UserInfo:UserInfo):
        self.info = UserInfo

    def setUserFullInfo(self, UserFullInfo:UserFullInfo):
        self.full = UserFullInfo
        self.bio = self.full.full_user.about

    def stringify(self):
        return (f"Username: {self.username} info: {self.info} full:{self.full} \n")
