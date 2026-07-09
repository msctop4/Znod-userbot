import asyncio
from telethon import TelegramClient, events

async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"\.del$", outgoing=True))
    async def del_cmd(event):
        if not event.is_reply:
            await event.edit("нужен reply")
            return
        reply = await event.get_reply_message()
        await reply.delete()
        await event.delete()

    @client.on(events.NewMessage(pattern=r"\.purge(?:\s+(\d+))?$", outgoing=True))
    async def purge_cmd(event):
        count = event.pattern_match.group(1)
        chat = await event.get_input_chat()
        if event.is_reply:
            reply = await event.get_reply_message()
            ids = [msg.id async for msg in client.iter_messages(chat, min_id=reply.id - 1, max_id=event.id)]
            ids.append(event.id)
            await client.delete_messages(chat, ids)
            return
        limit = int(count) if count else 100
        ids = [msg.id async for msg in client.iter_messages(chat, from_user='me', limit=limit, max_id=event.id)]
        deleted = len(ids)
        ids.append(event.id)
        await client.delete_messages(chat, ids)
        note = await client.send_message(chat, f"снесено {deleted} сообщений")
        await asyncio.sleep(2)
        await note.delete()