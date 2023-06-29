import os
import discord
from discord.ext import commands
import random
import asyncio


AddCommands = [
    'cogs.dicecog',
    'cogs.expressioncog',
    'cogs.wordwolfcog'
]


class DiceChan(commands.Bot):
    def __init__(self, command_prefix="/", intents=None):
        super().__init__(command_prefix, intents=intents)

    async def load_cogs(self):
        for cog in AddCommands:
            await self.load_extension(cog)

    async def on_ready(self):
        print("Ready")


async def main(bot, token):
    await bot.load_cogs()
    await bot.start(token)


if __name__ == '__main__':
    random.seed()
    TOKEN = os.environ['DICECHAN_TOKEN']

    intents = discord.Intents.all()
    intents.typing = False

    bot = DiceChan(intents=intents)

    asyncio.run(main(bot, TOKEN))
