import json
from telegram.error import TelegramError

async def send_report(bot):

    highlights = []

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
    positive = len(pos_msgs) / num_msgs if num_msgs > 0 else 0
    negative = len(neg_msgs) / num_msgs if num_msgs > 0 else 0

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
    
    max_data = {
        'most_positive': {'value': 0, 'text': ''},
        'most_negative': {'value': 0, 'text': ''},
        'most_hateful': {'value': 0, 'text': ''},
        'most_stereotype': {'value': 0, 'text': ''},
        'max_joy': {'value': 0, 'text': ''},
        'max_sadness': {'value': 0, 'text': ''},
        'max_anger': {'value': 0, 'text': ''},
        'max_fear': {'value': 0, 'text': ''}
    }

    for msg in sentiment:
        if msg['sentiment_probas']['pos'] > max_data['most_positive']['value']:
            max_data['most_positive'] = {'value': msg['sentiment_probas']['pos'], 'text': msg['text']}
        if msg['sentiment_probas']['neg'] > max_data['most_negative']['value']:
            max_data['most_negative'] = {'value': msg['sentiment_probas']['neg'], 'text': msg['text']}
        if msg['hate_probas']['hateful'] > max_data['most_hateful']['value']:
            max_data['most_hateful'] = {'value': msg['hate_probas']['hateful'], 'text': msg['text']}
        if msg['hate_probas']['stereotype'] > max_data['most_stereotype']['value']:
            max_data['most_stereotype'] = {'value': msg['hate_probas']['stereotype'], 'text': msg['text']}
        if msg['emotion_probas']['joy'] > max_data['max_joy']['value']:
            max_data['max_joy'] = {'value': msg['emotion_probas']['joy'], 'text': msg['text']}
        if msg['emotion_probas']['sadness'] > max_data['max_sadness']['value']:
            max_data['max_sadness'] = {'value': msg['emotion_probas']['sadness'], 'text': msg['text']}
        if msg['emotion_probas']['anger'] > max_data['max_anger']['value']:
            max_data['max_anger'] = {'value': msg['emotion_probas']['anger'], 'text': msg['text']}
        if msg['emotion_probas']['fear'] > max_data['max_fear']['value']:
            max_data['max_fear'] = {'value': msg['emotion_probas']['fear'], 'text': msg['text']}

    for key, data in max_data.items():
        highlights.append({
            "emotion": key,
            "text": data["text"],
            "score": round(data["value"], 4)
        })

    with open("highlights.json", "w", encoding="utf-8") as out:
        json.dump(highlights, out, ensure_ascii=False, indent=4)

    for user in users:
        try:
            await bot.send_message(
                chat_id=user['user_id'],
                text = (
                    f"👋 Hello {user['username']}!\n\n"
                    f"🧠 *Today's Sentiment Analysis*\n"
                    f"• 🟢 Positivity: *{positive:.2%}*\n"
                    f"• 🔴 Negativity: *{negative:.2%}*\n"
                    f"• 🏁 Dominant sentiment: *{sentiment_result}*\n\n"

                    f"🎭 *Emotion Overview*\n"
                    f"• 😊 Joy: *{joy:.2%}*\n"
                    f"• 😢 Sadness: *{sadness:.2%}*\n"
                    f"• 😠 Anger: *{anger:.2%}*\n"
                    f"• 😱 Fear: *{fear:.2%}*\n"
                    f"• 🏁 Dominant emotion: *{emotion_result}*\n\n"

                    f"⚠️ *Other Overview*\n"
                    f"• ⁉️ Hate speech: *{hate:.2%}*\n"
                    f"• 🧩 Stereotypes: *{stereotype:.2%}*\n\n"

                    f"📊 *Most Intense Messages*\n"
                    f"• ✨ Most positive: *{max_data['most_positive']['value']:.2%}*\n"
                    f"• 💥 Most negative: *{max_data['most_negative']['value']:.2%}*\n"
                    f"• 🚫 Most hateful: *{max_data['most_hateful']['value']:.2%}*\n"
                    f"• 🧠 Most stereotypical: *{max_data['most_stereotype']['value']:.2%}*\n"
                    f"• 😄 Max joy: *{max_data['max_joy']['value']:.2%}*\n"
                    f"• 😡 Max anger: *{max_data['max_anger']['value']:.2%}*\n"
                    f"• 😭 Max sadness: *{max_data['max_sadness']['value']:.2%}*\n"
                    f"• 😨 Max fear: *{max_data['max_fear']['value']:.2%}*\n\n"

                    f"📅 See you tomorrow with a new report!"
                ),
                parse_mode='Markdown'
            )
            print(f"[REPORTER] Report sent to {user['username']}")
        except TelegramError as e:
            print(f"[REPORTER] Failed to send report to {user['username']}: {e}")
