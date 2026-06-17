import discord
from discord.ext import commands
import random
import aiohttp

class Anime(commands.Cog, name="anime"):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())


    @commands.command(name="hug")
    async def _hug(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} hugs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} hugs!"

        url = f"https://nekos.best/api/v2/hug"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="kiss")
    async def _kiss(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} kisss {user.mention}!"
        else:
            msg = f"{ctx.author.mention} kisss!"

        url = f"https://nekos.best/api/v2/kiss"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="pat")
    async def _pat(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} pats {user.mention}!"
        else:
            msg = f"{ctx.author.mention} pats!"

        url = f"https://nekos.best/api/v2/pat"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="slap")
    async def _slap(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} slaps {user.mention}!"
        else:
            msg = f"{ctx.author.mention} slaps!"

        url = f"https://nekos.best/api/v2/slap"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="punch")
    async def _punch(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} punchs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} punchs!"

        url = f"https://nekos.best/api/v2/punch"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="kick")
    async def _kick(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} kicks {user.mention}!"
        else:
            msg = f"{ctx.author.mention} kicks!"

        url = f"https://nekos.best/api/v2/kick"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="bite")
    async def _bite(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} bites {user.mention}!"
        else:
            msg = f"{ctx.author.mention} bites!"

        url = f"https://nekos.best/api/v2/bite"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="tickle")
    async def _tickle(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} tickles {user.mention}!"
        else:
            msg = f"{ctx.author.mention} tickles!"

        url = f"https://nekos.best/api/v2/tickle"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="poke")
    async def _poke(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} pokes {user.mention}!"
        else:
            msg = f"{ctx.author.mention} pokes!"

        url = f"https://nekos.best/api/v2/poke"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="cuddle")
    async def _cuddle(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} cuddles {user.mention}!"
        else:
            msg = f"{ctx.author.mention} cuddles!"

        url = f"https://nekos.best/api/v2/cuddle"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="stare")
    async def _stare(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} stares {user.mention}!"
        else:
            msg = f"{ctx.author.mention} stares!"

        url = f"https://nekos.best/api/v2/stare"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="wink")
    async def _wink(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} winks {user.mention}!"
        else:
            msg = f"{ctx.author.mention} winks!"

        url = f"https://nekos.best/api/v2/wink"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="smile")
    async def _smile(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} smiles {user.mention}!"
        else:
            msg = f"{ctx.author.mention} smiles!"

        url = f"https://nekos.best/api/v2/smile"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="smug")
    async def _smug(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} smugs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} smugs!"

        url = f"https://nekos.best/api/v2/smug"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="blush")
    async def _blush(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} blushs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} blushs!"

        url = f"https://nekos.best/api/v2/blush"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="cry")
    async def _cry(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} crys {user.mention}!"
        else:
            msg = f"{ctx.author.mention} crys!"

        url = f"https://nekos.best/api/v2/cry"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="pout")
    async def _pout(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} pouts {user.mention}!"
        else:
            msg = f"{ctx.author.mention} pouts!"

        url = f"https://nekos.best/api/v2/pout"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="shrug")
    async def _shrug(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} shrugs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} shrugs!"

        url = f"https://nekos.best/api/v2/shrug"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="dance")
    async def _dance(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} dances {user.mention}!"
        else:
            msg = f"{ctx.author.mention} dances!"

        url = f"https://nekos.best/api/v2/dance"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="wave")
    async def _wave(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} waves {user.mention}!"
        else:
            msg = f"{ctx.author.mention} waves!"

        url = f"https://nekos.best/api/v2/wave"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="highfive")
    async def _highfive(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} highfives {user.mention}!"
        else:
            msg = f"{ctx.author.mention} highfives!"

        url = f"https://nekos.best/api/v2/highfive"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="handhold")
    async def _handhold(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} handholds {user.mention}!"
        else:
            msg = f"{ctx.author.mention} handholds!"

        url = f"https://nekos.best/api/v2/handhold"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="nom")
    async def _nom(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} noms {user.mention}!"
        else:
            msg = f"{ctx.author.mention} noms!"

        url = f"https://nekos.best/api/v2/nom"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="baka")
    async def _baka(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} bakas {user.mention}!"
        else:
            msg = f"{ctx.author.mention} bakas!"

        url = f"https://nekos.best/api/v2/baka"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="kill")
    async def _kill(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} kills {user.mention}!"
        else:
            msg = f"{ctx.author.mention} kills!"

        url = f"https://nekos.best/api/v2/kill"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="lick")
    async def _lick(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} licks {user.mention}!"
        else:
            msg = f"{ctx.author.mention} licks!"

        url = f"https://nekos.best/api/v2/lick"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="yeet")
    async def _yeet(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} yeets {user.mention}!"
        else:
            msg = f"{ctx.author.mention} yeets!"

        url = f"https://nekos.best/api/v2/yeet"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="bonk")
    async def _bonk(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} bonks {user.mention}!"
        else:
            msg = f"{ctx.author.mention} bonks!"

        url = f"https://nekos.best/api/v2/bonk"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="headpat")
    async def _headpat(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} headpats {user.mention}!"
        else:
            msg = f"{ctx.author.mention} headpats!"

        url = f"https://nekos.best/api/v2/headpat"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="tail")
    async def _tail(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} tails {user.mention}!"
        else:
            msg = f"{ctx.author.mention} tails!"

        url = f"https://nekos.best/api/v2/tail"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="awoo")
    async def _awoo(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} awoos {user.mention}!"
        else:
            msg = f"{ctx.author.mention} awoos!"

        url = f"https://nekos.best/api/v2/awoo"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="feed")
    async def _feed(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} feeds {user.mention}!"
        else:
            msg = f"{ctx.author.mention} feeds!"

        url = f"https://nekos.best/api/v2/feed"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="confused")
    async def _confused(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} confuseds {user.mention}!"
        else:
            msg = f"{ctx.author.mention} confuseds!"

        url = f"https://nekos.best/api/v2/confused"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="wtf")
    async def _wtf(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} wtfs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} wtfs!"

        url = f"https://nekos.best/api/v2/wtf"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="sleep")
    async def _sleep(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} sleeps {user.mention}!"
        else:
            msg = f"{ctx.author.mention} sleeps!"

        url = f"https://nekos.best/api/v2/sleep"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="run")
    async def _run(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} runs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} runs!"

        url = f"https://nekos.best/api/v2/run"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="hide")
    async def _hide(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} hides {user.mention}!"
        else:
            msg = f"{ctx.author.mention} hides!"

        url = f"https://nekos.best/api/v2/hide"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="laugh")
    async def _laugh(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} laughs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} laughs!"

        url = f"https://nekos.best/api/v2/laugh"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="greet")
    async def _greet(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} greets {user.mention}!"
        else:
            msg = f"{ctx.author.mention} greets!"

        url = f"https://nekos.best/api/v2/greet"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="bye")
    async def _bye(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} byes {user.mention}!"
        else:
            msg = f"{ctx.author.mention} byes!"

        url = f"https://nekos.best/api/v2/bye"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="glomp")
    async def _glomp(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} glomps {user.mention}!"
        else:
            msg = f"{ctx.author.mention} glomps!"

        url = f"https://nekos.best/api/v2/glomp"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="cheer")
    async def _cheer(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} cheers {user.mention}!"
        else:
            msg = f"{ctx.author.mention} cheers!"

        url = f"https://nekos.best/api/v2/cheer"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="pounce")
    async def _pounce(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} pounces {user.mention}!"
        else:
            msg = f"{ctx.author.mention} pounces!"

        url = f"https://nekos.best/api/v2/pounce"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="purr")
    async def _purr(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} purrs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} purrs!"

        url = f"https://nekos.best/api/v2/purr"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="wag")
    async def _wag(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} wags {user.mention}!"
        else:
            msg = f"{ctx.author.mention} wags!"

        url = f"https://nekos.best/api/v2/wag"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="sip")
    async def _sip(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} sips {user.mention}!"
        else:
            msg = f"{ctx.author.mention} sips!"

        url = f"https://nekos.best/api/v2/sip"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="facepalm")
    async def _facepalm(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} facepalms {user.mention}!"
        else:
            msg = f"{ctx.author.mention} facepalms!"

        url = f"https://nekos.best/api/v2/facepalm"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="sigh")
    async def _sigh(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} sighs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} sighs!"

        url = f"https://nekos.best/api/v2/sigh"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="shy")
    async def _shy(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} shys {user.mention}!"
        else:
            msg = f"{ctx.author.mention} shys!"

        url = f"https://nekos.best/api/v2/shy"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="panic")
    async def _panic(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} panics {user.mention}!"
        else:
            msg = f"{ctx.author.mention} panics!"

        url = f"https://nekos.best/api/v2/panic"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="flex")
    async def _flex(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} flexs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} flexs!"

        url = f"https://nekos.best/api/v2/flex"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="sweat")
    async def _sweat(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} sweats {user.mention}!"
        else:
            msg = f"{ctx.author.mention} sweats!"

        url = f"https://nekos.best/api/v2/sweat"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="think")
    async def _think(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} thinks {user.mention}!"
        else:
            msg = f"{ctx.author.mention} thinks!"

        url = f"https://nekos.best/api/v2/think"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="drool")
    async def _drool(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} drools {user.mention}!"
        else:
            msg = f"{ctx.author.mention} drools!"

        url = f"https://nekos.best/api/v2/drool"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="thumbsup")
    async def _thumbsup(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} thumbsups {user.mention}!"
        else:
            msg = f"{ctx.author.mention} thumbsups!"

        url = f"https://nekos.best/api/v2/thumbsup"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="nod")
    async def _nod(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} nods {user.mention}!"
        else:
            msg = f"{ctx.author.mention} nods!"

        url = f"https://nekos.best/api/v2/nod"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="nope")
    async def _nope(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} nopes {user.mention}!"
        else:
            msg = f"{ctx.author.mention} nopes!"

        url = f"https://nekos.best/api/v2/nope"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="triggered")
    async def _triggered(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} triggereds {user.mention}!"
        else:
            msg = f"{ctx.author.mention} triggereds!"

        url = f"https://nekos.best/api/v2/triggered"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="scared")
    async def _scared(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} scareds {user.mention}!"
        else:
            msg = f"{ctx.author.mention} scareds!"

        url = f"https://nekos.best/api/v2/scared"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="bored")
    async def _bored(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} boreds {user.mention}!"
        else:
            msg = f"{ctx.author.mention} boreds!"

        url = f"https://nekos.best/api/v2/bored"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="comfy")
    async def _comfy(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} comfys {user.mention}!"
        else:
            msg = f"{ctx.author.mention} comfys!"

        url = f"https://nekos.best/api/v2/comfy"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="dizzy")
    async def _dizzy(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} dizzys {user.mention}!"
        else:
            msg = f"{ctx.author.mention} dizzys!"

        url = f"https://nekos.best/api/v2/dizzy"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="nervous")
    async def _nervous(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} nervouss {user.mention}!"
        else:
            msg = f"{ctx.author.mention} nervouss!"

        url = f"https://nekos.best/api/v2/nervous"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="excited")
    async def _excited(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} exciteds {user.mention}!"
        else:
            msg = f"{ctx.author.mention} exciteds!"

        url = f"https://nekos.best/api/v2/excited"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="happy")
    async def _happy(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} happys {user.mention}!"
        else:
            msg = f"{ctx.author.mention} happys!"

        url = f"https://nekos.best/api/v2/happy"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="sad")
    async def _sad(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} sads {user.mention}!"
        else:
            msg = f"{ctx.author.mention} sads!"

        url = f"https://nekos.best/api/v2/sad"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="angry")
    async def _angry(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} angrys {user.mention}!"
        else:
            msg = f"{ctx.author.mention} angrys!"

        url = f"https://nekos.best/api/v2/angry"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="surprised")
    async def _surprised(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} surpriseds {user.mention}!"
        else:
            msg = f"{ctx.author.mention} surpriseds!"

        url = f"https://nekos.best/api/v2/surprised"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="yawn")
    async def _yawn(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} yawns {user.mention}!"
        else:
            msg = f"{ctx.author.mention} yawns!"

        url = f"https://nekos.best/api/v2/yawn"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="stretch")
    async def _stretch(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} stretchs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} stretchs!"

        url = f"https://nekos.best/api/v2/stretch"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="bop")
    async def _bop(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} bops {user.mention}!"
        else:
            msg = f"{ctx.author.mention} bops!"

        url = f"https://nekos.best/api/v2/bop"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="spin")
    async def _spin(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} spins {user.mention}!"
        else:
            msg = f"{ctx.author.mention} spins!"

        url = f"https://nekos.best/api/v2/spin"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="jump")
    async def _jump(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} jumps {user.mention}!"
        else:
            msg = f"{ctx.author.mention} jumps!"

        url = f"https://nekos.best/api/v2/jump"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="roll")
    async def _roll(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} rolls {user.mention}!"
        else:
            msg = f"{ctx.author.mention} rolls!"

        url = f"https://nekos.best/api/v2/roll"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="clap")
    async def _clap(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} claps {user.mention}!"
        else:
            msg = f"{ctx.author.mention} claps!"

        url = f"https://nekos.best/api/v2/clap"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="praise")
    async def _praise(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} praises {user.mention}!"
        else:
            msg = f"{ctx.author.mention} praises!"

        url = f"https://nekos.best/api/v2/praise"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="tease")
    async def _tease(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} teases {user.mention}!"
        else:
            msg = f"{ctx.author.mention} teases!"

        url = f"https://nekos.best/api/v2/tease"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="beg")
    async def _beg(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} begs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} begs!"

        url = f"https://nekos.best/api/v2/beg"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="protect")
    async def _protect(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} protects {user.mention}!"
        else:
            msg = f"{ctx.author.mention} protects!"

        url = f"https://nekos.best/api/v2/protect"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="comfort")
    async def _comfort(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} comforts {user.mention}!"
        else:
            msg = f"{ctx.author.mention} comforts!"

        url = f"https://nekos.best/api/v2/comfort"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="glare")
    async def _glare(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} glares {user.mention}!"
        else:
            msg = f"{ctx.author.mention} glares!"

        url = f"https://nekos.best/api/v2/glare"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="mock")
    async def _mock(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} mocks {user.mention}!"
        else:
            msg = f"{ctx.author.mention} mocks!"

        url = f"https://nekos.best/api/v2/mock"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="salute")
    async def _salute(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} salutes {user.mention}!"
        else:
            msg = f"{ctx.author.mention} salutes!"

        url = f"https://nekos.best/api/v2/salute"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="bow")
    async def _bow(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} bows {user.mention}!"
        else:
            msg = f"{ctx.author.mention} bows!"

        url = f"https://nekos.best/api/v2/bow"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="cheerup")
    async def _cheerup(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} cheerups {user.mention}!"
        else:
            msg = f"{ctx.author.mention} cheerups!"

        url = f"https://nekos.best/api/v2/cheerup"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="snuggle")
    async def _snuggle(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} snuggles {user.mention}!"
        else:
            msg = f"{ctx.author.mention} snuggles!"

        url = f"https://nekos.best/api/v2/snuggle"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="sniff")
    async def _sniff(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} sniffs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} sniffs!"

        url = f"https://nekos.best/api/v2/sniff"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="gasp")
    async def _gasp(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} gasps {user.mention}!"
        else:
            msg = f"{ctx.author.mention} gasps!"

        url = f"https://nekos.best/api/v2/gasp"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="chuckle")
    async def _chuckle(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} chuckles {user.mention}!"
        else:
            msg = f"{ctx.author.mention} chuckles!"

        url = f"https://nekos.best/api/v2/chuckle"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="giggle")
    async def _giggle(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} giggles {user.mention}!"
        else:
            msg = f"{ctx.author.mention} giggles!"

        url = f"https://nekos.best/api/v2/giggle"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="grin")
    async def _grin(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} grins {user.mention}!"
        else:
            msg = f"{ctx.author.mention} grins!"

        url = f"https://nekos.best/api/v2/grin"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="smirk")
    async def _smirk(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} smirks {user.mention}!"
        else:
            msg = f"{ctx.author.mention} smirks!"

        url = f"https://nekos.best/api/v2/smirk"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="phew")
    async def _phew(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} phews {user.mention}!"
        else:
            msg = f"{ctx.author.mention} phews!"

        url = f"https://nekos.best/api/v2/phew"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="shiver")
    async def _shiver(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} shivers {user.mention}!"
        else:
            msg = f"{ctx.author.mention} shivers!"

        url = f"https://nekos.best/api/v2/shiver"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="tremble")
    async def _tremble(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} trembles {user.mention}!"
        else:
            msg = f"{ctx.author.mention} trembles!"

        url = f"https://nekos.best/api/v2/tremble"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="faint")
    async def _faint(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} faints {user.mention}!"
        else:
            msg = f"{ctx.author.mention} faints!"

        url = f"https://nekos.best/api/v2/faint"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="sneeze")
    async def _sneeze(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} sneezes {user.mention}!"
        else:
            msg = f"{ctx.author.mention} sneezes!"

        url = f"https://nekos.best/api/v2/sneeze"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="cough")
    async def _cough(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} coughs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} coughs!"

        url = f"https://nekos.best/api/v2/cough"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="burp")
    async def _burp(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} burps {user.mention}!"
        else:
            msg = f"{ctx.author.mention} burps!"

        url = f"https://nekos.best/api/v2/burp"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="hiccup")
    async def _hiccup(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} hiccups {user.mention}!"
        else:
            msg = f"{ctx.author.mention} hiccups!"

        url = f"https://nekos.best/api/v2/hiccup"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="snore")
    async def _snore(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} snores {user.mention}!"
        else:
            msg = f"{ctx.author.mention} snores!"

        url = f"https://nekos.best/api/v2/snore"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="daydream")
    async def _daydream(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} daydreams {user.mention}!"
        else:
            msg = f"{ctx.author.mention} daydreams!"

        url = f"https://nekos.best/api/v2/daydream"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="stumble")
    async def _stumble(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} stumbles {user.mention}!"
        else:
            msg = f"{ctx.author.mention} stumbles!"

        url = f"https://nekos.best/api/v2/stumble"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="fall")
    async def _fall(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} falls {user.mention}!"
        else:
            msg = f"{ctx.author.mention} falls!"

        url = f"https://nekos.best/api/v2/fall"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="trip")
    async def _trip(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} trips {user.mention}!"
        else:
            msg = f"{ctx.author.mention} trips!"

        url = f"https://nekos.best/api/v2/trip"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="slip")
    async def _slip(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} slips {user.mention}!"
        else:
            msg = f"{ctx.author.mention} slips!"

        url = f"https://nekos.best/api/v2/slip"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="crash")
    async def _crash(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} crashs {user.mention}!"
        else:
            msg = f"{ctx.author.mention} crashs!"

        url = f"https://nekos.best/api/v2/crash"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="bump")
    async def _bump(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} bumps {user.mention}!"
        else:
            msg = f"{ctx.author.mention} bumps!"

        url = f"https://nekos.best/api/v2/bump"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)

    @commands.command(name="huggle")
    async def _huggle(self, ctx, user: discord.Member = None):
        if user:
            msg = f"{ctx.author.mention} huggles {user.mention}!"
        else:
            msg = f"{ctx.author.mention} huggles!"

        url = f"https://nekos.best/api/v2/huggle"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'results' in data and len(data['results']) > 0:
                        img_url = data['results'][0]['url']
                        embed = discord.Embed(description=msg, color=discord.Color.random())
                        embed.set_image(url=img_url)
                        await ctx.send(embed=embed)
                        return
        except:
            pass

        await ctx.send(msg)
