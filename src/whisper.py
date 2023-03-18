import os
import aiohttp

API_KEY = os.environ["OPENAI"]

async def transcribe_audio(file_path):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }

    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            form_data = aiohttp.FormData()
            form_data.add_field("model", "whisper-1")
            form_data.add_field("file", f, filename=os.path.basename(file_path), content_type="audio/mpeg")
            
            async with session.post(url, headers=headers, data=form_data) as resp:
                response = await resp.json()
                return response.get("text")


async def whisper(file):
    return await transcribe_audio(file)
