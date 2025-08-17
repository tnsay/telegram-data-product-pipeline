from telethon import TelegramClient
from dotenv import load_dotenv
import os, json
import asyncio
from datetime import datetime


load_dotenv()


api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

CHANNELS = [
    "CheMed123",
    "lobelia4cosmetics",
    "tikvahpharma"
]

#client = TelegramClient("anon", api_id, api_hash)
async def scrape_channel(channel_name):
    try:
        async with TelegramClient("anon", api_id, api_hash) as client:
            print(f"⏳ Scraping channel: {channel_name}")
            messages = []
            async for msg in client.iter_messages(channel_name, limit=100):
                messages.append(msg.to_dict())

            # Date-based partition
            date_str = datetime.now().strftime("%Y-%m-%d")
            out_dir = f"../data/raw/telegram_messages/{date_str}/{channel_name}"
            os.makedirs(out_dir, exist_ok=True)
            
            out_file = f"{out_dir}/messages.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Saved {len(messages)} messages to {out_file}")
    except Exception as e:
        print(f"❌ Error scraping {channel_name}: {e}")

async def main():
    for channel in CHANNELS:
        await scrape_channel(channel)

if __name__ == "__main__":
    asyncio.run(main())
