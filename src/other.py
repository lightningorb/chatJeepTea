from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

# from tg_bot import convos
from utils import Conversation, Speaker, think
from speak import speak


async def HN(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from random import randrange
    import requests
    from readabilipy import simple_json_from_html_string

    user = update.effective_user

    if user.id not in convos:
        convos[user.id] = Conversation(user.id)

    convo = convos[user.id]
    convo.delete_cache()

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    response = requests.get(
        f"https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    )
    article_id = response.json()[randrange(0, 100)]
    article_api_link = (
        f"https://hacker-news.firebaseio.com/v0/item/{article_id}.json?print=pretty"
    )
    response = requests.get(article_api_link)

    article_html = requests.get(response.json()["url"], timeout=10).text
    article = simple_json_from_html_string(article_html, use_readability=True)
    plain_text = " ".join(x["text"] for x in article["plain_text"])

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    convo.add_entry(f"summarize the following:\n\n{plain_text}", Speaker.user)
    think(convo)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=convo.last_entry()
    )
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    fn = speak(convo.last_entry(), use_google=True, save_only=True)
    await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)
