import re
import asyncio
from telethon import TelegramClient, events

# --- Config ---
api_id = 25777114
api_hash = "83d41274e41d8330fc83876fb499432b"
phone_number = "+919908262004"

source_group = -1002682944548   # yaha se CC uthana
target_group = -1002882603089   # yaha bhejna

# --- Card Extractor Function ---
def extract_card_data(text: str):
    """
    Extract card data from messy text and return unified format:
    /ho CARD|MM|YY|CVV
    """

    # Normalize text
    clean = text.replace("\n", " ").replace(":", " ").replace("/", " ").replace("|", " ")
    nums = re.findall(r"\d{2,19}", clean)

    card, month, year, cvv = None, None, None, None

    # Detect card number (13–19 digits, usually 16)
    for n in nums:
        if 13 <= len(n) <= 19:
            card = n
            break

    # Detect expiry month
    for n in nums:
        if len(n) == 2 and 1 <= int(n) <= 12:
            month = n.zfill(2)
            break

    # Detect expiry year
    for n in nums:
        if len(n) == 2 and int(n) >= 24:  # example: 24, 25, 30
            year = n
            break
        elif len(n) == 4 and n.startswith("20"):  # example: 2027
            year = n[-2:]
            break

    # Detect CVV (3–4 digits)
    for n in nums:
        if len(n) in [3, 4] and n not in [month, year] and (card is None or n not in card):
            cvv = n
            break

    if card and month and year and cvv:
        return f"/ho {card}|{month}|{year}|{cvv}"
    return None

# --- Main Telethon Client ---
client = TelegramClient("cc_forwarder", api_id, api_hash)

@client.on(events.NewMessage(chats=source_group))
async def handler(event):
    raw_text = event.raw_text
    parsed = extract_card_data(raw_text)

    if parsed:
        await client.send_message(target_group, parsed)
        print(f"[✔] Sent: {parsed}")
    else:
        print(f"[✘] Failed to parse: {raw_text}")

async def main():
    print("🔑 Logging in...")
    await client.start(phone=phone_number)
    print("✅ Bot started. Listening for messages...")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
