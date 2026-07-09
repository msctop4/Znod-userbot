from telethon import TelegramClient, events


async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r'\.help$', outgoing=True))
    async def help_cmd(event):
        seen = set()
        for callback, ev in client.list_event_handlers():
            pattern = getattr(ev, 'pattern', None)
            if not pattern or not hasattr(pattern, '__self__'):
                continue
            raw = pattern.__self__.pattern
            cmd = raw.split('(')[0].split('$')[0].strip('\\').strip()
            if cmd:
                seen.add(cmd)
        text = 'команды:\n' + ' '.join(f'`{c}`' for c in sorted(seen))
        await event.edit(text)