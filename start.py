import asyncio
from src.bot import client
from src.inlinebot.bot import bot, dp

async def main():
    await client.start()
    await asyncio.gather(
        client.run_until_disconnected(), 
        dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())