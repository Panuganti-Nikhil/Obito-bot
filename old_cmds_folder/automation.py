import discord
from discord.ext import commands, tasks
import asyncio
import json
import os
import random

AUTO_DIR = "data/automation"
os.makedirs(AUTO_DIR, exist_ok=True)

class Automation(commands.Cog, name="automation"):
    """96-100: automated sabotage and monitoring."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.spam_task = None
        self.monitor_file = os.path.join(AUTO_DIR, "monitor.json")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autospam(self, ctx: commands.Context, interval: int, *, message: str):
        """96. start automated spamming in the current channel."""
        if self.spam_task:
            return await ctx.send("auto spam already running.")
        async def spam_loop():
            while True:
                try:
                    await ctx.channel.send(message)
                except:
                    pass
                await asyncio.sleep(interval)
        self.spam_task = self.bot.loop.create_task(spam_loop())
        await ctx.send(f"auto spam started every {interval}s.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stopspam(self, ctx: commands.Context):
        """97. stop automated spamming."""
        if self.spam_task:
            self.spam_task.cancel()
            self.spam_task = None
            await ctx.send("auto spam stopped.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autodelete(self, ctx: commands.Context, target: discord.Member, delay: float = 1.0):
        """98. automatically delete messages from a specific user."""
        await ctx.send(f"autodelete enabled on {target.mention}.", delete_after=5)
        def check(m):
            return m.author == target
        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=600)
                await asyncio.sleep(delay)
                try:
                    await msg.delete()
                except:
                    pass
        except asyncio.TimeoutError:
            await ctx.send(f"autodelete on {target.mention} timed out.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def monitor(self, ctx: commands.Context, target: discord.Member):
        """99. log all activity of a specific user."""
        data = {"target": str(target), "id": target.id, "events": []}
        filepath = os.path.join(AUTO_DIR, f"monitor_{target.id}.json")
        await ctx.send(f"monitoring {target.mention}.", delete_after=5)
        def check(m):
            return m.author == target
        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=600)
                data["events"].append({
                    "time": str(msg.created_at),
                    "channel": str(msg.channel),
                    "content": msg.content,
                })
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
        except asyncio.TimeoutError:
            await ctx.send(f"monitoring on {target.mention} ended.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autorole(self, ctx: commands.Context, role: discord.Role):
        """100. assign a specific role to every new member that joins."""
        self.bot.autorole = role
        await ctx.send(f"autorole set to {role.name}.", delete_after=5)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if hasattr(self.bot, "autorole") and self.bot.autorole:
            try:
                await member.add_roles(self.bot.autorole)
            except:
                pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Automation(bot))
