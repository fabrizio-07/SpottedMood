import json
from telegram.error import TelegramError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

plt.switch_backend('Agg')

def clean_markdown(text):
    return re.sub(r'([*_`\[\]])', r'\\\1', text)

def generate_plot(timestamps, values, emotion_name, color):

    if not timestamps:
        return None

    data = sorted(zip(timestamps, values))
    times = [x[0] for x in data]
    scores = [x[1] for x in data]

    plt.figure(figsize=(10, 5))
    plt.plot(times, scores, marker='o', linestyle='-', color=color, linewidth=2)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gcf().autofmt_xdate()
    
    plt.title(f"{emotion_name.capitalize()} Evolution (Last 24h)")
    plt.xlabel("Time")
    plt.ylabel("Intensity (0-1)")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    filename = f"plot_{emotion_name}.png"
    plt.savefig(filename)
    plt.close()
    return filename

async def send_report(bot):
    print("[REPORTER] Generating report and plots...")

    try:
        with open('sentiment.json', 'r', encoding='utf-8') as sntm:
            sentiment = json.load(sntm)
    except (FileNotFoundError, json.JSONDecodeError):
        print("[REPORTER] Error loading sentiment.json")
        return

    if not sentiment:
        print("[REPORTER] No messages to analyze.")
        return

    sums = {
        'pos': 0, 'neg': 0, 'hateful': 0, 'stereotype': 0,
        'joy': 0, 'sadness': 0, 'anger': 0, 'fear': 0
    }
    
    plot_data = {
        'joy': [], 'sadness': [], 'anger': [], 'fear': [], 'times': []
    }

    max_data = {
        'joy': {'value': -1, 'text': ''},
        'sadness': {'value': -1, 'text': ''},
        'anger': {'value': -1, 'text': ''},
        'fear': {'value': -1, 'text': ''},
        'pos': {'value': -1, 'text': ''},
        'neg': {'value': -1, 'text': ''}
    }

    for msg in sentiment:
 
        try:
            dt = datetime.fromisoformat(msg['date'])
        except ValueError:
            dt = datetime.now()

        plot_data['times'].append(dt)
        
        s_probs = msg['sentiment_probas']
        h_probs = msg['hate_probas']
        e_probs = msg['emotion_probas']

        sums['pos'] += s_probs['pos']
        sums['neg'] += s_probs['neg']
        sums['hateful'] += h_probs['hateful']
        sums['stereotype'] += h_probs['stereotype']
        
        sums['joy'] += e_probs['joy']
        sums['sadness'] += e_probs['sadness']
        sums['anger'] += e_probs['anger']
        sums['fear'] += e_probs['fear']

        plot_data['joy'].append(e_probs['joy'])
        plot_data['sadness'].append(e_probs['sadness'])
        plot_data['anger'].append(e_probs['anger'])
        plot_data['fear'].append(e_probs['fear'])

        mappings = [
            ('joy', e_probs['joy']), ('sadness', e_probs['sadness']),
            ('anger', e_probs['anger']), ('fear', e_probs['fear']),
            ('pos', s_probs['pos']), ('neg', s_probs['neg'])
        ]
        
        for key, val in mappings:
            if val > max_data[key]['value']:
                max_data[key] = {'value': val, 'text': clean_markdown(msg['text'])}

    count = len(sentiment)
    averages = {k: v / count for k, v in sums.items()}
    
    colors = {'joy': 'green', 'sadness': 'blue', 'anger': 'red', 'fear': 'purple'}
    plot_files = {}
    
    for emotion, color in colors.items():
        plot_files[emotion] = generate_plot(plot_data['times'], plot_data[emotion], emotion, color)

    report_data = {
        "date": datetime.now().isoformat(),
        "averages": averages,
        "max_messages": max_data,
        "plots": plot_files
    }
    
    with open("daily_report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=4)
    

    try:
        with open("users.json", "r", encoding='utf-8') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

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

    for user in users:
        try:
            await bot.send_message(
                chat_id=user['user_id'],
                text=(
                    f"👋 *Daily Report Ready!*\n\n"
                    f"The analysis for *Spotted DMI* is complete.\n"
                    f"Select a category below to see the plot and the most intense message."
                ),
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        except TelegramError as e:
            print(f"[REPORTER] Failed to send to {user.get('username', 'Unknown')}: {e}")