import os
import json


def load_config(user_id):
    if not os.path.exists(f"config_{user_id}.json"):
        save_config(user_id, {'language': 'en-US'})
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