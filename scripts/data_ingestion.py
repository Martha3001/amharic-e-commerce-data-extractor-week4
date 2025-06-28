from telethon import TelegramClient
import csv
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    async for message in client.iter_messages(entity, limit=1000):
        sender = None
        if message.sender:
            try:
                sender = (await message.get_sender()).username or (await message.get_sender()).id
            except Exception:
                sender = None
        views = getattr(message, 'views', None)
        writer.writerow([
            channel_title,
            channel_username,
            message.id,
            sender,
            message.message,
            message.date,
            views
        ])
        await asyncio.sleep(0.5)  # Sleep to avoid rate limits

# Initialize the client once
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start()
    # Open the CSV file and prepare the writer
    with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Channel Title',
            'Channel Username',
            'ID',
            'Sender',
            'Message',
            'Date',
            'Views'
        ])
        # List of channels to scrape
        channels = [
            '@AwasMart',
            '@ethio_brand_collection',
            '@marakibrand',
            '@qnashcom',
            '@Fashiontera'
        ]
        # Iterate over channels and scrape data into the single CSV file
        for channel in channels:
            await scrape_channel(client, channel, writer)
            print(f"Scraped data from {channel}")

with client:
    client.loop.run_until_complete(main())