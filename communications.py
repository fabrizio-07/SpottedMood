import asyncio
import json
import os
from telegram.ext import ApplicationBuilder

token = os.environ.get("TOKEN_BOT_API") 

async def send_announcement():
    if not token:
        print("Error: TOKEN_BOT_API not found in environment variables.")
        return

    print("🚀 Starting announcement broadcast...")
    
    app = ApplicationBuilder().token(token).build()
    
    try:
        with open("users.json", "r", encoding='utf-8') as f:
            users = json.load(f)
    except FileNotFoundError:
        print("❌ No users.json file found.")
        return

    count = 0
    
    for user in users:
        
        name = user.get('username', 'there')

        message = (
            f"ADMIN MESSAGE:\n\n"
            f"Hey {name}!\n" 
            #bla bla bla
        )

        try:
            await app.bot.send_message(
                chat_id=user['user_id'], 
                text=message, 
                parse_mode='Markdown'
            )
            print(f"✅ Sent to {name}")
            count += 1
            await asyncio.sleep(0.1) 
        except Exception as e:
            print(f"❌ Failed to send to {name}: {e}")

    print(f"\n🎉 Broadcast complete. Sent to {count} users.")

if __name__ == "__main__":
    asyncio.run(send_announcement())