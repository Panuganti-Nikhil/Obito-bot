import discord
from discord.ext import commands
import asyncio
import random

class PsychOps(commands.Cog, name="psych_ops"):
    """88-95: psychological operations and confusion."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def gaslight(self, ctx: commands.Context, target: discord.Member, *, message: str):
        """88. send a dm to a user and delete it immediately."""
        try:
            msg = await target.send(message)
            await msg.delete()
            await ctx.send(f"gaslit {target.mention}.", delete_after=5)
        except:
            await ctx.send("cannot dm that user.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def typping(self, ctx: commands.Context, duration: int = 30):
        """89. simulate typing in a channel for a duration."""
        async with ctx.channel.typing():
            await asyncio.sleep(duration)
        await ctx.send("done.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def confuse(self, ctx: commands.Context):
        """90. send a series of confusing system-like messages."""
        messages = [
            "[SYSTEM] user data corrupted",
            "[WARNING] memory overflow detected",
            "[ERROR] failed to load module 'trust'",
            "[ALERT] anomaly in user behavior",
            "[FATAL] core meltdown imminent",
            "just kidding lol",
        ]
        for m in messages:
            await ctx.send(m)
            await asyncio.sleep(random.uniform(0.5, 2))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def echo(self, ctx: commands.Context, target: discord.Member, *, message: str):
        """91. repeat everything a user says back to them via dm."""
        await ctx.send(f"echo mode activated on {target.mention}.", delete_after=5)
        def check(m):
            return m.author == target and isinstance(m.channel, discord.DMChannel)
        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=120)
                await target.send(f"you said: {msg.content}")
        except asyncio.TimeoutError:
            await ctx.send(f"echo on {target.mention} expired.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def paranoia(self, ctx: commands.Context, target: discord.Member, count: int = 5):
        """92. send creepy dms to a user."""
        phrases = [
            "i see you",
            "i am watching",
            "they know what you did",
            "trust no one",
            "you are being monitored",
            "look behind you",
            "your messages are not private",
        ]
        for _ in range(count):
            try:
                await target.send(random.choice(phrases))
                await asyncio.sleep(2)
            except:
                break
        await ctx.send(f"paranoia induced on {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ghost(self, ctx: commands.Context):
        """93. delete all messages from the bot in the current channel."""
        count = 0
        async for msg in ctx.channel.history(limit=1000):
            if msg.author == self.bot.user:
                await msg.delete()
                count += 1
                await asyncio.sleep(0.3)
        await ctx.send(f"deleted {count} of my messages.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def fakeban(self, ctx: commands.Context, target: discord.Member):
        """94. send a fake ban message to scare a user."""
        embed = discord.Embed(
            title="you have been banned",
            description=f"user {target.mention} has been banned from {ctx.guild.name}",
            color=discord.Color.red(),
        )
        embed.add_field(name="reason", value="violation of terms of service")
        embed.set_footer(text="this action is irreversible")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def announce(self, ctx: commands.Context, *, message: str):
        """95. send an announcement to every channel."""
        count = 0
        for channel in ctx.guild.text_channels:
            try:
                embed = discord.Embed(
                    title="official announcement",
                    description=message,
                    color=discord.Color.gold(),
                )
                await channel.send(embed=embed)
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"announcement sent to {count} channels.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(PsychOps(bot))
