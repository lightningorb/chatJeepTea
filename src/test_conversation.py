import json
from unittest.mock import MagicMock, AsyncMock
import unittest
import asyncio
from unittest.mock import patch
from conversation import Conversation, Entry, Speaker


class TestEntry(unittest.TestCase):
    def test_entry_language(self):
        entry = Entry("Bonjour, comment ça va?")
        self.assertEqual(entry.language, "fr-FR")

    def test_entry_text(self):
        entry = Entry("Hello, how are you?")
        self.assertEqual(entry.text, "Hello, how are you?")

    def test_entry_num_tokens(self):
        entry = Entry("Hello, how are you?", Speaker.user)
        expected_token_count = len(entry.tokens) + len(entry.role) + 1
        self.assertEqual(entry.num_tokens, 7)


class TestConversation(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_add_entry(self):
        convo = Conversation("test_convo")
        convo.add_entry("Hello, how are you?", Speaker.user)
        self.assertEqual(len(convo.context), 1)
        self.assertEqual(convo.context[0].text, "Hello, how are you?")
        self.assertEqual(convo.context[0].role, Speaker.user)

    def test_as_prompt(self):
        convo = Conversation("test_convo")
        convo.add_entry("Hello, how are you?", Speaker.user)
        prompt = convo.as_prompt()
        self.assertEqual(len(prompt), 1)
        self.assertEqual(prompt[0]["role"], Speaker.user)
        self.assertEqual(prompt[0]["content"], "Hello, how are you?")

    def test_last_entry(self):
        convo = Conversation("test_convo")
        convo.add_entry("Hello, how are you?", Speaker.user)
        last_entry = convo.last_entry()
        self.assertEqual(last_entry.text, "Hello, how are you?")
        self.assertEqual(last_entry.role, Speaker.user)

    def test_remove_first_entry(self):
        convo = Conversation("test_convo")
        convo.add_entry("Hello, how are you?", Speaker.user)
        convo.add_entry("I'm doing well, thank you!", Speaker.openai)
        convo.remove_first_entry()
        self.assertEqual(len(convo.context), 1)
        self.assertEqual(convo.context[0].text, "I'm doing well, thank you!")
        self.assertEqual(convo.context[0].role, Speaker.openai)


if __name__ == "__main__":
    unittest.main()
