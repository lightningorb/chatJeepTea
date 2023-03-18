from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


async def lang_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Languages",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Afrikaans (South Africa)", callback_data="lang: af-ZA"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Arabic (Saudi Arabia)", callback_data="lang: ar-XA"
                    )
                ],
                [InlineKeyboardButton("Bengali (India)", callback_data="lang: bn-IN")],
                [
                    InlineKeyboardButton(
                        "Bulgarian (Bulgaria)", callback_data="lang: bg-BG"
                    )
                ],
                [InlineKeyboardButton("Catalan (Spain)", callback_data="lang: ca-ES")],
                [
                    InlineKeyboardButton(
                        "Chinese (Mandarin, China)", callback_data="lang: cmn-CN"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Chinese (Mandarin, Taiwan)", callback_data="lang: cmn-TW"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Czech (Czech Republic)", callback_data="lang: cs-CZ"
                    )
                ],
                [InlineKeyboardButton("Danish (Denmark)", callback_data="lang: da-DK")],
                [InlineKeyboardButton("Dutch (Belgium)", callback_data="lang: nl-BE")],
                [
                    InlineKeyboardButton(
                        "Dutch (Netherlands)", callback_data="lang: nl-NL"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "English (Australia)", callback_data="lang: en-AU"
                    )
                ],
                [InlineKeyboardButton("English (India)", callback_data="lang: en-IN")],
                [
                    InlineKeyboardButton(
                        "English (United Kingdom)", callback_data="lang: en-GB"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "English (United States)", callback_data="lang: en-US"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Filipino (Philippines)", callback_data="lang: fil-PH"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Finnish (Finland)", callback_data="lang: fi-FI"
                    )
                ],
                [InlineKeyboardButton("French (Canada)", callback_data="lang: fr-CA")],
                [InlineKeyboardButton("French (France)", callback_data="lang: fr-FR")],
                [InlineKeyboardButton("Greek (Greece)", callback_data="lang: el-GR")],
                [InlineKeyboardButton("Gujarati (India)", callback_data="lang: gu-IN")],
                [InlineKeyboardButton("Hebrew (Israel)", callback_data="lang: he-IL")],
                [InlineKeyboardButton("Hindi (India)", callback_data="lang: hi-IN")],
                [
                    InlineKeyboardButton(
                        "Hungarian (Hungary)", callback_data="lang: hu-HU"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Icelandic (Iceland)", callback_data="lang: is-IS"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Indonesian (Indonesia)", callback_data="lang: id-ID"
                    )
                ],
                [InlineKeyboardButton("Italian (Italy)", callback_data="lang: it-IT")],
                [InlineKeyboardButton("Japanese (Japan)", callback_data="lang: ja-JP")],
                [InlineKeyboardButton("Kannada (India)", callback_data="lang: kn-IN")],
                [
                    InlineKeyboardButton(
                        "Korean (South Korea)", callback_data="lang: ko-KR"
                    )
                ],
                [InlineKeyboardButton("Latvian (Latvia)", callback_data="lang: lv-LV")],
                [
                    InlineKeyboardButton(
                        "Lithuanian (Lithuania)", callback_data="lang: lt-LT"
                    )
                ],
                [InlineKeyboardButton("Malay (Malaysia)", callback_data="lang: ms-MY")],
                [
                    InlineKeyboardButton(
                        "Malayalam (India)", callback_data="lang: ml-IN"
                    )
                ],
                [InlineKeyboardButton("Marathi (India)", callback_data="lang: mr-IN")],
                [
                    InlineKeyboardButton(
                        "Norwegian Bokmål (Norway)", callback_data="lang: nb-NO"
                    )
                ],
                [InlineKeyboardButton("Polish (Poland)", callback_data="lang: pl-PL")],
                [
                    InlineKeyboardButton(
                        "Portuguese (Brazil)", callback_data="lang: pt-BR"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Portuguese (Portugal)", callback_data="lang: pt-PT"
                    )
                ],
                [InlineKeyboardButton("Punjabi (India)", callback_data="lang: pa-IN")],
                [
                    InlineKeyboardButton(
                        "Romanian (Romania)", callback_data="lang: ro-RO"
                    )
                ],
                [InlineKeyboardButton("Russian", callback_data="lang: ru-RU")],
                [InlineKeyboardButton("Serbian (Serbia)", callback_data="lang: sr-RS")],
                [InlineKeyboardButton("Spanish (Spain)", callback_data="lang: es-ES")],
                [
                    InlineKeyboardButton(
                        "Spanish (United States)", callback_data="lang: es-US"
                    )
                ],
                [InlineKeyboardButton("Swedish (Sweden)", callback_data="lang: sv-SE")],
                [InlineKeyboardButton("Tamil (India)", callback_data="lang: ta-IN")],
                [InlineKeyboardButton("Telugu (India)", callback_data="lang: te-IN")],
                [InlineKeyboardButton("Thai (Thailand)", callback_data="lang: th-TH")],
                [InlineKeyboardButton("Turkish (Turkey)", callback_data="lang: tr-TR")],
                [
                    InlineKeyboardButton(
                        "Ukrainian (Ukraine)", callback_data="lang: uk-UA"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Vietnamese (Vietnam)", callback_data="lang: vi-VN"
                    )
                ],
            ]
        ),
    )


def main_menu_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "New Conversation", callback_data="new_conversation"
                ),
                InlineKeyboardButton("What is this?", callback_data="intro"),
                InlineKeyboardButton("Set Language", callback_data="lang_menu"),
            ],
            [
                InlineKeyboardButton("Longform", callback_data="longform_info"),
            ],
        ]
    )