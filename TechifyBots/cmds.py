from pyrogram import Client, filters
from pyrogram.types import *
from vars import *
from Database.maindb import mdb
from Database.userdb import udb
from Database.filestoredb import fsdb
import random, asyncio
from .fsub import get_fsub
from Script import text

# Reply Keyboard
getvideos_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("🎬 Get Videos")]],
    resize_keyboard=True
)

DELETE_TIME = 300  # 5 minutes


async def get_updated_limits():
    global FREE_LIMIT, PRIME_LIMIT
    limits = await mdb.get_global_limits()
    FREE_LIMIT = limits["free_limit"]
    PRIME_LIMIT = limits["prime_limit"]
    return limits


@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):

    # ───── FILE STORE LINK HANDLER ─────
    if len(message.command) > 1 and message.command[1].startswith("store_"):
        store_id = message.command[1][6:]
        files = await fsdb.get_files(store_id)

        if not files:
            await message.reply_text("❌ Invalid or expired link")
            return

        sent = []
        for msg_id in files:
            m = await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=DATABASE_CHANNEL_ID,
                message_id=msg_id,
                protect_content=True
            )
            sent.append(m.id)

        await message.reply_text("⚠️ Files will be deleted after 5 minutes")

        await asyncio.sleep(DELETE_TIME)
        await client.delete_messages(message.chat.id, sent)
        return
    # ─────────────────────────────────

    # Ban check
    if await udb.is_user_banned(message.from_user.id):
        await message.reply(
            "**🚫 You are banned from using this bot**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Support 🧑‍💻", url=f"https://t.me/{ADMIN_USERNAME}")]]
            )
        )
        return

    if IS_FSUB and not await get_fsub(client, message):
        return

    if await udb.get_user(message.from_user.id) is None:
        await udb.addUser(message.from_user.id, message.from_user.first_name)

    await message.reply_photo(
        photo=random.choice(PICS),
        caption=text.START.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🍿 Buy Subscription", callback_data="pro")],
            [InlineKeyboardButton("ℹ️ About", callback_data="about"),
             InlineKeyboardButton("📚 Help", callback_data="help")]
        ])
    )

    await message.reply_text(
        "👇 Use the button below to get videos",
        reply_markup=getvideos_keyboard
    )


@Client.on_message(
    (filters.command("getvideos") |
     (filters.text & filters.regex("^🎬 Get Videos$")))
    & filters.private
)
async def send_random_video(client, message):

    if await udb.is_user_banned(message.from_user.id):
        return

    limits = await get_updated_limits()
    if limits.get("maintenance"):
        await message.reply_text("🛠️ Bot under maintenance")
        return

    if IS_FSUB and not await get_fsub(client, message):
        return

    user = await mdb.get_user(message.from_user.id)
    plan = user.get("plan", "free")

    videos = await mdb.get_all_videos() if plan == "prime" else await mdb.get_free_videos()
    if not videos:
        await message.reply_text("No videos available")
        return

    video = random.choice(videos)

    m = await client.copy_message(
        chat_id=message.chat.id,
        from_chat_id=DATABASE_CHANNEL_ID,
        message_id=video["video_id"]
    )

    await mdb.increment_daily_count(message.from_user.id)
    await asyncio.sleep(300)
    await m.delete()
