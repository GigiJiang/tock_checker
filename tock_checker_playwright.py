import sys
print("▶️ Script has started")
sys.stdout.flush()

import asyncio
import time
import requests
from playwright.async_api import async_playwright

TEST_URL = "https://www.exploretock.com/archipelagoseattle/experience/537575/2025-chefs-counter-summer-experience"
TOCK_URL = "https://www.exploretock.com/fui-hui-hua-san-francisco/experience/559289/fu-hui-hua-chinese-chef-ges-counter-experience"
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
        await page.goto(TEST_URL, wait_until='domcontentloaded', timeout=60000)

        try:
            await page.wait_for_selector('button.ConsumerCalendar-day.is-available', timeout=10000)
        except:
            ts = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"🔍 No available dates. ({ts})")
            return

        available_days = page.locator('button.ConsumerCalendar-day.is-available')
        count = await available_days.count()

        if count > 0:
            labels = []
            for i in range(count):
                labels.append(await available_days.nth(i).get_attribute('aria-label'))
            print(f"✅ Found available dates: {labels}")
            send_ifttt_notification()
        else:
            ts = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"🔍 No available dates (but passed selector wait). ({ts})")

    except Exception as e:
        print("❌ Error during check:", e)
    finally:
        await browser.close()


async def main():
    print("🚀 Starting Tock monitor (Playwright via Docker)...")
    sys.stdout.flush()
    while True:
        async with async_playwright() as playwright:
            await check_page(playwright)
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
