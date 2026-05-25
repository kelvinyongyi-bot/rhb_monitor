import requests
from bs4 import BeautifulSoup
import time
import os

BOT_TOKEN = os.getenv("8932643702:AAFlkU8olEtBwQihXSWkfICIXaQvpdNTu8k")
CHAT_ID = os.getenv("7785113371")

URL = "https://onlinebanking.rhbgroup.com/"
CACHE_FILE = "rhb_cache.txt"


def send_telegram(msg):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(api, data=data)


def get_page_content():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers, timeout=30)
    return r.text


def check_update():
    html = get_page_content()

    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text()

    keyword = "maintenance"

    lines = []

    for line in text.splitlines():
        if keyword.lower() in line.lower():
            clean = line.strip()

            if clean:
                lines.append(clean)

    result = "\\n".join(lines)

    old = ""

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            old = f.read()

    if result != old and result != "":
        send_telegram(f"RHB Maintenance Update Detected:\\n\\n{result}")

        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(result)

        print("NEW UPDATE SENT")

    else:
        print("START")
        
        send_telegram("BOT ONLINE")

while True:
    try:
        check_update()
    except Exception as e:
        print("ERROR:", e)

    time.sleep(300)
