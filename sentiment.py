import json

async def sentiment_analyze(sentiment_analyzer, hate_analyzer, emotion_analyzer):
    with open('messages.json', 'r', encoding='utf-8') as msgs:
        messages = json.load(msgs)

    results = []

    print("[SENTIMENT] Analyzing today's messages...")
    for msg in messages:
        sentiment = sentiment_analyzer.predict(msg['text'])
        hatefulness = hate_analyzer.predict(msg['text'])
        emotion = emotion_analyzer.predict(msg['text'])

        results.append({
            'id': msg['id'],
            'text': msg['text'],
            'sentiment_probas': sentiment.probas,
            'hate_probas': hatefulness.probas,
            'emotion_probas': emotion.probas
        })

    with open('sentiment.json', 'w', encoding='utf-8') as sntm:
        json.dump(results, sntm, indent=2, ensure_ascii=False)