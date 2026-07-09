from telethon import TelegramClient, events


async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"\.id$", outgoing=True))
    async def id_cmd(event):
        lines = [f"чат: `{event.chat_id}`"]

        if event.is_reply:
            reply = await event.get_reply_message()
            sender = await reply.get_sender()
            lines.append(f"юзер: `{sender.id}`")
            lines.append(f"сообщение: `{reply.id}`")
        else:
            me = await client.get_me()
            lines.append(f"юзер: `{me.id}`")

        await event.edit("\n".join(lines))