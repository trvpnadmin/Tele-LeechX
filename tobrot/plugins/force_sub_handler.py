import asyncio

from tobrot import FSUB_CHANNEL, LOGGER, bot
from pyrogram import enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def get_invite_link(client, chat_id):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        LOGGER.info(f"FloodWait : Sleeping {e.value}s")
        await asyncio.sleep(e.value)
        return await get_invite_link(client, chat_id)


async def handle_force_sub(client, cmd: Message):
    if FSUB_CHANNEL and FSUB_CHANNEL.startswith("-100"):
        channel_chat_id = int(FSUB_CHANNEL)
    elif FSUB_CHANNEL and (not FSUB_CHANNEL.startswith("-100")):
        channel_chat_id = FSUB_CHANNEL
    else:
        return 200
    try:
        user = bot.get_chat_member(chat_id=channel_chat_id, user_id=cmd.from_user.id)
        if user.status == "kicked":
            await bot.reply_text(
                text="**Sorry, You are Banned to Use me.**",
                disable_web_page_preview=True
            )
            return 400
    except UserNotParticipant:
        try:
            invite_link = await get_invite_link(bot, chat_id=channel_chat_id)
        except Exception as err:
            print(f"Unable to do Force Subscribe to {FSUB_CHANNEL}\n\nError: {err}")
            return 200
        await bot.send_message(
            chat_id=cmd.chat.id,
            text="**Please Join Updates Channel to use this Bot!**\n\n"
                 "Due to Overload, Only Channel Subscribers can Use the Bot!",
            reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)]
                ])
        )
        return 400
    except Exception as err:
        LOGGER.info(f"Force Subscribe Error: {error}")
        return 200
    return 200
