import asyncio
import os
from playwright.async_api import async_playwright
import time
import requests

import subprocess
subprocess.run(["python", "-m", "playwright", "install", "chromium"], check=True)


TOCK_URL = "https://www.exploretock.com/fui-hui-hua-san-francisco"
IFTTT_EVENT_NAME = "fuhuihua_available"
IFTTT_KEY = "b5eKE_D5CdwaQ_OwMpQGga"
CHECK_INTERVAL_SECONDS = 300

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

async def check_page(playwright):
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    try:
        await page.goto(TOCK_URL, timeout=60000)
        content = await page.content()
        if "Available" in content or "availability" in content.lower():
            print("✅ Found availability! Sending notification...")
            send_ifttt_notification()
        else:
            print("🔍 No availability found. (", time.strftime('%Y-%m-%d %H:%M:%S'), ")")
    except Exception as e:
        print("❌ Error during check:", e)
    finally:
        await browser.close()

async def main():
    print("🚀 Starting Tock monitor (Playwright version)...")
    while True:
        async with async_playwright() as playwright:
            await check_page(playwright)
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
