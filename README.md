# SpottedMood: Automated SpottedDMI Analytics

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](#)
[![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](#)

## 📌 Summary
SpottedMood is an asynchronous, automated data-ingestion and Natural Language Processing (NLP) Telegram Bot, designed to extract, analyze, and report sentiment and emotions, within SpottedDMI community. It provides daily analytics (Sentiment, Hate Speech, Emotion, Stereotype, Topic) to help community managers and users monitor group health and user interactions.

## 🚀 Hardware requirements
The entire pipeline, including the continuous asynchronous polling and the execution of NLP models, is highly optimized for constrained environments. The system currently runs seamlessly in production on a **Raspberry Pi 4 (2GB RAM)**, demonstrating efficient memory management and preventing Out-Of-Memory exceptions during data processing.

## ⚙️ Architecture & Separation of Concerns
The project is engineered following the Separation of Concerns (SoC) principle, ensuring maintainability and scalability:

* **Data Ingestion (`msg_extractor.py`)**: Dedicated exclusively to asynchronous message extraction via the Telethon library.
* **NLP Pipeline (`sentiment.py & topic.py`)**: Handles the core analysis, currently utilizing `pysentimiento` to evaluate text independently of its source and `gemini-2.5-flash-lite` to get most discussed topics through the day.
* **Reporting System (`reporter.py`)**: Formats the analyzed data and handles outbound communications.
* **Orchestration (`main.py`)**: Acts as the central scheduler using `APScheduler`, coordinating background listening, daily analysis jobs, and user interface commands via `python-telegram-bot`.

## 🛠️ Setup & Installation
To ensure security, all sensitive credentials are managed via environment variables.

1. Clone the repository.
2. Install dependencies via `Pipfile`.
3. Get `Gemini` and `BotFather` API tokens.
4. Create a `.env` file in the root directory with the following variables:
   ```env
   API_ID=your_telegram_api_id
   API_HASH=your_telegram_api_hash
   TOKEN_BOT_API=your_bot_token
   PHONE_NUMBER=your_phone_number
   GEMINI_API_KEY=your_gemini_api_key
   ```
5. Execute telethon_auth.py
6. Execute main.py
   
## 🤳🏻 Usability
To interact with SpottedMood, simply start a chat with the bot and use the following commands:

* **/start** – Introduces the bot's features and subscribes you to the daily reports (sent at 10 PM) regarding mood, emotions, and content analysis.
* **/highlights** – Opens an interactive menu to view the most intense messages and graphical plots, generated using `matplotlib`, for specific emotions (Joy, Sadness, Anger, Fear) and general statistics.
* **/stop** – Unsubscribes you from the daily automated reports.
* **/help** – Displays the available commands and admin contact information for support.

## 📄 License
This project is licensed under the GNU General Public License v3.0 (GPLv3). See the [LICENSE](LICENSE) file for more details.
