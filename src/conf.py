import os
import json


# Todo this token math is really not great
model_max_tokens = 4097
response_max_tokens = 1000
prompt_max_tokens = model_max_tokens - response_max_tokens


def load_config(user_id):
    if not os.path.exists(f"config_{user_id}.json"):
        save_config(user_id, {"language": "en-US"})
    with open(f"config_{user_id}.json", "r") as f:
        return json.load(f)


def save_config(user_id, config):
    with open(f"config_{user_id}.json", "w") as f:
        json.dump(config, f, indent=4)


def get_language(user_id):
    config = load_config(user_id)
    return config.get("language")


def set_language(user_id, language):
    config = load_config(user_id)
    config["language"] = language
    save_config(user_id, config)
