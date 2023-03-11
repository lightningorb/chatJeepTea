import sys
from utils import think, speak, Entry, Speaker, Conversation
from record import record
from whisper import whisper

convo = Conversation()
convo.add_entry(
    "You are a physical trainer, with an Msc in sports science. Your goal is to make me lose belly fat.",
    Speaker.system,
)

while True:
    audio = record()
    transcript = whisper(audio)
    convo.add_entry(transcript, Speaker.user)
    think(convo)
    speak(convo.last_entry())
