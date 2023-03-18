import os

API_KEY = os.environ["OPENAI"]


def set_up_keys():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
