from telethon import events
import json

listener = None

async def store_messages(client, chat_id):
    global listener
    messages = []

    if listener is not None:
        return

    print("[MSG_EXTRACTOR] Waiting for new messages in Spotted DMI...")

    async def messages_listener(event):
        message = event.message
        if message and message.text and not message.text.startswith("by:"):
            json_message = {
                "id": message.id,
                "date": message.date.isoformat(),
                "text": message.text,
            }
            messages.append(json_message)
            print(f"[MSG_EXTRACTOR] New incoming message: '{json_message['text']}'")
            with open("messages.json", "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)

    listener = messages_listener
    client.add_event_handler(listener, events.NewMessage(chats=chat_id))

async def stop_store_messages(client):
    global listener
    if listener:
        print("[MSG_EXTRACTOR] Stop listening messages")
        client.remove_event_handler(listener)
        listener = None