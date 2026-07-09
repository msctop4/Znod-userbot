from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from telethon import TelegramClient, events

keyfile = Path('src/data/fernet.key')
keyfile.parent.mkdir(parents=True, exist_ok=True)

if not keyfile.exists():
    keyfile.write_bytes(Fernet.generate_key())

box = Fernet(keyfile.read_bytes())

async def get_text(event):
    text = event.pattern_match.group(1)
    if text:
        return text.strip()
    if event.is_reply:
        reply = await event.get_reply_message()
        return reply.raw_text
    return None

async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r'\.encrypt(?:\s+([\s\S]+))?$', outgoing=True))
    async def encrypt_cmd(event):
        text = await get_text(event)
        if not text:
            await event.edit('шифровать нечего')
            return
        token = box.encrypt(text.encode()).decode()
        await event.edit(f'`{token}`')

    @client.on(events.NewMessage(pattern=r'\.decrypt(?:\s+([\s\S]+))?$', outgoing=True))
    async def decrypt_cmd(event):
        token = await get_text(event)
        if not token:
            await event.edit('расшифровывать нечего')
            return
        try:
            text = box.decrypt(token.encode()).decode()
        except InvalidToken:
            await event.edit('токен битый или ключ не тот')
            return

        await event.edit(text)