from pyrogram import Client, filters
from pyrogram.types import *
import random, string, asyncio
from Database.filestoredb import fsdb
from vars import *

ACTIVE_STORE = {}
STORE_FILES = {}   # temp storage before link generation
DELETE_TIME = 300  # 5 minutes


def gen_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


@Client.on_message(filters.command("store") & filters.private & filters.user(ADMIN_ID))
async def start_store(client, message):
    user_id = message.from_user.id

    store_id = gen_id()
    ACTIVE_STORE[user_id] = store_id
    STORE_FILES[user_id] = []

    await fsdb.create_store(store_id)

    await message.reply("📁 **Send me files**")


@Client.on_message(filters.private & filters.media)
async def save_files(client, message):
    user_id = message.from_user.id
    if user_id not in ACTIVE_STORE:
        return

    # COPY FILE TO FILESTORE DATABASE CHANNEL
    copied = await client.copy_message(
        chat_id=FILESTORE_DB_CHANNEL,
        from_chat_id=message.chat.id,
        message_id=message.id
    )

    STORE_FILES[user_id].append(copied.message_id)

    # SHOW BUTTONS AFTER FIRST FILE
    if len(STORE_FILES[user_id]) == 1:
        await message.reply(
            "✅ **File added. Choose an option:**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add More", callback_data="add_more")],
                [InlineKeyboardButton("🔗 Generate Link", callback_data="gen_link"),
                 InlineKeyboardButton("❌ Cancel", callback_data="cancel_store")]
            ])
        )


@Client.on_callback_query()
async def store_buttons(client, query):
    user_id = query.from_user.id

    if user_id not in ACTIVE_STORE:
        await query.answer("No active store", show_alert=True)
        return

    store_id = ACTIVE_STORE[user_id]

    if query.data == "add_more":
        await query.message.edit_text("📁 **Send more files**")
        return

    elif query.data == "cancel_store":
        await fsdb.delete_store(store_id)
        ACTIVE_STORE.pop(user_id)
        STORE_FILES.pop(user_id)
        await query.message.edit_text("❌ **Store cancelled**")
        return

    elif query.data == "gen_link":
        files = STORE_FILES.get(user_id, [])
        if not files:
            await query.answer("No files added", show_alert=True)
            return

        # SAVE FILE IDS TO DATABASE
        for msg_id in files:
            await fsdb.add_file(store_id, msg_id)

        bot = await client.get_me()
        link = f"https://t.me/{bot.username}?start=store_{store_id}"

        await query.message.edit_text(
            f"🔗 **Link Generated:**\n\n{link}"
        )

        ACTIVE_STORE.pop(user_id)
        STORE_FILES.pop(user_id)
