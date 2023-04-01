from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


def main_menu_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "New Conversation", callback_data="new_conversation"
                ),
                InlineKeyboardButton("What is this?", callback_data="intro"),
            ],
            [
                InlineKeyboardButton("Longform", callback_data="longform_info"),
                InlineKeyboardButton("System", callback_data="system_info"),
            ],
        ]
    )
