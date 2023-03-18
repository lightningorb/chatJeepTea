import os
import subprocess
import tempfile
import conf
from google.cloud import texttospeech


async def speak(text, user_id, use_google=True, save_only=False):
    print(f"Synthesizing into text: {text}")
    lang = await conf.get_language(user_id)
    print("=" * 100)
    print(lang)
    print("=" * 100)
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=lang)
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
    return temp_file_name
