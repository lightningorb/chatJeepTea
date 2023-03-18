from speak import speak
from conversation import Speaker
from think import think
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_format = json.dumps(
    {
        "title": "TITLE",
        "author": "AUTHOR",
        "chapters": [
            {
                "title": "CHAPTER TITLE",
                "sections": [
                    {
                        "title": "SECTION NAME",
                        "content": "SECTION CONTENT",
                    }
                ],
            }
        ],
    }
)


async def generate_longform(convo, user, context, update):
    title = convo.last_entry()
    await convo.delete_cache()
    prompt = f"Write the outline as a json document for a book entitled: {title}. Please only respond with the json and nothing else. The json must be in the following format: \n\n{data_format}"
    convo.add_entry(prompt, Speaker.user)
    await think(convo)
    response = convo.last_entry()
    logger.info(response)
    await update.message.reply_text(f"assistant: {response}")
    prompts = generate_prompts(json.loads(response))
    await convo.delete_cache()
    for p in prompts:
        convo.add_entry(p, Speaker.user)
        try:
            await think(convo)
        except:
            logger.info("error thinking")
        fn = await speak(text=convo.last_entry(), user_id=user.id)
        try:
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)
        except:
            logger.info("error sending voice")


def generate_prompts(data):
    prompts = []
    author = data.get("author", "")
    author = f"in the style of {author}" if author else ""
    for c in data["chapters"]:
        for s in c["sections"]:
            prompt = f"""Write a section for a book titled: "{data['title']}" {author}, chapter: "{c['title']}", section: "{s['title']}", section content: "{s['content']}" """
            prompts.append(prompt)
    return prompts
