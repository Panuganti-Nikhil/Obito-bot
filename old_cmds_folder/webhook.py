import discord
from discord.ext import commands
import aiohttp
import asyncio

class Webhook(commands.Cog, name="webhook"):
    """webhook manipulation tools."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def createhook(self, ctx: commands.Context, name: str = "hook"):
        """create a webhook in the current channel."""
        try:
            hook = await ctx.channel.create_webhook(name=name)
            await ctx.send(f"created webhook: {hook.url}")
        except discord.Forbidden:
            await ctx.send("missing permissions.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sendhook(self, ctx: commands.Context, webhook_url: str, *, message: str):
        """send a message via a webhook url."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            try:
                await webhook.send(message, username="spoof")
                await ctx.send("message sent.")
            except Exception as e:
                await ctx.send(f"error: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def spammhook(self, ctx: commands.Context, webhook_url: str, count: int, *, message: str):
        """spam a webhook."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            for _ in range(count):
                try:
                    await webhook.send(message)
                    await asyncio.sleep(0.5)
                except:
                    pass
        await ctx.send(f"spammed {count} messages.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletehook(self, ctx: commands.Context, webhook_url: str):
        """delete a webhook by url."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            try:
                await webhook.delete()
                await ctx.send("webhook deleted.")
            except Exception as e:
                await ctx.send(f"error: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Webhook(bot))
