from telethon import TelegramClient, events
from telethon.tl.types import User


async def setup(client: TelegramClient):
    @client.on(events.NewMessage(pattern=r"\.info$", outgoing=True))
    async def info_cmd(event):
        user = await (await event.get_reply_message()).get_sender() if event.is_reply else await event.get_sender()

        if not isinstance(user, User):
            await event.edit("это не юзер")
            return

        name = user.first_name or ""
        if user.last_name:
            name += f" {user.last_name}"

        lines = [
            f"**{name}**",
            f"id: `{user.id}`",
            f"юзернейм: @{user.username}" if user.username else "юзернейм: нет",
            f"premium: {'да' if user.premium else 'нет'}",
            f"бот: {'да' if user.bot else 'нет'}",
            f"verified: {'да' if user.verified else 'нет'}",
        ]

        await event.edit("\n".join(lines))