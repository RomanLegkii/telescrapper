from functools import wraps
from dto import User as UserClass

def check_bio(func):
    @wraps(func)
    async def wrapper(User:UserClass, *args, **kwargs):
        if User.getBio() is None:
            print(f"No bio for {User.getUsername()}")
            return
        return await func(User, *args, **kwargs)
    return wrapper