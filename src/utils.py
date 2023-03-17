import json
import os

import aiohttp
import aiofiles
import tiktoken
from conf import prompt_max_tokens, response_max_tokens

import keys

keys.set_up_keys()
enc = tiktoken.get_encoding("gpt2")


class Speaker:
    user = "user"
    openai = "assistant"
    system = "system"


class Entry:
    def __init__(self, text, role=Speaker.user):
        self.tokens = enc.encode(text)[:prompt_max_tokens]
        self.role = role

    @property
    def text(self):
        return enc.decode(self.tokens)

    @property
    def num_tokens(self):
        return len(self.tokens)


class Conversation:
    def __init__(self, convo_id, load_cache=True):
        self.convo_id = convo_id
        self.context = []
        # if load_cache:
        #     if os.path.exists(f"/tmp/conversation_{convo_id}.json"):
        #         with open(f"/tmp/conversation_{convo_id}.json", "r") as f:
        #             self.context = [
        #                 Entry(x["content"], x["role"]) for x in json.loads(f.read())
        #             ]

    async def replace_last_entry_with_text(self, entry):
        self.context[-1] = entry

    async def delete_cache(self):
        self.context = []
        if os.path.exists(f"/tmp/conversation_{self.convo_id}.json"):
            os.unlink(f"/tmp/conversation_{self.convo_id}.json")

    async def save(self):
        pass
        # async with aiofiles.open(f"/tmp/conversation_{self.convo_id}.json", "w") as w:
        #     await w.write(await json.dumps(self.as_prompt(), indent=4))

    async def add_entry(self, text, role):
        self.context.append(Entry(text, role))

    async def as_prompt(self):
        c = []
        for i, e in enumerate(self.context):
            c.append(dict(role=e.role, content=e.text.strip()))
        return c

    async def last_entry(self):
        return self.context[-1].text

    @property
    async def num_tokens(self):
        return sum([x.num_tokens for x in self.context])

    async def remove_first_entry(self):
        if self.context:
            first_index = (0, 1)[self.context[0].role == "system"]
            del self.context[first_index]

    async def remove_in_excess(self, count):
        while await self.num_tokens > count:
            await self.remove_first_entry()


async def think(convo):
    await convo.remove_in_excess(prompt_max_tokens)
    await convo.save()
    print("Getting completion")
    prompt = await convo.as_prompt()
    print("=========")
    print(prompt)
    print("=========")
    print(f"Num tokens according to us: {await convo.num_tokens}")
    print("=========")

    while True:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {keys.API_KEY}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": prompt,
                    "max_tokens": response_max_tokens,
                    "n": 1,
                    "stop": None,
                    "temperature": 0.7,
                },
            ) as resp:
                response = await resp.json()
                print("response:")
                print(response)
                r = response["choices"][0]["message"]["content"]
                if r:
                    await convo.add_entry(r, Speaker.openai)
                    await convo.save()
                    break
                else:
                    print("Did not get a response. Try again?")
                    if input("y/n: ").strip() == "y":
                        pass
                    else:
                        break
