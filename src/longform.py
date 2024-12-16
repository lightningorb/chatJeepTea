from speak import speak
from conversation import Speaker
from think import think
import json
import logging
from utils import reply_text

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
    def chunk_text(text, max_size):
        """Split text into smaller chunks within the max_size limit."""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            if current_size + len(word) + 1 > max_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
            current_chunk.append(word)
            current_size += len(word) + 1  # Include space

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    title = convo.last_entry().text
    await convo.delete_cache()
    prompt = f"Write the outline as a json document for a book entitled: {title}. Please only respond with the json and nothing else. The json must be in the following format: \n\n{data_format}"
    convo.add_entry(prompt, Speaker.user)
    await think(convo)
    response = convo.last_entry().text
    logger.info(response)
    await reply_text(update.message, f"assistant: {response}")
    prompts = generate_prompts(json.loads(response))
    await convo.delete_cache()

    for p in prompts:
        convo.add_entry(p, Speaker.user)
        try:
            await think(convo)
        except Exception:
            logger.info("Error during thinking")

        text = convo.last_entry().text
        # Chunk the text if it exceeds the size limit (e.g., 500 characters)
        chunks = chunk_text(text, max_size=500)

        for chunk in chunks:
            fn = await speak(
                text=chunk,
                user_id=user.id,
                lang=convo.last_entry().language,
            )
            try:
                await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)
            except Exception as e:
                logger.info("Error sending voice")
                logger.info(e)

def generate_prompts(data):
    prompts = []
    author = data.get("author", "")
    author = f"in the style of {author}" if author else ""
    for c in data["chapters"]:
        for s in c["sections"]:
            prompt = f"""Write a section for a book titled: "{data['title']}" {author}, chapter: "{c['title']}", section: "{s['title']}", section content: "{s['content']}" """
            prompts.append(prompt)
    return prompts
