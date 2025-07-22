import sys
print("▶️ Script has started")
sys.stdout.flush()

import asyncio
import time
import requests
from playwright.async_api import async_playwright

# TOCK_URL = "https://www.exploretock.com/fui-hui-hua-san-francisco"
TOCK_URL = "https://www.exploretock.com/archipelagoseattle"
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
        await page.goto(TOCK_URL, wait_until='networkidle', timeout=60000)
        # Click the Search button to load availability
        print("Clicking Book now")
        await page.click('button:has-text("Book now")')
        # Check for Calendar
        print("Waiting for Calendar")
        await page.wait_for_selector('button.ConsumerCalendar-day')
        print("Calendar loaded")
        available_days = page.locator('button.ConsumerCalendar-day.is-available')
        count = await available_days.count()
        if count > 0:
            dates = []
            for i in range(count):
                label = await available_days.nth(i).get_attribute('aria-label')
                dates.append(label)
            print(f"✅ Found available dates: {dates}")
            send_ifttt_notification()
        else:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"🔍 No availability found. ({timestamp})")
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
