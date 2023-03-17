import json
import os

import openai
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
        if load_cache:
            if os.path.exists(f"/tmp/conversation_{convo_id}.json"):
                with open(f"/tmp/conversation_{convo_id}.json", "r") as f:
                    self.context = [
                        Entry(x["content"], x["role"]) for x in json.loads(f.read())
                    ]

    def replace_last_entry_with_text(self, entry):
        self.context[-1] = entry

    def delete_cache(self):
        self.context = []
        if os.path.exists(f"/tmp/conversation_{self.convo_id}.json"):
            os.unlink(f"/tmp/conversation_{self.convo_id}.json")

    def save(self):
        with open(f"/tmp/conversation_{self.convo_id}.json", "w") as w:
            w.write(json.dumps(self.as_prompt(), indent=4))

    def add_entry(self, text, role):
        self.context.append(Entry(text, role))

    def as_prompt(self):
        c = []
        for i, e in enumerate(self.context):
            c.append(dict(role=e.role, content=e.text.strip()))
        return c

    def last_entry(self):
        return self.context[-1].text

    @property
    def num_tokens(self):
        return sum([x.num_tokens for x in self.context])

    def remove_first_entry(self):
        if self.context:
            first_index = (0, 1)[self.context[0].role == "system"]
            del self.context[first_index]

    def remove_in_excess(self, count):
        while self.num_tokens > count:
            self.remove_first_entry()


def think(convo):
    convo.remove_in_excess(prompt_max_tokens)
    convo.save()
    print("Getting completion")
    prompt = convo.as_prompt()
    print("=========")
    print(prompt)
    print("=========")
    print(f"Num tokens according to us: {convo.num_tokens}")
    print("=========")

    while True:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=response_max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        print("response:")
        print(response)
        r = response["choices"][0]["message"]["content"]
        if r:
            convo.add_entry(r, Speaker.openai)
            convo.save()
            break
        else:
            print("Did not get a response. Try again?")
            if input("y/n: ").strip() == "y":
                pass
            else:
                break
