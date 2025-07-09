import importlib
import telethon_auth as ta
import msg_extractor as me
from telethon import TelegramClient
import os
import asyncio

importlib.reload(ta)
importlib.reload(me)

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
phone_number = os.environ.get("PHONE_NUMBER")
username = "SpottedMood"
spotted_id = -1001409670397

if not api_id or not api_hash or not phone_number:
    raise ValueError("API_ID, API_HASH e PHONE_NUMBER must be set in .env file.")

client = TelegramClient(username, api_id, api_hash)

async def main():
    async with client:
        await ta.first_auth(client, phone_number)
        await me.store_messages(client,spotted_id)
        await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Error:", e)
