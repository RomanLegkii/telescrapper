from functools import wraps
from dto.User import User as UserClass
from dto.Settings import Settings

def checkBio(func):
    @wraps(func)
    async def wrapper(User:UserClass, Settings:Settings, *args, **kwargs):
        if User.getBio() is None:
            print(f"No bio for {User.getUsername()}")
            return
        return await func(User, Settings, *args, **kwargs)
    return wrapper