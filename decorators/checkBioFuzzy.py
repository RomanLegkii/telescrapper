
from functools import wraps
from dto import User as UserClass
from dto import User as UserClass
from dto import Settings
from fuzzywuzzy import fuzz

def checkBioFuzzy(func):
    @wraps(func)
    async def wrapper(User:UserClass, Settings:Settings, *args, **kwargs):
        if User.getBio() is None:
             print(f"No bio for @{User.getUsername()}")
             return
        ratio = fuzz.ratio(Settings.getNeedle().lower(), User.getBio().lower())
        print(f"Similarity for {User.getUsername()}: {ratio}")
        if ratio < Settings.getMinimum():
            return
        return await func(User, Settings, *args, **kwargs)
    return wrapper