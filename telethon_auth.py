from telethon.errors import SessionPasswordNeededError

async def first_auth(client,phone_number):
    await client.connect()
    print("[TELETHON_AUTH] Client connected...")

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        try:
            code = input("[TELETHON_AUTH] Insert the Telegram OTP-code: ")
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            password = input("[TELETHON_AUTH] Two-step verification enabled. Please enter your password: ")
            await client.sign_in(password=password)
    
    me = await client.get_me()
    print("[TELETHON_AUTH] Authenticated as:", me.first_name, f"(@{me.username})")