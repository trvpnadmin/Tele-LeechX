import asyncio

from tobrot import FSUB_CHANNEL, LOGGER, bot
from pyrogram import enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def get_invite_link(client, chat_id):
    try:
        invite_link = bot.create_chat_invite_link(chat_id=chat_id)
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
        if user.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.MEMBER]:
            try:
                invite_link = await get_invite_link(client, chat_id=channel_chat_id)
            except Exception as err:
                LOGGER.info(f"Unable to Generate Invite Link of {FSUB_CHANNEL}\n\nError: {err}")
                return 200
            bot.send_message(
                chat_id=cmd.chat.id,
                text="<b>Dear,\nYou haven't joined our Channel yet.\nJoin to <u>Use Bots Without Restrictions.</u></b>",
                parse_mode = enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🤖 Join Channel", url=invite_link.invite_link)]
                    ])
            )
            return 400
    except Exception as err:
        LOGGER.info(f"Force Subscribe Error: {err}")
        return 200
    return 200
