import os
import json
import aiofiles

# Todo this token math is really not great
model_max_tokens = 4097
response_max_tokens = 1000
prompt_max_tokens = model_max_tokens - response_max_tokens


async def load_config(user_id):
    if not os.path.exists(f"config_{user_id}.json"):
        await save_config(user_id, {"language": "en-US"})
    async with aiofiles.open(f"config_{user_id}.json", "r") as f:
        return json.loads(await f.read())


async def save_config(user_id, config):
    async with aiofiles.open(f"config_{user_id}.json", "w") as f:
        await f.write(json.dumps(config, indent=4))


async def get_language(user_id):
    config = await load_config(user_id)
    return config.get("language")


async def set_language(user_id, language):
    config = await load_config(user_id)
    config["language"] = language
    await save_config(user_id, config)
