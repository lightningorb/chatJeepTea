# ChatJeepTea

ChatJeepTea is a Telegram chat bot that uses OpenAI's API, Whisper, and Google text-to-speech to enable voice-based conversations in near-realtime. It is written in Python.

## Getting Started

To use ChatJeepTea, you will need to set the following environment variables:
- `TOKEN` for your Telegram bot token
- `OPENAI` for your OpenAI API key
- `GOOGLE_APPLICATION_CREDENTIALS` for your Google Cloud Platform service account keyfile

### Installation

1. Clone this repository
1. `python3 -m venv .venv`
1. `. .venv/bin/activate`
1. Install dependencies with `pip3 install -r src/requirements.txt`
1. Set environment variables (or even better, use direnv)
1. Run `python3 tg_bot.py`

### Usage

To chat with ChatJeepTea, simply add the bot to a Telegram chat and send messages as usual. The bot will respond to your messages with voice messages generated by Google text-to-speech. 

Note: group chats are not currently supported.

## Contributing

We welcome contributions to ChatJeepTea! To get started, simply fork this repository and submit a pull request with your changes. Please commit often. 

## License

ChatJeepTea is currently closed source and not available under an open source license.