import discord
from discord.ext import commands
import random
import csv
import os
import asyncio


WordsCsv = os.path.join('data', 'wordwolf_odai.csv')


class WordwCog(commands.Cog):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        with open(WordsCsv, encoding="utf_8") as f:
            reader = csv.reader(f)
            self.odai = [row for row in reader]
        self.timer_on_flag = {}
        self.ww_on_flag = {}

    @commands.command()
    async def timer(self, ctx, time: float = 3.0):
        if time > 10:
            return await ctx.send("設定時間が長すぎます。最高でも2時間までしか設定できません。")
        await ctx.send("@here タイマー{}分でセットされました。".format(time))
        wait_time_m = int(time)
        wait_time_sec = int(60 * time)
        res = wait_time_sec - int(wait_time_m * 60)
        if res > 0:
            await asyncio.sleep(res)
            await ctx.send("@here 残り{}分".format(wait_time_m))
        for t in range(wait_time_m - 1):
            await asyncio.sleep(60)
            res_m = wait_time_m - 1 - t
            await ctx.send("@here 残り{}分".format(res_m))
        await asyncio.sleep(30)
        await ctx.send("@here 残り30秒")
        await asyncio.sleep(30)
        await ctx.send("@here 終了")

    @commands.group(invoke_without_command=True)
    async def ww(self, ctx):
        await ctx.send("サブコマンドや引数を指定してないか、間違っています。以下にサブコマンドを記載します。")
        wwhelper = discord.Embed(title="/ww サブコマンド",
                                 description="二つります。",
                                 color=0xadd8e6)
        wwhelper.add_field(name="begin *member",
                           value="ワードウルフを開始します。引数に参加者全員の名前を記入してください。",
                           inline=False)
        wwhelper.add_field(name="add a b",
                           value="お題を追加できます。既に存在する場合は却下されます。",
                           inline=False)
        await ctx.send(embed=wwhelper)

    @ww.command()
    async def begin(self, ctx, *participants: discord.Member, time: float = 3.0):
        self.ww_on_flag.setdefault(str(ctx.guild), False)
        if self.ww_on_flag[str(ctx.guild)] is True:
            return await ctx.send(("既に実行されています。"
                                   "身に覚えのないない場合、製作者に連絡してください。"))
        if len(self.odai) < 1:
            with open(WordsCsv, encoding="utf_8") as f:
                reader = csv.reader(f)
                self.odai = [row for row in reader]

        chosed = random.randint(0, len(self.odai))
        words = self.odai[chosed]

        unique_memb_set = set(participants)
        unique_memb_list = list(unique_memb_set)
        for par in unique_memb_list:
            if par.bot == 1:
                unique_memb_list.remove(par)

        if len(unique_memb_list) == 1:
            return await ctx.send("可哀そうに、、、一人だけだなんて、、、")
        elif len(unique_memb_list) == 0:
            return await ctx.send("botだけじゃできないけどね")

        random.shuffle(unique_memb_list)
        for index, memb in enumerate(unique_memb_list):
            if index == 0:
                await memb.send(words[0])
            else:
                await memb.send(words[1])

        self.odai.pop(chosed)

        self.ww_on_flag[str(ctx.guild)] = True
        await self.timer(ctx, time)
        await ctx.send("終了")
        self.ww_on_flag[str(ctx.guild)] = False

    @ww.command()
    async def add(self, ctx, first: str, second: str):
        await ctx.send("審議中...")
        new_words = [first, second]

        with open(WordsCsv, encoding="utf_8") as f:
            reader = csv.reader(f)
            all_words = [row for row in reader]

        for registered in all_words:
            if set(new_words) == set(registered):
                return await ctx.send("却下します")

        with open(WordsCsv, 'a', encoding="utf_8") as f:
            writer = csv.writer(f)
            writer.writerow(new_words)

        await ctx.send("追加しました！！")


def setup(bot):
    bot.add_cog(WordwCog(bot))
