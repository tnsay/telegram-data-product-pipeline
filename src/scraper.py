from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os, json

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("anon", api_id, api_hash)

async def scrape_channel(channel_name):
    await client.start()
    messages = []
    async for msg in client.iter_messages(channel_name, limit=100):
        messages.append(msg.to_dict())
    out_dir = f"data/raw/{channel_name}"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/messages.json", "w") as f:
        json.dump(messages, f)
    await client.disconnect()
