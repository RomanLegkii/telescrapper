from functools import wraps
from dto import User as UserClass
from dto import Settings

def checkPhoto(func):
    @wraps(func)
    async def wrapper(User:UserClass, Settings:Settings, *args, **kwargs):
        if User.getUserInfo().photo is None:
            print(f"No photo for {User.getUsername()}")
            return
        return await func(User, Settings, *args, **kwargs)
    return wrapper