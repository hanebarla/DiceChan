import discord
import os
import json
from discord.ext import commands


ExpJson = os.path.join('data', 'sentence.json')


class ExpCog(commands.Cog):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def reply(self, ctx):
        reply = ""

        if "使い方" in ctx.content:
            if "ない" in ctx.content or "なく" in ctx.content or "なえ" in ctx.content:
                reply = "ふざけないで"
            else:
                with open(ExpJson, encoding="utf_8") as f:
                    expj = json.load(f)

                head_exp = "以下に各コマンドについての説明"
                d100_exp = expj["expression"]["/d100"]
                d20_exp = expj["expression"]["/d20"]
                d_exp = expj["expression"]["/d"]
                ww_exp = expj["expression"]["/ww"]
                other_exp = expj["expression"]["other"]
                rpj_exp = expj["expression"]["repoj"]

                helper = discord.Embed(title="About DiceChan", description=head_exp, color=0xadd8e6)
                helper.add_field(name="/d100", value=d100_exp, inline=False)
                helper.add_field(name="/d20", value=d20_exp, inline=False)
                helper.add_field(name="/d", value=d_exp, inline=False)
                helper.add_field(name="/ww", value=ww_exp, inline=False)
                helper.add_field(name="その他", value=other_exp, inline=False)
                helper.add_field(name="レポジトリ", value=rpj_exp, inline=False)
        else:
            reply = "何か用？"

        await ctx.channel.send(reply) if len(reply) > 0 else await ctx.channel.send(embed=helper)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            await self.reply(message)


async def setup(bot):
    await bot.add_cog(ExpCog(bot))
