from telethon import events, TelegramClient
import os

async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"\.download", outgoing=True))
    async def download_cmd(event):
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            await event.edit("ответь на фото или видео")
            return
        if not getattr(reply.media, 'ttl_seconds', 0):
            await event.edit("это не одноразовое медиа")
            return
        try:
            path = await reply.download_media()
            if path:
                await client.send_file('me', path, caption="скачано из одноразового")
                os.remove(path)
            else:
                await event.edit("не удалось скачать")
        except Exception as e:
            await event.edit(f"Ошибка: {str(e)}")