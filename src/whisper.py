import openai


def whisper(file):
    file = open(file, "rb")
    r = openai.Audio.transcribe("whisper-1", file)
    return r.get("text")
