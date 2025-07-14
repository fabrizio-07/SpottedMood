import importlib
import telethon_auth as ta
import msg_extractor as me
import sentiment
from telethon import TelegramClient
import os
import asyncio
from pysentimiento import create_analyzer

importlib.reload(ta)
importlib.reload(me)
importlib.reload(sentiment)

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
phone_number = os.environ.get("PHONE_NUMBER")
username = "SpottedMood"
spotted_id = -1001409670397

if not api_id or not api_hash or not phone_number:
    raise ValueError("API_ID, API_HASH e PHONE_NUMBER must be set in .env file.")

client = TelegramClient(username, api_id, api_hash)

analyzer = create_analyzer(task="sentiment", lang="it")
hate_analyzer = create_analyzer(task="hate_speech", lang="it")

async def main():
    async with client:
        await ta.first_auth(client, phone_number)
        await me.store_messages(client,spotted_id) #I haven't already managed store_messages and run_until_disconnected execution timing to be sure the bot won't stuck on these lines. 
        await client.run_until_disconnected() 
        await sentiment.sentiment_analyze(analyzer, hate_analyzer)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Error:", e)
