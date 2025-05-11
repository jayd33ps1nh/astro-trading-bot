import asyncio
from telegram import Bot
from datetime import datetime, time as dtime
import pytz
import time

# === CONFIGURATION ===
API_TOKEN = '7811272432:AAE0WF60uAKCDw3hyTeN-xcDWxuKZSRtJ8Q'
CHAT_ID = 787078802  # Your Telegram chat ID
TIMEZONE = pytz.timezone("Asia/Kolkata")  # IST

bot = Bot(token=API_TOKEN)

# === ALERT SETTINGS ===
DAILY_ALERT_TIMES = [dtime(8, 0), dtime(17, 0)]  # 8:00 AM and 5:00 PM IST

GANN_LEVELS = {
    "Resistance": 48920,
    "Support": 48540,
    "Key Level": 48730
}

REVERSAL_ALERTS = [
    {
        "time": dtime(11, 20),
        "aspect": "Moon trine Jupiter",
        "note": "Watch for directional change."
    }
]

# === MESSAGE GENERATORS ===
def gann_levels_msg():
    return (
        "GANN LEVELS ALERT\n"
        f"• Resistance: {GANN_LEVELS['Resistance']}\n"
        f"• Support: {GANN_LEVELS['Support']}\n"
        f"• Key Level: {GANN_LEVELS['Key Level']}\n"
        "Based on 1927 cycle projection."
    )

def reversal_msg(event):
    return (
        "REVERSAL TIME ALERT\n"
        f"Next critical window: {event['time'].strftime('%I:%M %p')} IST\n"
        f"Aspect: {event['aspect']}\n"
        f"{event['note']}"
    )

# === ALERT DISPATCHER ===
async def send_alerts():
    while True:
        now = datetime.now(TIMEZONE)
        current_time = now.time().replace(second=0, microsecond=0)

        # Daily alerts
        if current_time in DAILY_ALERT_TIMES:
            await bot.send_message(chat_id=CHAT_ID, text=gann_levels_msg())
            for event in REVERSAL_ALERTS:
                await bot.send_message(chat_id=CHAT_ID, text=reversal_msg(event))

            await asyncio.sleep(60)  # Avoid re-sending within the same minute

        # Reversal alerts if time matches
        for event in REVERSAL_ALERTS:
            if current_time == event["time"]:
                await bot.send_message(chat_id=CHAT_ID, text=reversal_msg(event))
                await asyncio.sleep(60)

        await asyncio.sleep(20)

# === MAIN ENTRY ===
async def main():
    print("Bot started and monitoring Phase 2 alerts 24/7 (IST)...")
    await send_alerts()

if __name__ == "__main__":
    asyncio.run(main())
