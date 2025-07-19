from functools import wraps
from dto import User as UserClass
from dto import Settings

def checkBioContains(func):
    @wraps(func)
    async def wrapper(User:UserClass, Settings:Settings, *args, **kwargs):
        if User.getBio() is None or Settings.getNeedle().lower() not in Settings.getBio().lower():
            print(f"Needle or bio wasn't found for {Settings.getUsername()}")
            return
        return await func(User, Settings, *args, **kwargs)
    return wrapper