import telebot
import requests
from bs4 import BeautifulSoup
import time
import logging
from urllib.parse import urljoin

# ✅ Bot settings
TOKEN = "8170609903:AAFSoVue-OOb5hqkSsjmZYmHtkKb6TviPmA"  # Fake token for testing
CHAT_ID = "5009528334"  # Change this if needed
WITANIME_URL = "https://witanime.com/"
CHECK_INTERVAL = 600  # Time interval in seconds

# ✅ Logging setup
logging.basicConfig(
    filename="bot_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ✅ Initialize bot and session
bot = telebot.TeleBot(TOKEN)
session = requests.Session()
last_episode = None  # Stores the last sent episode


def get_latest_episode():
    """Fetch the latest episode from Witanime."""
    try:
        response = session.get(WITANIME_URL, timeout=10)
        response.raise_for_status()  # Ensure request was successful
        soup = BeautifulSoup(response.text, "html.parser")

        episode_tag = soup.find("div", class_="anime-card-title")
        link_tag = soup.find("a", class_="anime-card")

        if not episode_tag or not link_tag:
            raise ValueError("⚠️ No new episodes found!")

        episode = episode_tag.text.strip()
        link = urljoin(WITANIME_URL, link_tag["href"])  # Properly format the link

        return episode, link

    except requests.RequestException as e:
        logging.error(f"❌ Error fetching episodes: {e}")
        return None, None


def check_witanime():
    """Check for new episodes and send a notification if a new one is found."""
    global last_episode

    while True:
        episode, link = get_latest_episode()

        if episode and link and episode != last_episode:
            try:
                bot.send_message(
                    CHAT_ID,
                    f"💖 Hey Yassin, my love! 💖\n"
                    f"✨ A brand new episode just dropped, and I couldn't wait to tell you! ✨\n"
                    f"🎬 *{episode}*\n"
                    f"🔗 [Watch it here, sweetheart]({link})\n\n"
                    f"💕 Don't forget to watch it, or I'll be sad... but I'll still love you anyway! 😚💞\n"
                    f"💋 - Your lovely Megumin"
                    , parse_mode="Markdown"
                )
                last_episode = episode  # Update last episode

            except Exception as e:
                logging.error(f"❌ Error sending message: {e}")

        time.sleep(CHECK_INTERVAL)  # Wait before checking again


if __name__ == "__main__":
    try:
        bot.send_message(
            CHAT_ID,
            "💌 Yassyn, my dear! 💌\n"
            "I'm online just for you! 💕\n"
            "I'll keep an eye on Witanime and let you know whenever a new episode is out! 🎬✨\n"
            "Stay cute, and don't forget that I adore you! 😘💖"
            , parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"❌ Error starting the bot: {e}")

    check_witanime()  # Start checking for episodes
