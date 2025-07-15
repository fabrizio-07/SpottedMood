from telethon import events
import json

async def store_messages(client, chat_id):
    
    print("Waiting for new messages in Spotted DMI...")
    messages = []

    @client.on(events.NewMessage(chats=chat_id))
    async def handler(event):
        message = event.message
        
        if message and message.text:
            json_message = {
                "id": message.id,
                "date": message.date.isoformat(),
                "text": message.text,
            }
            if not json_message["text"].startswith("by:"):
                messages.append(json_message)
                print(f"New incoming message: '{messages[-1]['text']}'")

                with open("messages.json", "w", encoding="utf-8") as f:
                    json.dump(messages, f, ensure_ascii=False, indent=2)
            