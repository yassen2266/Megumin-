import telebot
import requests
from bs4 import BeautifulSoup
import time
import logging

# ✅ Bot settings
TOKEN = "8170609903:AAFSoVue-OOb5hqkSsjmZYmHtkKb6TviPmA"
CHAT_ID = "5009528334"
WITANIME_URL = "https://witanime.com/"
CHECK_INTERVAL = 600  # Time interval in seconds

# ✅ Logging setup
logging.basicConfig(filename="bot_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Initialize bot
bot = telebot.TeleBot(TOKEN)
session = requests.Session()
last_episode = ""

def get_latest_episode():
    """Fetches the latest episode from Witanime."""
    response = session.get(WITANIME_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    episode_tag = soup.find("div", class_="anime-card-title")
    link_tag = soup.find("a", class_="anime-card")
    
    if not episode_tag or not link_tag:
        raise ValueError("⚠️ No episode data found!")

    episode = episode_tag.text.strip()
    link = WITANIME_URL.rstrip("/") + link_tag["href"]

    return episode, link

def check_witanime():
    """Checks for new episodes and sends a notification if a new one is found."""
    global last_episode

    while True:
        try:
            episode, link = get_latest_episode()

            if episode != last_episode:
                bot.send_message(
                    CHAT_ID, 
                    f"✨🔥 Explosion! 🔥✨\n"
                    f"🆕 *Yassen!* A new episode just dropped!\n"
                    f"🎬 *{episode}*\n"
                    f"🔗 [Watch now]({link})\n\n"
                    f"💖 Don't forget to watch it, or I'll cast an even BIGGER explosion next time or mapye kissing you🙈! 🔥\n"
                    f"🔮 - Megumin"
                    , parse_mode="Markdown"
                )
                last_episode = episode

        except Exception as e:
            logging.error(f"❌ Error occurred: {e}")
            print(f"❌ Error: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    bot.send_message(
        CHAT_ID, 
        "⚡✨ Megumin is now online! ✨⚡\n"
        "🔥 I'm watching Witanime for you, *Yassen!* 🔥\n"
        "🚀 Get ready for explosions of new episodes!\n"
        "💥 Explosion!!! 💥"
        , parse_mode="Markdown"
    )
    check_witanime()
