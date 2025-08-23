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

async def scrape_channel(channel_name):
    try:
        async with TelegramClient("anon", api_id, api_hash) as client:
            print(f"⏳ Scraping channel: {channel_name}")
            messages = []

            # Date-based partition
            date_str = datetime.now().strftime("%Y-%m-%d")
            out_dir = f"../data/raw/telegram_messages/{date_str}/{channel_name}"
            media_dir = f"{out_dir}/media"
            os.makedirs(out_dir, exist_ok=True)
            os.makedirs(media_dir, exist_ok=True)

            async for msg in client.iter_messages(channel_name, limit=100):
                msg_dict = msg.to_dict()

                # If the message has a photo or document, download it
                if msg.photo or msg.document:
                    try:
                        file_path = await msg.download_media(file=media_dir)
                        msg_dict["downloaded_media_path"] = file_path
                    except Exception as e:
                        print(f"⚠️ Could not download media from {channel_name}: {e}")

                messages.append(msg_dict)

            print(f"📌 Collected {len(messages)} messages from {channel_name}")

            # Save messages.json
            out_file = f"{out_dir}/{channel_name}_messages.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2, default=str)

            print(f"✅ Saved {len(messages)} messages + media to {out_file}")
    except Exception as e:
        print(f"❌ Error scraping {channel_name}: {e}")

async def main():
    for channel in CHANNELS:
        await scrape_channel(channel)

if __name__ == "__main__":
    asyncio.run(main())
















# from telethon import TelegramClient
# from dotenv import load_dotenv
# import os, json
# import asyncio
# from datetime import datetime


# load_dotenv()


# api_id = os.getenv("TELEGRAM_API_ID")
# api_hash = os.getenv("TELEGRAM_API_HASH")

# CHANNELS = [
#     "CheMed123",
#     "lobelia4cosmetics",
#     "tikvahpharma"
# ]

# #client = TelegramClient("anon", api_id, api_hash)
# async def scrape_channel(channel_name):
#     try:
#         async with TelegramClient("anon", api_id, api_hash) as client:
#             print(f"⏳ Scraping channel: {channel_name}")
#             messages = []



#             async for msg in client.iter_messages(channel_name, limit=100):
#                 messages.append(msg.to_dict())

#             print(f"📌 Collected {len(messages)} messages from {channel_name}")

#             # Date-based partition
#             date_str = datetime.now().strftime("%Y-%m-%d")
#             out_dir = f"../data/raw/telegram_messages/{date_str}/{channel_name}"
#             os.makedirs(out_dir, exist_ok=True)
            
#             out_file = f"{out_dir}/messages.json"
#             with open(out_file, "w", encoding="utf-8") as f:
#                 json.dump(messages, f, ensure_ascii=False, indent=2, default=str)
            
#             print(f"✅ Saved {len(messages)} messages to {out_file}")
#     except Exception as e:
#         print(f"❌ Error scraping {channel_name}: {e}")

# async def main():
#     for channel in CHANNELS:
#         await scrape_channel(channel)

# if __name__ == "__main__":
#     asyncio.run(main())
