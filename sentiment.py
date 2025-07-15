import json

async def sentiment_analyze(analyzer, hate_analyzer):
    with open('messages.json', 'r', encoding='utf-8') as msgs:
        messages = json.load(msgs)

    results = []

    print("[SENTIMENT] Analyzing today's messages...")
    for msg in messages:
        sentiment = analyzer.predict(msg['text'])
        hatefulness = hate_analyzer.predict(msg['text'])

        results.append({
            'id': msg['id'],
            'sentiment_probas': sentiment.probas,
            'hate_probas': hatefulness.probas
        })

    with open('sentiment.json', 'w', encoding='utf-8') as sntm:
        json.dump(results, sntm, indent=2, ensure_ascii=False)