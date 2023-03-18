import os
import tempfile
import asyncio
import logging
import aiofiles
from google.cloud import texttospeech
import conf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def speak(text, user_id):
    logger.info(f"Synthesizing into text: {text}")
    lang = await conf.get_language(user_id)
    logger.info(f"Language: {lang}")

    def synthesize_speech():
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=lang)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        return client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, synthesize_speech)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_name = f"{temp_file.name}.mp3"
    temp_file.close()

    async with aiofiles.open(temp_file_name, "wb") as out:
        await out.write(response.audio_content)
        logger.info(f'Audio content written to file "{temp_file_name}"')

    return temp_file_name
