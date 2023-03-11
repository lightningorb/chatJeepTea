import unittest
from unittest.mock import AsyncMock, patch
from telegram import Update, Message, Voice
from telegram.ext import Context
from main import echo


class TestEcho(unittest.IsolatedAsyncioTestCase):
    async def test_echo(self):
        # Mock necessary objects and dependencies
        user = AsyncMock()
        user.mention_html.return_value = "user"

        voice = AsyncMock(spec=Voice)
        voice.file_id = "123"
        message = AsyncMock(spec=Message)
        message.voice = voice
        message.reply_html = AsyncMock()

        update = AsyncMock(spec=Update)
        update.effective_user = user
        update.message = message

        context = AsyncMock(spec=Context)
        context.bot.get_file.return_value.file_path = "https://example.com/test.ogg"
        context.bot.send_voice = AsyncMock()

        # Call the function and test the result
        with patch("main.whisper") as mock_whisper:
            mock_whisper.return_value = "test whisper"
            with patch("main.think") as mock_think:
                with patch("main.speak") as mock_speak:
                    mock_speak.return_value = "test speak"
                    await echo(update, context)

        mock_whisper.assert_called_once_with("/tmp/123.ogg.mp3")
        mock_think.assert_called_once()
        mock_speak.assert_called_once_with(
            mock_think.return_value.last_entry(), use_google=True, save_only=True
        )
        context.bot.send_voice.assert_called_once_with(
            chat_id=update.effective_chat.id, voice="test speak"
        )
        message.reply_html.assert_called_once_with(
            mock_think.return_value.last_entry(), reply_markup=mock.ANY
        )


if __name__ == "__main__":
    unittest.main()
