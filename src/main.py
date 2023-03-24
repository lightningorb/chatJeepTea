import asyncio
import os
import tempfile

import aiofiles
import aiohttp
from telegram import __version__ as TG_VER, Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.ext import CallbackQueryHandler

import conf
import keys
from intl import longform_info_text
from longform import generate_longform
from menus import main_menu_keyboard
from speak import speak
from conversation import Speaker, Conversation
from think import think
from whisper import whisper
from auth import check_is_authorized
from utils import reply_text

keys.set_up_keys()

convos = {}


async def download_file(file_path: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(file_path) as response:
            content = await response.read()
    return content


async def run_ffmpeg(file_name: str, temp_file_name: str) -> None:
    cmd = f"ffmpeg -i {file_name} -vn -ar 44100 -ac 2 -ab 192k -f mp3 {temp_file_name}"
    process = await asyncio.create_subprocess_shell(cmd)
    await process.communicate()


async def intro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    msg = "Hello and welcome to Chat Jeep Tea. To speak to me, record and send a voice message by doing a long press on the microphone icon at the bottom right of telegram. I will respond to your message. To bring up the help menu at any time, type /help. Please bear in mind I keep a certain (somewhat small) amount of the conversation history as context. This helps us have a more natural conversation. Go ahead, ask me anything."

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"assistant: {msg}"
    )

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    user = update.effective_user

    fn = await speak(msg, user.id, "en-US")
    await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)


async def new_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in convos:
        convos[user.id] = await Conversation.create(user.id)
    convo = convos.get(user.id)
    await convo.delete_cache()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Conversation cleared"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(rf"Hi {user.mention_html()}!")
    await update.message.reply_text("Help Menu:", reply_markup=main_menu_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help menu:", reply_markup=main_menu_keyboard())


async def longform_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=longform_info_text
    )


async def longform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please provide the title of the book / podcast / longform article you want to generate",
    )


async def write_file(file_name: str, content: bytes) -> None:
    async with aiofiles.open(file_name, "wb") as f:
        await f.write(content)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if not await check_is_authorized(str(user.id)):
        await update.message.reply_text(f"You're not authorized to use this app. Please ask the admin to authorize: {user.id}")
        return

    voice = update.message.voice

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    if user.id not in convos:
        convos[user.id] = await Conversation.create(user.id)

    convo = convos[user.id]

    if voice:
        file_name = f"/tmp/{voice.file_id}.ogg"
        file_path = (await context.bot.get_file(voice.file_id)).file_path
        response = await download_file(file_path)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_name = f"{temp_file.name}.mp3"
        temp_file.close()
        await write_file(file_name, response)
        await run_ffmpeg(file_name, temp_file_name)
        t = await whisper(temp_file_name)
        convo.add_entry(t, Speaker.user)
        await reply_text(update.message, f"user: {t}")
    else:
        convo.add_entry(update.message.text, Speaker.user)

    if (
        update.message.reply_to_message
        and update.message.reply_to_message.text == longform_info_text
    ):
        await generate_longform(convo, user, context, update)
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    await think(convo)
    await reply_text(update.message, f"assistant: {convo.last_entry().text}")
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    fn = await speak(
        text=convo.last_entry().text, user_id=user.id, lang=convo.last_entry().language
    )
    await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)


def main() -> None:
    TG_VER_INFO = (0, 0, 0, 0, 0)
    try:
        from telegram import __version_info__

        TG_VER_INFO = __version_info__
    except ImportError:
        pass
    if TG_VER_INFO < (20, 0, 0, "alpha", 1):
        raise RuntimeError(
            f"This example is not compatible with your current PTB version {TG_VER}."
        )
    application = Application.builder().token(os.environ["TOKEN"]).build()
    application.add_handler(
        CallbackQueryHandler(new_conversation, pattern="new_conversation")
    )
    application.add_handler(CallbackQueryHandler(intro, pattern="intro"))
    application.add_handler(
        CallbackQueryHandler(longform_info, pattern="longform_info")
    )
    application.add_handler(CallbackQueryHandler(longform, pattern="longform"))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler((filters.TEXT | filters.ATTACHMENT) & ~filters.COMMAND, chat)
    )
    application.run_polling()


if __name__ == "__main__":
    main()
