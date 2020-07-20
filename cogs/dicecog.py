from discord.ext import commands
import random


class DiceCog(commands.Cog):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.equ = [
            "e",
            "=",
            "E"
        ]
        self.less = [
            "l",
            "<",
            "L"
        ]
        self.gain = [
            ">",
            "g",
            "G"
        ]

    def Suc_Fal(self, rand, sub1):
        eflag = 0
        gflag = 0
        lflag = 0
        out = ""

        for ope in self.equ:
            if(ope in sub1):
                eflag = 1
                sub1 = sub1.replace(ope, '')
                break

        for ope in self.less:
            if(ope in sub1):
                lflag = 1
                sub1 = sub1.replace(ope, '')
                break

        for ope in self.gain:
            if(ope in sub1):
                gflag = 1
                sub1 = sub1.replace(ope, '')
                break
        try:
            bas = int(sub1)
            if lflag:
                if eflag:
                    output = (rand <= bas)
                else:
                    output = (rand < bas)
            elif gflag:
                if eflag:
                    output = (rand >= bas)
                else:
                    output = (rand > bas)
            elif eflag:
                output = (rand == bas)

            if output:
                out = str(rand) + " 成功"
            else:
                out = str(rand) + " 失敗"
        except Exception:
            out = str(rand) + " コマンドが適切じゃないよ"

        return out

    @commands.command()
    async def d100(self, ctx, *args):
        rand = random.randint(1, 100)
        okng = ""
        mes = "値:"

        if len(args) == 1:
            okng = self.Suc_Fal(rand, args[0])
        elif len(args) > 1:
            sub1 = ""
            for arg in args:
                sub1 += arg
            okng = self.Suc_Fal(rand, sub1)
        else:
            okng = str(rand)

        mes += okng

        if rand > 95:
            mes = "```cs\r" + mes + " ファンブル! (>_<) ```"
        elif rand <= 5:
            mes = "```fix\r" + mes + "( クリティカル! )```"
        else:
            mes = "```\r" + mes + "```"

        await ctx.send(mes)

    @commands.command()
    async def d20(self, ctx, *args):
        rand = random.randint(1, 20)
        okng = ""
        mes = "値:"

        if len(args) == 1:
            okng = self.Suc_Fal(rand, args[0])
        elif len(args) > 1:
            sub1 = ""
            for arg in args:
                sub1 += arg
            okng = self.Suc_Fal(rand, sub1)
        else:
            okng = str(rand)

        mes += okng

        if rand > 19:
            mes = "```cs\r" + mes + " ファンブル! (>_<) ```"
        elif rand <= 1:
            mes = "```fix\r" + mes + "( クリティカル! )```"
        else:
            mes = "```\r" + mes + "```"

        await ctx.send(mes)

    @commands.command()
    async def d(self, ctx, dice):
        pos = dice.find('d')
        sum = 0
        out = ""
        inner = "["

        try:
            num = int(dice[:pos])
            legth = int(dice[pos + 1:])
            for i in range(num):
                tmp = random.randint(1, legth)
                if tmp == legth:
                    inner += str(tmp) + "*,"
                else:
                    inner += str(tmp) + ","

                if i == (num - 1):
                    inner += ']'
                else:
                    inner += " "

                sum += tmp

            out = "```\r 合計:" + str(sum) + " " + inner + "```"
            await ctx.send(out)
        except Exception:
            await ctx.send("コマンドの引数が違うよ‼")

    async def reply(self, ctx):
        if "使い方" in ctx.content:
            if "ない" in ctx.content or "なえ" in ctx.contentor or "なく" in ctx.content:
                reply = "ふざけないで"
            else:
                begin = "```\r"
                end = "```"
                d100_exp = "/d100: 1から100までの乱数を1つ出すよ。\
                            一様分布でリアルダイスと確率分布は違うよ。\
                            今後修正していくよ\
                            optionに引数に大小比較をとれるよ。\
                            大なり小なりを使えるよ。\
                            '>10'や'g10','> 10'といった感じ\n"

                d20_exp = "/d20: 1から20までの乱数を一つだすよ。\
                           一様分布でリアルダイスとは同じはず。 \
                           後はd100と同じだよ。\n"

                dndn_exp = "/d xdy: y面ダイスをx回ふるよ。\
                            optionは今後増やしていく予定。\n"

                repo = "レポジトリはここだよ。\nhttps://github.com/hanebarla/DiceChan"
                reply = begin + d100_exp + "\n" + \
                    d20_exp + "\n" + dndn_exp + "\n" + repo + end
        else:
            reply = "何か用？"

        await ctx.channel.send(reply)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            await self.reply(message)


def setup(bot):
    bot.add_cog(DiceCog(bot))
