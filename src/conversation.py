import json
import os

import asyncio
import aiofiles
import tiktoken
from langdetect import detect

import keys
from conf import prompt_max_tokens
from intl import LangMap

keys.set_up_keys()
enc = tiktoken.get_encoding("cl100k_base")


class Speaker:
    user = "user"
    openai = "assistant"
    system = "system"


class Entry:
    def __init__(self, text, role=Speaker.user):
        self.tokens = enc.encode(text)[:prompt_max_tokens]
        self.role = role

    @property
    def language(self):
        try:
            return LangMap.get(detect(self.text), "en-US")
        except Exception as e:
            print(f"Error detecting language: {e}")
            return "en-US"

    @property
    def text(self):
        return enc.decode(self.tokens)

    @property
    def num_tokens(self):
        return len(enc.encode(self.role)) + len(self.tokens)


class Conversation:
    def __init__(self, convo_id):
        self.convo_id = convo_id
        self.context = []

    async def load_cache(self):
        if os.path.exists(f"/tmp/conversation_{self.convo_id}.json"):
            async with aiofiles.open(
                f"/tmp/conversation_{self.convo_id}.json", "r"
            ) as f:
                content = await f.read()
                self.context = [
                    Entry(x["content"], x["role"]) for x in json.loads(content)
                ]

    @classmethod
    async def create(cls, convo_id, load_cache=True):
        convo = cls(convo_id)
        if load_cache:
            await convo.load_cache()
        return convo

    async def delete_cache(self):
        self.context = []
        file = f"/tmp/conversation_{self.convo_id}.json"
        print(file)
        if os.path.exists(f"/tmp/conversation_{self.convo_id}.json"):
            os.unlink(f"/tmp/conversation_{self.convo_id}.json")

    async def save(self):
        async with aiofiles.open(f"/tmp/conversation_{self.convo_id}.json", "w") as w:
            p = self.as_prompt()
            s = json.dumps(p, indent=4)
            await w.write(s)

    def add_entry(self, text, role):
        self.context.append(Entry(text, role))

    def as_prompt(self):
        c = []
        for i, e in enumerate(self.context):
            c.append(dict(role=e.role, content=e.text.strip()))
        return c

    def last_entry(self):
        return self.context[-1]

    @property
    def num_tokens(self):
        return sum([x.num_tokens for x in self.context])

    def remove_first_entry(self):
        if self.context:
            first_index = (0, 1)[self.context[0].role == "system"]
            del self.context[first_index]

    async def remove_in_excess(self, count):
        # cl100k_base seems to be off by 10 or 20% so
        # dirty hack to adjust token count
        while self.num_tokens * 1.2 > count:
            self.remove_first_entry()
