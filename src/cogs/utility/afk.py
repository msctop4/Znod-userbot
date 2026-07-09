from datetime import datetime
from telethon import TelegramClient, events

state = {'on': False, 'reason': '', 'since': None, 'notified': set()}


async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r'\.afk(?:\s+(.+))?$', outgoing=True))
    async def afk_on(event):
        state['on'] = True
        state['reason'] = event.pattern_match.group(1) or 'без причины'
        state['since'] = datetime.now()
        state['notified'].clear()
        await event.edit(f"AFK: {state['reason']}")

    @client.on(events.NewMessage(outgoing=True))
    async def afk_off(event):
        if state['on'] and not event.raw_text.startswith('.afk'):
            state['on'] = False
            await event.respond('на связи')

    @client.on(events.NewMessage(incoming=True))
    async def afk_notify(event):
        if not state['on']:
            return
        if not (event.is_private or event.mentioned):
            return
        if event.chat_id in state['notified']:
            return
        state['notified'].add(event.chat_id)
        idle = int((datetime.now() - state['since']).total_seconds() // 60)
        await event.reply(f"AFK ({state['reason']}), ушёл {idle} мин назад")