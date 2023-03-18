import aiohttp
import keys

from conf import prompt_max_tokens, response_max_tokens
from conversation import Speaker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def think(convo):
    await convo.remove_in_excess(prompt_max_tokens)
    await convo.save()
    logger.info("Getting completion")
    prompt = convo.as_prompt()
    logger.info("=========")
    logger.info(prompt)
    logger.info("=========")
    logger.info(f"Num tokens according to us: {convo.num_tokens}")
    logger.info("=========")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {keys.API_KEY}"},
            json={
                "model": "gpt-3.5-turbo",
                "messages": prompt,
                "max_tokens": response_max_tokens,
                "n": 1,
                "stop": None,
                "temperature": 0.7,
            },
        ) as resp:
            response = await resp.json()
            logger.info("response:")
            logger.info(response)
            r = response["choices"][0]["message"]["content"]
            if r:
                convo.add_entry(r, Speaker.openai)
                await convo.save()
