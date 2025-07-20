from functools import wraps
from dto.User import User as UserClass
from dto.Settings import Settings

def checkChannel(func):
    @wraps(func)
    async def wrapper(User:UserClass, Settings:Settings, *args, **kwargs):
        if User.getUserFullInfo().full_user.personal_channel_id is None:
            print(f"No channel for {User.getUsername()}")
            return
        return await func(User, Settings, *args, **kwargs)
    return wrapper