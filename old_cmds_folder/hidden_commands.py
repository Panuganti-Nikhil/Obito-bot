import discord
from discord.ext import commands
import asyncio
import random
import string
import aiohttp
import os

class HiddenCommands(commands.Cog, name="hidden_commands"):
    """miscellaneous hidden exploitation commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def nickall(self, ctx: commands.Context, *, nickname: str):
        """nickname all members."""
        count = 0
        for member in ctx.guild.members:
            if member.top_role >= ctx.guild.me.top_role:
                continue
            try:
                await member.edit(nick=nickname[:32])
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"nicknamed {count} members.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def wipe(self, ctx: commands.Context, amount: int = 100):
        """bulk delete messages."""
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"deleted {amount} messages.", delete_after=3)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def embed(self, ctx: commands.Context, title: str, *, description: str):
        """send a custom embed."""
        embed = discord.Embed(title=title, description=description, color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botleave(self, ctx: commands.Context):
        """make the bot leave the current server."""
        await ctx.send("goodbye.")
        await ctx.guild.leave()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def channeltopic(self, ctx: commands.Context, *, topic: str):
        """change the current channel topic."""
        await ctx.channel.edit(topic=topic)
        await ctx.send("topic updated.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def createrole(self, ctx: commands.Context, name: str, color: str = "ff0000"):
        """create a role with specified name and hex color."""
        color_int = int(color.lstrip("#"), 16)
        role = await ctx.guild.create_role(name=name, color=discord.Color(color_int))
        await ctx.send(f"created role {role.mention}.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleterole(self, ctx: commands.Context, *, role: discord.Role):
        """delete a role."""
        await role.delete()
        await ctx.send("role deleted.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unicode(self, ctx: commands.Context, *, text: str):
        """convert text to unicode characters for bypassing filters."""
        result = []
        for char in text:
            if char.isascii() and char.isalpha():
                result.append(chr(ord(char) + 65248))
            else:
                result.append(char)
        await ctx.send("".join(result))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def zalgo(self, ctx: commands.Context, *, text: str):
        """apply zalgo text effect."""
        zalgo_chars = [
            '\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305',
            '\u0306', '\u0307', '\u0308', '\u0309', '\u030a', '\u030b',
            '\u030c', '\u030d', '\u030e', '\u030f', '\u0310', '\u0311',
            '\u0312', '\u0313', '\u0314', '\u0315', '\u031a', '\u031b',
        ]
        result = []
        for char in text:
            result.append(char)
            for _ in range(random.randint(0, 8)):
                result.append(random.choice(zalgo_chars))
        await ctx.send("".join(result))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def react(self, ctx: commands.Context, message_id: int, *emojis):
        """add reactions to a message by id."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            for emoji in emojis:
                await msg.add_reaction(emoji)
                await asyncio.sleep(0.5)
            await ctx.send("reactions added.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def button(self, ctx: commands.Context, label: str, url: str):
        """send a message with a button."""
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label=label, url=url))
        await ctx.send("click below:", view=view)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def poll(self, ctx: commands.Context, *, question: str):
        """create a poll with reactions."""
        msg = await ctx.send(f"poll: {question}")
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hidename(self, ctx: commands.Context, *, name: str):
        """rename the bot."""
        await ctx.guild.me.edit(nick=name)
        await ctx.send("bot nickname updated.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutup(self, ctx: commands.Context, target: discord.Member):
        """timeout a member."""
        try:
            await target.timeout(discord.utils.utcnow() + discord.timedelta(minutes=5))
            await ctx.send(f"timed out {target.mention} for 5 minutes.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(HiddenCommands(bot))
