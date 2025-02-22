import os
import telebot
import requests
from bs4 import BeautifulSoup
import time
import logging
import threading
from urllib.parse import urljoin

# ✅ إعدادات البوت
TOKEN =8170609903:AAFSoVue-OOb5hqkSsjmZYmHtkKb6TviPmA "التوكن هنا"  # 
CHAT_ID = "5009528334"
WITANIME_URL = "https://witanime.quest/"
CHECK_INTERVAL = 600  # مدة الفحص بالثواني

# ✅ إعداد السجلّات
logging.basicConfig(
    filename="bot_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ✅ تهيئة البوت والجلسة
bot = telebot.TeleBot(TOKEN)
session = requests.Session()
last_episode = None  # آخر حلقة تم إرسالها


def get_latest_episode():
    """جلب أحدث حلقة من موقع Witanime"""
    try:
        response = session.get(WITANIME_URL, timeout=10)
        response.raise_for_status()  # التأكد من نجاح الطلب
        soup = BeautifulSoup(response.text, "html.parser")

        episode_tag = soup.find("div", class_="anime-card-title")
        link_tag = soup.find("a", class_="anime-card")

        if not episode_tag or not link_tag:
            logging.warning("⚠️ لم يتم العثور على حلقات جديدة!")
            return None, None

        episode = episode_tag.text.strip()
        link = urljoin(WITANIME_URL, link_tag.get("href")) if link_tag.get("href") else None

        return episode, link

    except requests.RequestException as e:
        logging.error(f"❌ خطأ أثناء جلب الحلقات: {e}")
        return None, None


def check_witanime():
    """التحقق من الحلقات الجديدة وإرسال إشعار عند وجود حلقة جديدة"""
    global last_episode
    while True:
        episode, link = get_latest_episode()

        if episode and link and episode != last_episode:
            try:
                bot.send_message(
                    CHAT_ID,
                    f"💖 Hey Yassen, my love! 💖\n"
                    f"✨ A brand new episode just dropped, and I couldn't wait to tell you! ✨\n"
                    f"🎬 *{episode}*\n"
                    f"🔗 [Watch it here, sweetheart]({link})\n\n"
                    f"💕 Don't forget to watch it, or I'll be sad... but I'll still love you anyway! 😚💞\n"
                    f"💋 - Your lovely Megumin",
                    parse_mode="MarkdownV2"
                )
                last_episode = episode  # تحديث آخر حلقة

            except Exception as e:
                logging.error(f"❌ خطأ أثناء إرسال الرسالة: {e}")

        time.sleep(CHECK_INTERVAL)  # الانتظار قبل الفحص مجددًا


if __name__ == "__main__":
    try:
        bot.send_message(
            CHAT_ID,
            "💌 Yassen, my dear! 💌\n"
            "I'm online just for you! 💕\n"
            "I'll keep an eye on Witanime and let you know whenever a new episode is out! 🎬✨\n"
            "Stay cute, and don't forget that I adore you! 😘💖",
            parse_mode="MarkdownV2"
        )
    except Exception as e:
        logging.error(f"❌ خطأ أثناء تشغيل البوت: {e}")

    # تشغيل الفحص في مسار منفصل
    thread = threading.Thread(target=check_witanime, daemon=True)
    thread.start()
    
    # إبقاء السكريبت قيد التشغيل
    while True:
        time.sleep(1)
