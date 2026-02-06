import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

def handle_commands(users_file):

    print("[HANDLERS] Waiting for commands...")
    
    def load_report_data():
        try:
            with open("daily_report.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        data = query.data
        report = load_report_data()

        if not report:
            await query.message.reply_text("⚠️ No report data available yet.")
            return

        if data == "report_stats":

            avg = report['averages']

            topic = report.get('topics', {}).get('general', 'N/A')

            total_sentiment = avg['pos'] + avg['neg']
            
            if total_sentiment > 0:
                pos_pct = avg['pos'] / total_sentiment
                neg_pct = avg['neg'] / total_sentiment
            else:
                pos_pct = 0.0
                neg_pct = 0.0
            
            msg = (
                f"📊 *General Statistics*\n\n"
                f"🗣 *Main Topic:* _{topic}_\n\n"
                f"• Positivity: `{pos_pct:.2%}`\n"
                f"• Negativity: `{neg_pct:.2%}`\n"
                f"• Hate Speech: `{avg['hateful']:.2%}`\n"
                f"• Stereotypes: `{avg['stereotype']:.2%}`\n\n"
                f"• Joy: `{avg['joy']:.2%}`\n"
                f"• Sadness: `{avg['sadness']:.2%}`\n"
                f"• Anger: `{avg['anger']:.2%}`\n"
                f"• Fear: `{avg['fear']:.2%}`\n\n"
                f"Type /highlights to switch category."
            )
            await query.message.reply_text(msg, parse_mode="Markdown")

        elif data.startswith("report_"):

            emotion = data.split("_")[1]
            
            plot_file = report['plots'].get(emotion)
            top_msgs = report['max_messages'].get(emotion, [])

            topic = report.get('topics', {}).get(emotion, 'N/A')

            msg_list_str = ""
            for i, item in enumerate(top_msgs, 1):
                text = item['text']
                if len(text) > 150: 
                    text = text[:150] + "..."
                
                msg_list_str += f"{i}. _{text}_ ({item['value']:.1%})\n"
            
            caption = (
                f"*{emotion.upper()} Analysis* 📉\n\n"
                f"🗣 *Trending Topic:* _{topic}_\n\n"
                f"Here is how {emotion} fluctuated over the last 24h.\n\n"
                f"🔥 *Top 5 Intense Messages:*\n"
                f"{msg_list_str}\n\n"
                f"Type /highlights to switch category."
            )


            if plot_file and os.path.exists(plot_file):
                await query.message.reply_photo(
                    photo=open(plot_file, 'rb'),
                    caption=caption,
                    parse_mode="Markdown"
                )
            else:
                await query.message.reply_text(f"⚠️ Plot not found for {emotion}.\n\n{caption}", parse_mode="Markdown")

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

        print(f"[HANDLERS] {update.message.from_user.first_name} has used /start")

        user = update.message.from_user
        await update.message.reply_text(
            f"👋 *Hey {user.first_name}!* \n\n"
            f"I'm *SpottedMood*. I analyze Spotted DMI daily.\n"
            f"I'll send you an interactive report at 10 PM. Use /highlights to see the menu now.",
            parse_mode="Markdown"
        )
        
        if users_file.exists():
            with open("users.json", "r", encoding='utf-8') as usrs:
                try: users = json.load(usrs)
                except: users = []
        else: users = []
        
        if not any(u["user_id"] == user.id for u in users):
            users.append({"user_id": user.id, "username": user.first_name})
            with open("users.json", "w", encoding='utf-8') as usrs:
                usrs.write(json.dumps(users, indent=2))

    async def highlights(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        print(f"[HANDLERS] {update.message.from_user.first_name} has used /highlights")

        keyboard = [
            [
                InlineKeyboardButton("😊 Joy", callback_data="report_joy"),
                InlineKeyboardButton("😢 Sadness", callback_data="report_sadness")
            ],
            [
                InlineKeyboardButton("😠 Anger", callback_data="report_anger"),
                InlineKeyboardButton("😱 Fear", callback_data="report_fear")
            ],
            [
                InlineKeyboardButton("📊 General Stats", callback_data="report_stats")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📊 *Select a category to view analysis & plots:*",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def help(update: Update, context:ContextTypes.DEFAULT_TYPE):

        print(f"[HANDLERS] {update.message.from_user.first_name} has used /help")

        await update.message.reply_text(
            "🛠 *SpottedMood Bot Help*\n\n"
            "Here are the available commands:\n\n"
            "• /start – Introduce SpottedMood Bot and subscribe to the daily report about mood, emotions, stereotypical and hateful content detected in Spotted DMI.\n"
            "• /highlights – Show the most intense messages and a plot of each emotion, from the latest report.\n"
            "• /stop – Unsubscribe from daily reports.\n"
            "• /help – Display this help message.\n\n"
            "For issues or feedback, contact the bot admin: @Avaja\\_mbare\n\n"
            "Stay tuned and keep spot! 🤖💬",
            parse_mode="Markdown"
        )

    async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):

        print(f"[HANDLERS] {update.message.from_user.first_name} has used /stop")

        if users_file.exists():
            with open("users.json", "r", encoding='utf-8') as usrs:
                try:
                    users = json.load(usrs)
                except Exception:
                    users = []
        else:
            users = []

        user_id = update.message.from_user.id
        initial_count = len(users)
        
        users = [u for u in users if u["user_id"] != user_id]

        if len(users) < initial_count:
            with open("users.json", "w", encoding='utf-8') as usrs:
                usrs.write(json.dumps(users, ensure_ascii=False, indent=2))
            print(f"[HANDLERS] {update.message.from_user.first_name} removed from users.json")

        await update.message.reply_text(
            f"I will not send you updates anymore, until you use the /start command again! 👋✨",
            parse_mode="Markdown"
        )

    return start, highlights, help, stop, button_handler