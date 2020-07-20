import sys
from discord.ext import commands
import traceback
import random


AddCommands = ['cogs.dicecog']


class DiceChan(commands.Bot):

    def __init__(self, command_prefix="/"):
        super().__init__(command_prefix)

        for cog in AddCommands:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print("Ready")


if __name__ == '__main__':
    random.seed()
    args = sys.argv
    TOKEN = args[1]

    bot = DiceChan()
    bot.run(TOKEN)
