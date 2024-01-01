from bot.myDb import myDb
from bot.url import short_me
from bot.config import Config
from bot.Db import *

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client

def access(func):
    async def wrapper(client: Client, msg: Message):
        try:
            if msg.from_user.id in Config.AUTH_USERS:
                print("IS ADMIN")
                return await func(client, msg)

            token_live = myDb.check_access(msg.from_user.id)

            if not token_live:
                token = myDb.gen_token(msg.from_user.id)
                bot_ = await TGBot.get_me()
                btn = [[InlineKeyboardButton("Gen Token", url=short_me(f"https://telegram.me/{bot_.username}?start={token}"))]]
                await msg.reply(
                    text=f"You need to generate Token to use me {msg.from_user.mention}.\n\n",
                    reply_markup=InlineKeyboardMarkup(btn),
                )
                myDb.client.set(f"acc^{msg.from_user.id}", 0)
                return

        except Exception as e:
            logger.error(f"Error in access function: {e}")

    return wrapper
