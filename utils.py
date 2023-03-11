import tempfile
import json
import re
import subprocess
from google.cloud import texttospeech
import openai
import os
import keys
import sys

keys.set_up_keys()


class Speaker:
    user = "user"
    openai = "assistant"
    system = "system"


class Entry:
    def __init__(self, text, role):
        self.text = text
        self.role = role

    @property
    def num_tokens(self):
        tokens = re.findall(
            r'([^\s"{},:\[\]]*[^\s"{},:]*[^\s"{},:\[\]]*|["{\},:\[\]])', self.text
        )
        return len(tokens)


class Conversation:
    def __init__(self, convo_id):
        self.convo_id = convo_id
        self.context = []
        if os.path.exists(f"/tmp/conversation_{convo_id}.json"):
            with open(f"/tmp/conversation_{convo_id}.json", "r") as f:
                self.context = [
                    Entry(x["content"], x["role"]) for x in json.loads(f.read())
                ]
                print(self.as_prompt())

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
        while self.num_tokens > 1000:
            self.remove_first_entry()


def think(convo):
    convo.save()
    print("Getting completion")
    prompt = convo.as_prompt()
    print("=========")
    print(prompt)
    print("=========")

    convo.remove_in_excess(1000)

    while True:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=1,
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


def speak(text, use_google=False, save_only=False):
    print(f"Synthesizing into text: {text}")
    if use_google:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-GB-Standard-C",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_name = f"{temp_file.name}.mp3"
        temp_file.close()
        with open(temp_file_name, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "{temp_file_name}"')
        if save_only == False:
            os.system(f"afplay {temp_file_name}")
        return temp_file_name
    else:
        subprocess.run(["say", text])


if __name__ == "__main__":
    prompt = """
Great job on completing the warm-up! Here's the next step:
Step 2: Squats - Stand with your feet shoulder-width apart and toes pointed slightly outwards. Slowly bend your knees and lower your hips towards the ground, keeping your chest up and your weight on your heels. Once your thighs are parallel to the ground, push through your heels and return to a standing position. Repeat for 10-12 reps.
Next!
"""

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop="±",
        temperature=1,
    )
    print(response.choices)
