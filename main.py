import telethon_auth as ta
import msg_extractor as me
import sentiment
import handlers
from telethon import TelegramClient
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Bot
import os
import asyncio
from pysentimiento import create_analyzer
import pathlib
import threading

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN_BOT_API")
phone_number = os.environ.get("PHONE_NUMBER")
username = "SpottedMood"
spotted_id = -1001409670397

if not api_id or not api_hash or not phone_number:
    raise ValueError("API_ID, API_HASH e PHONE_NUMBER must be set in .env file.")

users_file = pathlib.Path("users.json")

client = TelegramClient(username, api_id, api_hash)
app=ApplicationBuilder().token(bot_token).build()

analyzer = create_analyzer(task="sentiment", lang="it")
hate_analyzer = create_analyzer(task="hate_speech", lang="it")

app.add_handler(CommandHandler("start",handlers.handle_commands(users_file)))

async def main():
    async with client:
        await ta.first_auth(client, phone_number)
        await me.store_messages(client,spotted_id) #I haven't already managed store_messages and run_until_disconnected execution timing to be sure the bot won't stuck on these lines. 
        await client.run_until_disconnected() 
        await sentiment.sentiment_analyze(analyzer, hate_analyzer)

if __name__ == "__main__":
    try:
        threading.Thread(target=lambda: asyncio.run(main()), daemon=True).start()
        app.run_polling()
    except Exception as e:
        print("Error:", e)
