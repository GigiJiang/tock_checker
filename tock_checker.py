import requests
from bs4 import BeautifulSoup
import time

# === Config ===
TOCK_URL = "https://www.exploretock.com/fui-hui-hua-san-francisco"
IFTTT_EVENT_NAME = "fuhuihua_available"
IFTTT_KEY = "b5eKE_D5CdwaQ_OwMpQGga"
CHECK_INTERVAL_SECONDS = 300  # 5 minutes

def check_tock_page():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; TockChecker/1.0)"
        }
        response = requests.get(TOCK_URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        if "Available" in text or "availability" in text.lower():
            print("✅ Found availability! Sending notification...")
            send_ifttt_notification()
        else:
            print("🔍 No availability found. (", time.strftime('%Y-%m-%d %H:%M:%S'), ")")
    except Exception as e:
        print("❌ Error during check:", e)

def send_ifttt_notification():
    url = f"https://maker.ifttt.com/trigger/{IFTTT_EVENT_NAME}/with/key/{IFTTT_KEY}"
    data = {
        "value1": "Fui Hui Hua 有位置了！",
        "value2": TOCK_URL
    }
    try:
        r = requests.post(url, json=data)
        if r.status_code == 200:
            print("📲 Notification sent via IFTTT")
        else:
            print("⚠️ Failed to send notification:", r.text)
    except Exception as e:
        print("❌ Notification error:", e)

if __name__ == "__main__":
    print("🚀 Starting Tock monitor...")
    while True:
        check_tock_page()
        time.sleep(CHECK_INTERVAL_SECONDS)
