import os
import aiohttp
import json

API_KEY = os.environ["OPENAI"]


async def transcribe_audio(file_path):
    url = "https://api.openai.com/v1/engines/whisper-1/transcripts"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/octet-stream",
    }

    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            async with session.post(url, headers=headers, data=f) as resp:
                response = await resp.json()
                return response.get("text")


async def whisper(file):
    return await transcribe_audio(file)
