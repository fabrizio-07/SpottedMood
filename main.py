import telethon_auth as ta
import msg_extractor as me
import sentiment
import handlers
import reporter
from telethon import TelegramClient
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Bot
from telegram.error import TelegramError
import os
import asyncio
from pysentimiento import create_analyzer
import pathlib
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN_BOT_API")
phone_number = os.environ.get("PHONE_NUMBER")
username = "SpottedMood"
spotted_id = -1001409670397
users_file = pathlib.Path("users.json")
messages_file = pathlib.Path("messages.json")
highlights_file = pathlib.Path("highlights.json")

if not api_id or not api_hash or not phone_number:
    raise ValueError("API_ID, API_HASH e PHONE_NUMBER must be set in .env file.")

print("[MAIN] Starting the bot")

client = TelegramClient(username, api_id, api_hash)

app=ApplicationBuilder().token(bot_token).build()
start_cmd, highlights_cmd, help_cmd = handlers.handle_commands(users_file, highlights_file)
app.add_handler(CommandHandler("start", start_cmd))
app.add_handler(CommandHandler("highlights", highlights_cmd))
app.add_handler(CommandHandler("help",help_cmd))

sentiment_analyzer = create_analyzer(task="sentiment", lang="it")
hate_analyzer = create_analyzer(task="hate_speech", lang="it")
emotion_analyzer = create_analyzer(task="emotion", lang="it")

scheduler = AsyncIOScheduler()

async def start_listening():
    await me.store_messages(client, spotted_id, messages_file)

async def stop_listening():
    await me.stop_store_messages(client)

async def daily_job():
    print("[MAIN] Starting to analyze messages and send report...")
    await stop_listening()
    await sentiment.sentiment_analyze(sentiment_analyzer, hate_analyzer, emotion_analyzer)
    await reporter.send_report(app.bot)
    print("[MAIN] Emptying messages.json")
    messages_file.write_text("[]")
    await start_listening()

async def main():
    print("[MAIN] Starting initial authentication...")
    await client.connect()
    await ta.first_auth(client, phone_number)
    print("[MAIN] Starting to listen messages...")
    await start_listening()

    scheduler.add_job(daily_job, CronTrigger(hour=22, minute=0))
    scheduler.start()

    await app.initialize()
    await app.start()

    await asyncio.gather(
        app.updater.start_polling(),
        client.disconnected
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Error:", e)
