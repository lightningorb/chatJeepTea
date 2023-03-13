from google.cloud import texttospeech
import keys

keys.set_up_keys()

client = texttospeech.TextToSpeechClient()

voices = client.list_voices().voices

for voice in voices:
    name = voice.name
    language_codes = ", ".join(voice.language_codes)
    gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name

    print(f"Name: {name}")
    print(f"Supported language codes: {language_codes}")
    print(f"Gender: {gender}")
    print()
