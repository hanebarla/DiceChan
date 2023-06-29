from discord.ext import commands
import random
import re


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
    async def dog(self, ctx):
        await ctx.send('わん！')

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
    async def d(self, ctx, dice="1d1", *args):
        is_d = re.search('d', dice)
        if not is_d or not dice:
            return await ctx.send("コマンドの引数が違う～")

        if dice == "1d1":
            return await ctx.send("無意味な行為だね")

        pos = is_d.start()
        dsum = 0
        out = ""
        okng = ""
        sub1 = ""
        inner = "["

        for arg in args:
            sub1 += arg

        try:
            num = int(dice[:pos])
            if num > 1000:
                raise ValueError

            legth = int(dice[pos + 1:])
            for i in range(num):
                tmp = random.randint(1, legth)
                if tmp == legth:
                    inner += str(tmp) + "*"
                elif tmp == 1:
                    inner += str(tmp) + "`"
                else:
                    inner += str(tmp)

                if i == (num - 1):
                    inner += ']'
                else:
                    inner += ", "

                dsum += tmp

                if len(sub1) > 0:
                    okng = self.Suc_Fal(dsum, sub1)
                else:
                    okng = str(dsum)

            out = "```\r 合計:" + okng + " " + inner + "```"
            await ctx.send(out)
        except ValueError:
            await ctx.send("大きすぎるよ!!")
        except Exception:
            await ctx.send("コマンドの引数が違うよ‼")


async def setup(bot):
    await bot.add_cog(DiceCog(bot))
