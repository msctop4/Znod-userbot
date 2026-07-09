import asyncio
from telethon import TelegramClient, events

async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r'\.spam (\d+) (.+)', outgoing=True))
    async def spam_cmd(event):
        count = int(event.pattern_match.group(1))
        text = event.pattern_match.group(2)
        await event.delete()
        for _ in range(count):
            await event.respond(text)