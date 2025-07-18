import json
from telegram import Update
from telegram.ext import ContextTypes

def handle_commands(users_file):
    print("[HANDLERS] Waiting for commands...")
    async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

        await update.message.reply_text(
            f"👋 *Hey {update.message.from_user.first_name}!* \n\n"
            f"I'm *SpottedMood* — your friendly mood analyst bot! 🧠💬\n\n"
            f"Every day at 🕙 *10:00 PM*, I’ll send you a quick report about the *sentiment*, *emotions*, and *hateful content* found in the spots and comments from *Spotted DMI*.\n\n"
            f"Stay tuned to see how the mood of the day evolves! 📊✨",
            parse_mode='Markdown'
        )

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