import os
import tempfile
import asyncio

import conf
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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

import keys
from intl import longform_info_text
from utils import think, Speaker, Conversation
from speak import speak
from whisper import whisper

keys.set_up_keys()

convos = {}


async def run_ffmpeg(file_name: str, temp_file_name: str) -> None:
    cmd = f"ffmpeg -i {file_name} -vn -ar 44100 -ac 2 -ab 192k -f mp3 {temp_file_name}"
    process = await asyncio.create_subprocess_shell(cmd)
    await process.communicate()


async def intro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async def typing():
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )

    await typing()

    msg = "Hello and welcome to Chat Jeep Tea. To speak to me, record and send a voice message by doing a long press on the microphone icon at the bottom right of telegram. I will respond to your message. To bring up the help menu at any time, type /help. Please bear in mind I keep a certain (somewhat small) amount of the conversation history as context. This helps us have a more natural conversation. Go ahead, ask me anything."

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"assistant: {msg}"
    )

    await typing()

    fn = await speak(
        msg,
        use_google=True,
        save_only=True,
    )
    await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)


async def new_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    convo = convos.get(user.id)
    if convo:
        convo.delete_cache()
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
    print("longform_info")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=longform_info_text
    )


async def longform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("longform")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please provide the title of the book / podcast / longform article you want to generate",
    )


def main_menu_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "New Conversation", callback_data="new_conversation"
                ),
                InlineKeyboardButton("What is this?", callback_data="intro"),
                InlineKeyboardButton("Set Language", callback_data="lang_menu"),
            ],
            [
                InlineKeyboardButton("Longform", callback_data="longform_info"),
            ],
        ]
    )


async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    match = context.match.string[len("lang: ") :]
    conf.set_language(user.id, match)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Language: {match} set."
    )


async def lang_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Languages",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Afrikaans (South Africa)", callback_data="lang: af-ZA"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Arabic (Saudi Arabia)", callback_data="lang: ar-XA"
                    )
                ],
                [InlineKeyboardButton("Bengali (India)", callback_data="lang: bn-IN")],
                [
                    InlineKeyboardButton(
                        "Bulgarian (Bulgaria)", callback_data="lang: bg-BG"
                    )
                ],
                [InlineKeyboardButton("Catalan (Spain)", callback_data="lang: ca-ES")],
                [
                    InlineKeyboardButton(
                        "Chinese (Mandarin, China)", callback_data="lang: cmn-CN"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Chinese (Mandarin, Taiwan)", callback_data="lang: cmn-TW"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Czech (Czech Republic)", callback_data="lang: cs-CZ"
                    )
                ],
                [InlineKeyboardButton("Danish (Denmark)", callback_data="lang: da-DK")],
                [InlineKeyboardButton("Dutch (Belgium)", callback_data="lang: nl-BE")],
                [
                    InlineKeyboardButton(
                        "Dutch (Netherlands)", callback_data="lang: nl-NL"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "English (Australia)", callback_data="lang: en-AU"
                    )
                ],
                [InlineKeyboardButton("English (India)", callback_data="lang: en-IN")],
                [
                    InlineKeyboardButton(
                        "English (United Kingdom)", callback_data="lang: en-GB"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "English (United States)", callback_data="lang: en-US"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Filipino (Philippines)", callback_data="lang: fil-PH"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Finnish (Finland)", callback_data="lang: fi-FI"
                    )
                ],
                [InlineKeyboardButton("French (Canada)", callback_data="lang: fr-CA")],
                [InlineKeyboardButton("French (France)", callback_data="lang: fr-FR")],
                [InlineKeyboardButton("Greek (Greece)", callback_data="lang: el-GR")],
                [InlineKeyboardButton("Gujarati (India)", callback_data="lang: gu-IN")],
                [InlineKeyboardButton("Hebrew (Israel)", callback_data="lang: he-IL")],
                [InlineKeyboardButton("Hindi (India)", callback_data="lang: hi-IN")],
                [
                    InlineKeyboardButton(
                        "Hungarian (Hungary)", callback_data="lang: hu-HU"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Icelandic (Iceland)", callback_data="lang: is-IS"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Indonesian (Indonesia)", callback_data="lang: id-ID"
                    )
                ],
                [InlineKeyboardButton("Italian (Italy)", callback_data="lang: it-IT")],
                [InlineKeyboardButton("Japanese (Japan)", callback_data="lang: ja-JP")],
                [InlineKeyboardButton("Kannada (India)", callback_data="lang: kn-IN")],
                [
                    InlineKeyboardButton(
                        "Korean (South Korea)", callback_data="lang: ko-KR"
                    )
                ],
                [InlineKeyboardButton("Latvian (Latvia)", callback_data="lang: lv-LV")],
                [
                    InlineKeyboardButton(
                        "Lithuanian (Lithuania)", callback_data="lang: lt-LT"
                    )
                ],
                [InlineKeyboardButton("Malay (Malaysia)", callback_data="lang: ms-MY")],
                [
                    InlineKeyboardButton(
                        "Malayalam (India)", callback_data="lang: ml-IN"
                    )
                ],
                [InlineKeyboardButton("Marathi (India)", callback_data="lang: mr-IN")],
                [
                    InlineKeyboardButton(
                        "Norwegian Bokmål (Norway)", callback_data="lang: nb-NO"
                    )
                ],
                [InlineKeyboardButton("Polish (Poland)", callback_data="lang: pl-PL")],
                [
                    InlineKeyboardButton(
                        "Portuguese (Brazil)", callback_data="lang: pt-BR"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Portuguese (Portugal)", callback_data="lang: pt-PT"
                    )
                ],
                [InlineKeyboardButton("Punjabi (India)", callback_data="lang: pa-IN")],
                [
                    InlineKeyboardButton(
                        "Romanian (Romania)", callback_data="lang: ro-RO"
                    )
                ],
                [InlineKeyboardButton("Russian", callback_data="lang: ru-RU")],
                [InlineKeyboardButton("Serbian (Serbia)", callback_data="lang: sr-RS")],
                [InlineKeyboardButton("Spanish (Spain)", callback_data="lang: es-ES")],
                [
                    InlineKeyboardButton(
                        "Spanish (United States)", callback_data="lang: es-US"
                    )
                ],
                [InlineKeyboardButton("Swedish (Sweden)", callback_data="lang: sv-SE")],
                [InlineKeyboardButton("Tamil (India)", callback_data="lang: ta-IN")],
                [InlineKeyboardButton("Telugu (India)", callback_data="lang: te-IN")],
                [InlineKeyboardButton("Thai (Thailand)", callback_data="lang: th-TH")],
                [InlineKeyboardButton("Turkish (Turkey)", callback_data="lang: tr-TR")],
                [
                    InlineKeyboardButton(
                        "Ukrainian (Ukraine)", callback_data="lang: uk-UA"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Vietnamese (Vietnam)", callback_data="lang: vi-VN"
                    )
                ],
            ]
        ),
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    voice = update.message.voice

    async def typing():
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )

    await typing()
    if user.id not in convos:
        convos[user.id] = Conversation(user.id)

    convo = convos[user.id]

    if voice:
        file_name = f"/tmp/{voice.file_id}.ogg"
        file_info = await context.bot.get_file(voice.file_id)
        file_path = file_info.file_path
        response = requests.get(file_path)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_name = f"{temp_file.name}.mp3"
        temp_file.close()
        with open(file_name, "wb") as f:
            f.write(response.content)
        await run_ffmpeg(file_name, temp_file_name)
        t = await whisper(temp_file_name)
        await convo.add_entry(t, Speaker.user)
        await update.message.reply_text(f"user: {t}")
    else:
        await convo.add_entry(update.message.text, Speaker.user)

    if (
        update.message.reply_to_message
        and update.message.reply_to_message.text == longform_info_text
    ):
        from longform import generate_longform

        await generate_longform(convo, user, context, update)
        return

    await typing()
    await think(convo)
    await update.message.reply_text(f"assistant: {await convo.last_entry()}")
    await typing()
    fn = await speak(
        text=await convo.last_entry(), user_id=user.id, use_google=True, save_only=True
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
    application.add_handler(CallbackQueryHandler(lang_menu, pattern="lang_menu"))
    application.add_handler(CallbackQueryHandler(set_lang, pattern="lang: (.*)"))
    application.add_handler(
        CallbackQueryHandler(longform_info, pattern="longform_info")
    )
    application.add_handler(CallbackQueryHandler(longform, pattern="longform"))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler((filters.TEXT | filters.ATTACHMENT) & ~filters.COMMAND, echo)
    )
    application.run_polling()
