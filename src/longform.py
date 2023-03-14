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
                        "title": "SECION NAME",
                        "content": "SECTION CONTENT",
                    }
                ],
            }
        ],
    }
)


async def generate_longform(convo, user, context, update):
    print("Generating longform!")
    title = convo.last_entry()
    convo.delete_cache()
    prompt = f"Write the outline as a json document for a book entitled: {title}. Please only respond with the json and nothing else. The json must be in the following format: \n\n{data_format}"
    print(prompt)
    convo.add_entry(prompt, Speaker.user)
    # think(convo)
    response = convo.last_entry()
    prompts = generate_prompts(data)
    convo.delete_cache()
    for p in prompts:
        convo.add_entry(p, Speaker.user)
        think(convo)
        fn = speak(
            text=convo.last_entry(), user_id=user.id, use_google=True, save_only=True
        )
        try:
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=fn)
        except:
            pass


def generate_prompts(data):
    prompts = []
    for c in data["chapters"]:
        for s in c["sections"]:
            prompt = f"""Write a section for a book titled: "{data['title']}", chapter: "{c['title']}", section: "{s['title']}", section content: "{s['content']}" """
            prompts.append(prompt)
    print(prompts)
    return prompts


data = {
    "title": "The art of living care free",
    "author": "Unknown",
    "chapters": [
        {
            "title": "Introduction",
            "sections": [{"title": "", "content": "Importance of living care free"}],
        },
        {
            "title": "Chapter 1: Understanding the concept of living care free",
            "sections": [
                {
                    "title": "Section 1: Defining care free living",
                    "content": "What it means to live care free",
                },
                {
                    "title": "Section 2: Common misconceptions",
                    "content": "Dispelling myths about living care free",
                },
            ],
        },
        {
            "title": "Chapter 2: Preparing for a care free life",
            "sections": [
                {
                    "title": "Section 1: Embracing change",
                    "content": "The importance of being open to change",
                },
                {
                    "title": "Section 2: Letting go",
                    "content": "Tips for letting go of things that hold you back",
                },
            ],
        },
        {
            "title": "Chapter 3: Simple habits for a care free life",
            "sections": [
                {
                    "title": "Section 1: Decluttering",
                    "content": "The benefits of decluttering your life and how to do it",
                },
                {
                    "title": "Section 2: Mindfulness",
                    "content": "The role of mindfulness in living care free",
                },
                {
                    "title": "Section 3: Prioritizing self-care",
                    "content": "How taking care of yourself can lead to a care free life",
                },
            ],
        },
        {
            "title": "Chapter 4: Overcoming obstacles to a care free life",
            "sections": [
                {
                    "title": "Section 1: Fear",
                    "content": "How to overcome fear and take risks",
                },
                {
                    "title": "Section 2: Negative self-talk",
                    "content": "Recognizing and changing negative self-talk",
                },
                {
                    "title": "Section 3: Other people's expectations",
                    "content": "The danger of living up to other people's expectations and how to break free",
                },
            ],
        },
        {
            "title": "Chapter 5: Maintaining a care free life",
            "sections": [
                {
                    "title": "Section 1: Staying motivated",
                    "content": "Tips for staying motivated to live care free",
                },
                {
                    "title": "Section 2: Incorporating care free habits into daily life",
                    "content": "How to make care free living a permanent part of your life",
                },
            ],
        },
        {
            "title": "Conclusion",
            "sections": [
                {
                    "title": "",
                    "content": "Final thoughts and encouragement to continue living care free",
                }
            ],
        },
    ],
}


# print(generate_prompts(data))
