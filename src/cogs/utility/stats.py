import platform
from datetime import datetime
import telethon
from telethon import TelegramClient, events

start = datetime.now()


async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r'\.stats$', outgoing=True))
    async def stats_cmd(event):
        delta = datetime.now() - start
        secs = int(delta.total_seconds())
        h, secs = divmod(secs, 3600)
        m, s = divmod(secs, 60)
        dialogs = 0
        async for _ in client.iter_dialogs():
            dialogs += 1
        cogs_loaded = sum(1 for callback, ev in client.list_event_handlers() if getattr(ev, 'pattern', None))
        lines = [
            '**статистика юзербота**',
            f"аптайм: `{h}ч {m}м {s}с`",
            f"чатов: `{dialogs}`",
            f"хендлеров: `{cogs_loaded}`",
            f"python: `{platform.python_version()}`",
            f"telethon: `{telethon.__version__}`",
        ]
        await event.edit('\n'.join(lines))