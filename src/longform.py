from speak import speak
from utils import think, Speaker, Conversation, Entry
import json

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
    title = await convo.last_entry()
    await convo.delete_cache()
    prompt = f"Write the outline as a json document for a book entitled: {title}. Please only respond with the json and nothing else. The json must be in the following format: \n\n{data_format}"
    await convo.add_entry(prompt, Speaker.user)
    await think(convo)
    response = await convo.last_entry()
    print(response)
    await update.message.reply_text(f"assistant: {response}")
    prompts = generate_prompts(json.loads(response))
    await convo.delete_cache()
    for p in prompts:
        await convo.add_entry(p, Speaker.user)
        try:
            await think(convo)
        except:
            print("error thinking")
        fn = await speak(
            text=await convo.last_entry(),
            user_id=user.id,
            use_google=True,
            save_only=True,
        )
        try:
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)
        except:
            print("error sending voice")


def generate_prompts(data):
    prompts = []
    author = data.get("author", "")
    author = f"in the style of {author}" if author else ""
    for c in data["chapters"]:
        for s in c["sections"]:
            prompt = f"""Write a section for a book titled: "{data['title']}" {author}, chapter: "{c['title']}", section: "{s['title']}", section content: "{s['content']}" """
            prompts.append(prompt)
    return prompts
