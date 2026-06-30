from telethon import TelegramClient, events

async def setup(client: TelegramClient):

    @client.on(events.NewMessage(pattern='.test'))
    async def test_cmd(event):
        await event.edit('Hi')
