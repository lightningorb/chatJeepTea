import aiohttp
import asyncio
import logging
import aiofiles
import tempfile
import keys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def speak(text, lang="en-US", model="tts-1", user_id=None):
    logger.info(f"Synthesizing text: {text}")
    logger.info(f"Language: {lang}")
    logger.info(f"Model: {model}")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {keys.API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "input": text,
                "model": model,
                "voice": 'alloy',
                "format": "mp3"
            },
        ) as resp:
            logger.info(f"HTTP Status: {resp.status}")
            if resp.status == 200:
                audio_content = await resp.read()

                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                temp_file_name = temp_file.name
                temp_file.close()

                async with aiofiles.open(temp_file_name, "wb") as out_file:
                    await out_file.write(audio_content)
                    logger.info(f'Audio content written to file "{temp_file_name}"')

                return temp_file_name
            else:
                error = await resp.json()
                logger.error(f"Error synthesizing speech: {error}")
                raise Exception(f"API Error: {error}")

# Example usage
async def main():
    try:
        audio_file = await speak("Hello! How can I assist you today?")
        logger.info(f"Audio file saved at: {audio_file}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())