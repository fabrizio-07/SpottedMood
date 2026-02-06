import os
import json
from google import genai
from google.genai import types
from collections import defaultdict

async def analyze_daily_topics(sentiment_data):

    print("[TOPIC] Preparing data for LLM...")

    grouped_messages = defaultdict(list)
    all_text = []

    for item in sentiment_data:
        text = item['text']
        all_text.append(text)
        
        emotions = item['emotion_probas']
        dominant_emotion = max(emotions, key=emotions.get)
        
        if len(text) > 7: 
            grouped_messages[dominant_emotion].append(text)

    prompt = f"""
    You are an analyst for a university "Spotted" channel. 
    Below are the messages from today, grouped by the emotion detected.

    Task:
    1. Identify the ONE most discussed topic in the "ALL_MESSAGES" list.
    2. Identify the ONE most discussed topic for EACH emotion category.
    
    Constraints:
    - The topic must be concise (max 5-6 words).
    - If a category has no messages or no clear topic, return "N/A".
    - Output strictly valid JSON.
    - IMPORTANT: Use exactly these keys in your JSON: "general", "joy", "sadness", "anger", "fear".

    Input Data:
    --- ALL MESSAGES ---
    {json.dumps(all_text[:300], ensure_ascii=False)} 
    
    --- JOY MESSAGES ---
    {json.dumps(grouped_messages['joy'][:100], ensure_ascii=False)}
    
    --- SADNESS MESSAGES ---
    {json.dumps(grouped_messages['sadness'][:100], ensure_ascii=False)}
    
    --- ANGER MESSAGES ---
    {json.dumps(grouped_messages['anger'][:100], ensure_ascii=False)}
    
    --- FEAR MESSAGES ---
    {json.dumps(grouped_messages['fear'][:100], ensure_ascii=False)}
    """

    try:
        print("[TOPIC] Calling Gemini API...")
        
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json'
            )
        )

        print(f"[TOPIC] Raw Response: {response.text}")
        
        result = json.loads(response.text)

        result = {k.lower(): v for k, v in result.items()}
        
        default_keys = ["general", "joy", "sadness", "anger", "fear"]
        cleaned_result = {k: result.get(k, "N/A") for k in default_keys}
        
        print("[TOPIC] Success:", cleaned_result)
        return cleaned_result

    except Exception as e:
        print(f"[TOPIC] Error: {e}")
        return {
            "general": "Unknown",
            "joy": "Unknown",
            "sadness": "Unknown",
            "anger": "Unknown",
            "fear": "Unknown"
        }