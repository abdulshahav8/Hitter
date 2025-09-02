from telethon import TelegramClient, events
import re

# ================== CONFIG ==================
API_ID = 25777114
API_HASH = "83d41274e41d8330fc83876fb499432b"
PHONE_NUMBER = "+919908262004"

SOURCE_GROUP = -1002682944548    # Jaha se uthana hai
TARGET_GROUP = -1002882603089    # Jaha bhejna hai
# =============================================

# Regex patterns for CC extraction (covering all combos)
cc_patterns = [
    r'(\d{13,16})[| ](\d{1,2})[|/ ](\d{2,4})[| ](\d{3,4})',   # 4111111111111111|12|25|123
    r'(\d{13,16})\s+(\d{1,2})[ /](\d{2,4})\s+(\d{3,4})',       # 4111111111111111 12/25 123
]

# To avoid duplicates in one run
seen = set()

# Initialize client
client = TelegramClient("cc_forwarder", API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_GROUP))
async def handler(event):
    text = event.raw_text
    combos = []

    for pattern in cc_patterns:
        for match in re.findall(pattern, text):
            ccnum, month, year, cvv = match

            # Normalize month/year
            month = month.zfill(2)
            year = year[-2:]  # Take last 2 digits
            combo = f"/ho {ccnum}|{month}|{year}|{cvv}"

            if combo not in seen:
                seen.add(combo)
                combos.append(combo)

    # Send all extracted combos
    for combo in combos:
        await client.send_message(TARGET_GROUP, combo)
        print("Forwarded:", combo)


async def main():
    print("Starting CC Forwarder Bot...")
    await client.start(PHONE_NUMBER)
    print("Bot is now running 24/7...")

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
