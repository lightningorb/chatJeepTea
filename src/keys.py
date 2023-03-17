import openai
import os

API_KEY = os.environ["OPENAI"]


def set_up_keys():
    openai.api_key = os.environ["OPENAI"]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
