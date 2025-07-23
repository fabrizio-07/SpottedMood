import json
from telegram import Update
from telegram.ext import ContextTypes

def handle_commands(users_file,hl_file):

    print("[HANDLERS] Waiting for commands...")

    with open("highlights.json","r",encoding="utf-8") as f:
        raw_hl = json.load(f)
        hl = {item["emotion"]: item for item in raw_hl}
    
    async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

        print(f"[HANDLERS] {update.message.from_user.first_name} has used /start")

        await update.message.reply_text(
            f"👋 *Hey {update.message.from_user.first_name}!* \n\n"
            f"I'm *SpottedMood* — your friendly mood analyst bot! 🧠💬\n\n"
            f"Every day at 🕙 *10:00 PM*, I’ll send you a quick report about the *sentiment*, *emotions*, and *hateful content* found in the spots and comments from *Spotted DMI*.\n\n"
            f"Type /help to learn more about my commands.\n\n"
            f"Stay tuned to see how the mood of the day evolves! 📊✨",
            parse_mode="Markdown"
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

    async def highlights(update: Update, context:ContextTypes.DEFAULT_TYPE):

        print(f"[HANDLERS] {update.message.from_user.first_name} has used /highlights")

        if hl_file.exists():
            await update.message.reply_text(
                f"📊 *Last Report Most Intense Messages*:\n"
                f"• ✨ Most *positive* message: '{hl.get('most_positive', {}).get('text', 'N/A')}'\n\n"
                f"• 💥 Most *negative* message: '{hl.get('most_negative', {}).get('text', 'N/A')}'\n\n"
                f"• 🚫 Most *hateful* message: '{hl.get('most_hateful', {}).get('text', 'N/A')}'\n\n"
                f"• 🧠 Most *stereotypical* message: '{hl.get('most_stereotype', {}).get('text', 'N/A')}'\n\n"
                f"• 😄 Max *joy* message: '{hl.get('max_joy', {}).get('text', 'N/A')}'\n\n"
                f"• 😡 Max *anger* message: '{hl.get('max_anger', {}).get('text', 'N/A')}'\n\n"
                f"• 😭 Max *sadness* message: '{hl.get('max_sadness', {}).get('text', 'N/A')}'\n\n"
                f"• 😨 Max *fear* message: '{hl.get('max_fear', {}).get('text', 'N/A')}'\n\n",
                parse_mode="Markdown"
            )

    async def help(update: Update, context:ContextTypes.DEFAULT_TYPE):

        print(f"[HANDLERS] {update.message.from_user.first_name} has used /help")

        await update.message.reply_text(
            "🛠 *SpottedMood Bot Help*\n\n"
            "Here are the available commands:\n\n"
            "• /start – Introduce SpottedMood Bot and subscribe to the daily report about mood, emotions, stereotypical and hateful content detected in Spotted DMI.\n"
            "• /highlights – Show the most intense messages from the latest report.\n"
            "• /help – Display this help message.\n\n"
            "For issues or feedback, contact the bot admin: @Avaja\\_mbare\n\n"
            "Stay tuned and keep spot! 🤖💬",
            parse_mode="Markdown"
        )

    return start, highlights, help