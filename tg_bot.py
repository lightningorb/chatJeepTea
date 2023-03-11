import keys
import tempfile
import os
import requests
from telegram import __version__ as TG_VER, ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import sys
from utils import think, speak, Entry, Speaker, Conversation
from record import record
from whisper import whisper

keys.set_up_keys()

convos = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!", reply_markup=ForceReply(selective=True)
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    voice = update.message.voice
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
        think(convo)
        fn = speak(convo.last_entry(), use_google=True, save_only=True)
        await update.message.reply_html(
            convo.last_entry(), reply_markup=ForceReply(selective=True)
        )
        await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)
    else:
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!", reply_markup=ForceReply(selective=True)
        )


def main() -> None:
    application = Application.builder().token(os.environ["TOKEN"]).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler((filters.TEXT | filters.ATTACHMENT) & ~filters.COMMAND, echo)
    )
    application.run_polling()


if __name__ == "__main__":
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
    main()
