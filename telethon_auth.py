async def first_auth(client,phone_number):
    await client.connect()
    print("Client connected...")

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input("Insert the Telegram OTP-code: ")
        await client.sign_in(phone_number, code)
    
    me = await client.get_me()
    print("Authenticated as:", me.first_name, f"(@{me.username})")