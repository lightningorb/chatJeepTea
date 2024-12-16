import os
import json
import aiofiles


async def load_auth_data(file_path, user_id):
    if not os.path.exists(file_path):
        async with aiofiles.open(file_path, "w") as w:
            await w.write(json.dumps([user_id]))
    async with aiofiles.open(file_path, "r") as f:
        data = await f.read()
    return json.loads(data)


async def check_is_authorized(user_id):
    file_path = "src/auth.json"
    try:
        auth_data = await load_auth_data(file_path, user_id)
        return user_id in auth_data
    except Exception as e:
        print(f"Error while checking authorization: {e}")
        return False
