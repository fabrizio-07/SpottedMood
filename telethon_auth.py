from telethon import TelegramClient
import os

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
phone_number = os.environ.get("PHONE_NUMBER")
username = "SpottedMood"

if not api_id or not api_hash or not phone_number:
    raise ValueError("API_ID, API_HASH e PHONE_NUMBER must be set in .env file.")

client = TelegramClient(username, api_id, api_hash)

async def main():
    await client.connect()
    print("Client connected...")

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input("Insert the Telegram OTP-code: ")
        await client.sign_in(phone_number, code)
    
    me = await client.get_me()
    print("Authenticated as:", me.first_name, f"(@{me.username})")

with client:
    try:
        client.loop.run_until_complete(main())
    except Exception as e:
        print("Error: ", e)

