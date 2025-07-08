from telethon import TelegramClient
import os

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
phone_number = os.environ.get('PHONE_NUMBER')  

client = TelegramClient('SpottedMoodBot', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)  
    me = await client.get_me()
    print("Autenticato come utente:", me.first_name, me.username)

with client:
    client.loop.run_until_complete(main())
