import json
from telegram.error import TelegramError

async def send_report(bot):
    try:
        with open('sentiment.json', 'r', encoding='utf-8') as sntm:
            sentiment = json.load(sntm)

    except FileNotFoundError:
        print("[REPORTER] File 'sentiment.json' not found.")
        return
    
    except json.JSONDecodeError:
        print("[REPORTER] Error decoding 'sentiment.json'.")
        return

    pos_msgs = [msg for msg in sentiment if msg['sentiment_probas']['pos'] > msg['sentiment_probas']['neg']]
    neg_msgs = [msg for msg in sentiment if msg['sentiment_probas']['neg'] >= msg['sentiment_probas']['pos']]

    num_msgs = len(pos_msgs) + len(neg_msgs)
    if num_msgs > 0:
        positive = len(pos_msgs) / num_msgs
        negative = len(neg_msgs) / num_msgs
    else:
        positive = 0
        negative = 0

    hate = sum(msg['hate_probas']['hateful'] for msg in sentiment) / len(sentiment)
    stereotype = sum(msg['hate_probas']['stereotype'] for msg in sentiment) / len(sentiment)
    joy = sum(msg['emotion_probas']['joy'] for msg in sentiment) / len(sentiment)
    sadness = sum(msg['emotion_probas']['sadness'] for msg in sentiment) / len(sentiment)
    anger = sum(msg['emotion_probas']['anger'] for msg in sentiment) / len(sentiment)
    fear = sum(msg['emotion_probas']['fear'] for msg in sentiment) / len(sentiment)
    
    emotions={
        'joy' : joy,
        'anger' : anger,
        'fear' : fear,
        'sadness' : sadness
    }
    
    sentiment_result = "positive" if positive > negative else "negative"
    emotion_result = max(emotions, key=emotions.get)

    try:
        with open("users.json", "r", encoding='utf-8') as f:
            users = json.load(f)

    except FileNotFoundError:
        print("[REPORTER] File 'users.json' not found.")
        return
    
    most_pos, most_neg, most_hate, most_stereotype, most_fear, most_anger, most_joy, most_sadness = 0,0,0,0,0,0,0,0
    for msg in sentiment:
        if msg['sentiment_probas']['pos'] > most_pos:
            most_pos = msg['sentiment_probas']['pos']
        if msg['sentiment_probas']['neg'] > most_neg:
            most_neg = msg['sentiment_probas']['neg']
        if msg['hate_probas']['hateful'] > most_hate:
            most_hate = msg['hate_probas']['hateful']
        if msg['hate_probas']['stereotype'] > most_stereotype:
            most_stereotype = msg['hate_probas']['stereotype']  
        if msg['emotion_probas']['joy'] > most_joy:
            most_joy = msg['emotion_probas']['joy']
        if msg['emotion_probas']['sadness'] > most_sadness:
            most_sadness = msg['emotion_probas']['sadness']
        if msg['emotion_probas']['anger'] > most_anger:
            most_anger = msg['emotion_probas']['anger']
        if msg['emotion_probas']['fear'] > most_fear:
            most_fear = msg['emotion_probas']['fear']

    for user in users:
        try:
            await bot.send_message(
                chat_id=user['user_id'],
                text = (
                    f"👋 Hello {user['username']}!\n\n"
                    f"🧠 *Today's Sentiment Analysis*\n"
                    f"• 🟢 Positivity: *{positive:.2%}*\n"
                    f"• 🔴 Negativity: *{negative:.2%}*\n"
                    f"• ⚠️ Hate speech: *{hate:.2%}*\n"
                    f"• 🧩 Stereotypes: *{stereotype:.2%}*\n"
                    f"• 🏁 Dominant sentiment: *{sentiment_result}*\n\n"

                    f"🎭 *Emotion Overview*\n"
                    f"• 😊 Joy: *{joy:.2%}*\n"
                    f"• 😢 Sadness: *{sadness:.2%}*\n"
                    f"• 😠 Anger: *{anger:.2%}*\n"
                    f"• 😱 Fear: *{fear:.2%}*\n"
                    f"• 🏁 Dominant emotion: *{emotion_result}*\n\n"

                    f"📊 *Most Intense Messages*\n"
                    f"• ✨ Most positive: *{most_pos:.2%}*\n"
                    f"• 💥 Most negative: *{most_neg:.2%}*\n"
                    f"• 🚫 Most hateful: *{most_hate:.2%}*\n"
                    f"• 🧠 Most stereotypical: *{most_stereotype:.2%}*\n"
                    f"• 😄 Max joy: *{most_joy:.2%}*\n"
                    f"• 😡 Max anger: *{most_anger:.2%}*\n"
                    f"• 😭 Max sadness: *{most_sadness:.2%}*\n"
                    f"• 😨 Max fear: *{most_fear:.2%}*\n\n"

                    f"📅 See you tomorrow with a new report!"
                ),
                parse_mode='Markdown'
            )
            print(f"[REPORTER] Report sent to {user['username']}")
        except TelegramError as e:
            print(f"[REPORTER] Failed to send report to {user['username']}: {e}")
