import importlib, sys
from pathlib import Path
from telethon import TelegramClient, events


async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"\.reload (\w+)", outgoing=True))
    async def reload_cmd(event):
        name = event.pattern_match.group(1)
        target = None
        for category in Path('src/cogs').iterdir():
            if not category.is_dir():
                continue
            file = category / f"{name}.py"
            if file.exists():
                target = f"src.cogs.{category.name}.{name}"
                break
        if not target:
            await event.edit(f"ког `{name}` не найден")
            return
        for callback, ev in client.list_event_handlers():
            if getattr(callback, '__module__', None) == target:
                client.remove_event_handler(callback, ev)
        try:
            module = importlib.reload(sys.modules[target]) if target in sys.modules else importlib.import_module(target)
            await module.setup(client)
        except Exception as e:
            await event.edit(f"не взлетело: {e}")
            return
        await event.edit(f"`{target}` перезагружен")