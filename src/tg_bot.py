import keys
import tempfile
import os
import requests
from telegram import __version__ as TG_VER, ForceReply, Update
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from textwrap import dedent

from utils import think, speak, Entry, Speaker, Conversation
from record import record
from whisper import whisper

keys.set_up_keys()

convos = {}


async def intro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    async def typing():
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )

    await typing()

    msg = "Hello and welcome to Chat Jeep Tea. To speak to me, record and send a voice message by doing a long press on the microphone icon at the bottom right of telegram. I will respond to your message. To bring up the help menu at any time, type /help. Please bear in mind I keep a certain (somewhat small) amount of the conversation history as context. This helps us have a more natural conversation. If you want to start a new conversation simply press the 'new conversation' button in the help menu. However this is usually not required as i deal well with context switching. Go ahead, ask me anything."

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"assistant: {msg}"
    )

    await typing()

    fn = speak(
        msg,
        use_google=True,
        save_only=True,
    )
    await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)


async def new_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Done")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(rf"Hi {user.mention_html()}!")
    await update.message.reply_text("Help Menu:", reply_markup=main_menu_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help menu:", reply_markup=main_menu_keyboard())


def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("New Conversation", callback_data="new_conversation"),
            InlineKeyboardButton("What is this?", callback_data="intro"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    voice = update.message.voice

    async def typing():
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )

    await typing()

    if voice:
        if user.id not in convos:
            convos[user.id] = Conversation(user.id)
        convo = convos[user.id]
        file_name = f"/tmp/{voice.file_id}.ogg"
        file_info = await context.bot.get_file(voice.file_id)
        file_path = file_info.file_path
        response = requests.get(file_path)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_name = f"{temp_file.name}.mp3"
        temp_file.close()
        with open(file_name, "wb") as f:
            f.write(response.content)
        os.system(
            f"ffmpeg -i {file_name} -vn -ar 44100 -ac 2 -ab 192k -f mp3 {temp_file_name}"
        )
        t = whisper(temp_file_name)
        convo.add_entry(t, Speaker.user)
        await update.message.reply_text(f"user: {t}")
        await typing()
        think(convo)
        await update.message.reply_text(f"assistant: {convo.last_entry()}")
        await typing()
        fn = speak(convo.last_entry(), use_google=True, save_only=True)
        await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)
    else:
        await update.message.reply_text(rf"Hi {user.mention_html()}!")


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
    # application.add_handler(CallbackQueryHandler(main_menu, pattern="main"))
    application.add_handler(
        CallbackQueryHandler(new_conversation, pattern="new_conversation")
    )
    application.add_handler(CallbackQueryHandler(intro, pattern="intro"))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler((filters.TEXT | filters.ATTACHMENT) & ~filters.COMMAND, echo)
    )
    application.run_polling()
