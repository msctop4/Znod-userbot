from telethon import events, TelegramClient
from telethon.tl import types
import random

async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"\.spamgeo(?:\s+(\d+))?", outgoing=True))
    async def spamgeo_cmd(event):
        try:
            count = int(event.pattern_match.group(1)) if event.pattern_match.group(1) else 5
            for i in range(count):
                lat = random.uniform(-85, 85)
                lon = random.uniform(-180, 180)
                geo = types.InputMediaGeoPoint(
                    types.InputGeoPoint(lat=lat, long=lon)
                )
                await event.respond(file=geo)
            await event.delete()
        except Exception as e:
            await event.edit(f"Ошибка: {str(e)}")