import os
import subprocess
import tempfile
import conf
from google.cloud import texttospeech


def speak(text, user_id, use_google=False, save_only=False):
    print(f"Synthesizing into text: {text}")
    lang = conf.get_language(user_id)
    print("=" * 100)
    print(lang)
    print("=" * 100)
    if use_google:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            # language_code="en-US",
            # name="en-GB-Standard-C",
            language_code=lang
            # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
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
