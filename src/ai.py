import sys
from utils import think, Entry, Speaker, Conversation
from speak import speak
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
