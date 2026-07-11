from telethon import TelegramClient, events  

async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"\.spamcheck$", outgoing=True))
    async def spamcheck_cmd(event):
        await event.edit("стучусь в @SpamBot...")
        try:
            async with client.conversation("spambot", timeout=15) as conv:
                await conv.send_message("/start")
                response = await conv.get_response()
                reply = response.text or "пустой ответ"
        except Exception as e:
            await event.edit(f"не получилось достучаться: {e}")
            return
        lower = reply.lower()
        clean_phrases = ["good news", "хорошие новости", "свободен от", "free of any", "no limits"]
        limited_phrases = ["limited", "restricted", "заблокирован", "временно ограничен", "получил ограничения"]
        if any(p in lower for p in clean_phrases):
            status = "✅ аккаунт чист"
        elif any(p in lower for p in limited_phrases):
            status = "⚠️ есть ограничения"
        else:
            status = "ℹ️ смотри ответ ниже"
        text = f"**{status}**\n\n{reply}"
        await event.edit(text)