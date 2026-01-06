from pyrogram import Client, filters
from pyrogram.types import *
import random, string, asyncio
from Database.filestoredb import fsdb
from vars import *

ACTIVE_STORE = {}
DELETE_TIME = 300  # 5 minutes

def gen_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@Client.on_message(filters.command("store") & filters.private & filters.user(ADMIN_ID))
async def start_store(client, message):
    store_id = gen_id()
    ACTIVE_STORE[message.from_user.id] = store_id
    await fsdb.create_store(store_id)

    await message.reply(
        "📁 **Send files now**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add More", callback_data="add_more")],
            [InlineKeyboardButton("✅ Generate Link", callback_data="gen_link"),
             InlineKeyboardButton("❌ Cancel", callback_data="cancel_store")]
        ])
    )

@Client.on_message(filters.private & filters.media)
async def save_files(client, message):
    user_id = message.from_user.id
    if user_id not in ACTIVE_STORE:
        return

    store_id = ACTIVE_STORE[user_id]
    await fsdb.add_file(store_id, message.id)

@Client.on_callback_query()
async def store_buttons(client, query):
    user_id = query.from_user.id
    if user_id not in ACTIVE_STORE:
        return

    store_id = ACTIVE_STORE[user_id]

    if query.data == "gen_link":
        link = f"https://t.me/{(await client.get_me()).username}?start=store_{store_id}"
        await query.message.edit_text(f"🔗 **Link Generated:**\n{link}")
        del ACTIVE_STORE[user_id]

    elif query.data == "cancel_store":
        await fsdb.delete_store(store_id)
        del ACTIVE_STORE[user_id]
        await query.message.edit_text("❌ **Store cancelled**")

