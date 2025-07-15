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

    positive = sum(msg['sentiment_probas']['pos'] for msg in sentiment) / len(sentiment)
    negative = sum(msg['sentiment_probas']['neg'] for msg in sentiment) / len(sentiment)
    hate = sum(msg['hate_probas']['hateful'] for msg in sentiment) / len(sentiment)
    stereotype = sum(msg['hate_probas']['stereotype'] for msg in sentiment) / len(sentiment)
    
    sentiment_result = "positive" if positive > negative else "negative"

    try:
        with open("users.json", "r", encoding='utf-8') as f:
            users = json.load(f)

    except FileNotFoundError:
        print("[REPORTER] File 'users.json' not found.")
        return
    
    most_pos, most_neg, most_hate, most_stereotype = 0,0,0,0
    for msg in sentiment:
        if msg['sentiment_probas']['pos'] > most_pos:
            most_pos = msg['sentiment_probas']['pos']
        if msg['sentiment_probas']['neg'] > most_neg:
            most_neg = msg['sentiment_probas']['neg']
        if msg['hate_probas']['hateful'] > most_hate:
            most_hate = msg['hate_probas']['hateful']
        if msg['hate_probas']['stereotype'] > most_stereotype:
            most_stereotype = msg['hate_probas']['stereotype']

    for user in users:
        try:
            await bot.send_message(
                chat_id=user['user_id'],
                text=(
                    f"Hi {user['username']}!\n\n"
                    f"Today's sentiment analysis results are:\n"
                    f"Most common mood: {sentiment_result}\n"
                    f"{positive:.2%} positive\n"
                    f"{negative:.2%} negative\n"
                    f"{hate:.2%} hateful\n"
                    f"{stereotype:.2%} stereotype\n\n"
                    f"Most positivite message has {most_pos:.2%} positive mood\n"
                    f"Most negativity message has {most_neg:.2%} negative mood\n"
                    f"Most hateful message has {most_hate:.2%} hatefulness\n"
                    f"Most stereotyped message has {most_stereotype:.2%} stereotype\n\n"
                    "See you tomorrow for the next report!"
                )
            )
            print(f"[REPORTER] Report sent to {user['username']}")
        except TelegramError as e:
            print(f"[REPORTER] Failed to send report to {user['username']}: {e}")
