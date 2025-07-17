import json
from telegram import Update
from telegram.ext import ContextTypes

def handle_commands(users_file):
    print("[HANDLERS] Waiting for commands...")
    async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

        await update.message.reply_text(f"Hello {update.message.from_user.first_name}!\nThat's SpottedMood, a Bot that analyzes sentiment and hatefulness behind the spots and the comments of Spotted DMI.\nI will give you a daily report of them right here, everyday at 10P.M.")

        if users_file.exists():
            with open("users.json", "r", encoding='utf-8') as usrs:
                try:
                    users = json.load(usrs)
                except Exception:
                    users = []
        else:
            users = []

        user_id = update.message.from_user.id
        if not any(u["user_id"] == user_id for u in users):
            users.append({
                "user_id" : user_id,
                "username" : update.message.from_user.first_name
            })
            with open("users.json", "w", encoding='utf-8') as usrs:
                usrs.write(json.dumps(users, ensure_ascii=False, indent=2))

            print(f"[HANDLERS] New user added: {update.message.from_user.first_name}")
    return start