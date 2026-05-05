import discord
from discord.ext import commands
import asyncio
import aiohttp
import json
import os

WEBHOOK_DIR = "data/webhooks"
os.makedirs(WEBHOOK_DIR, exist_ok=True)

class WebhookAdvanced(commands.Cog, name="webhook_advanced"):
    """1-10: advanced webhook exploitation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookall(self, ctx: commands.Context, *, name: str = "backup"):
        """1. create a webhook with the same name in every channel."""
        created = 0
        for channel in ctx.guild.text_channels:
            try:
                await channel.create_webhook(name=name)
                created += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"created {created} webhooks named '{name}'.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookinfo(self, ctx: commands.Context, webhook_url: str):
        """2. get detailed information about a webhook url."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            try:
                w = await webhook.fetch()
                info = f"name: {w.name}\nid: {w.id}\ntoken: {w.token}\nchannel: {w.channel_id}\nguild: {w.guild_id}\navatar: {w.avatar}"
                await ctx.send(f"```\n{info}\n```")
            except Exception as e:
                await ctx.send(f"error: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookavatar(self, ctx: commands.Context, webhook_url: str, *, avatar_url: str):
        """3. change a webhook's avatar."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            async with session.get(avatar_url) as resp:
                if resp.status == 200:
                    avatar_bytes = await resp.read()
                    await webhook.edit(avatar=avatar_bytes)
                    await ctx.send("webhook avatar updated.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookname(self, ctx: commands.Context, webhook_url: str, *, name: str):
        """4. change a webhook's display name."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            await webhook.edit(name=name)
            await ctx.send(f"webhook name changed to '{name}'.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookembed(self, ctx: commands.Context, webhook_url: str, title: str, *, description: str):
        """5. send an embed through a webhook."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            embed = discord.Embed(title=title, description=description, color=discord.Color.random())
            await webhook.send(embed=embed)
            await ctx.send("embed sent via webhook.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookfile(self, ctx: commands.Context, webhook_url: str):
        """6. send an attached file through a webhook."""
        if not ctx.message.attachments:
            return await ctx.send("attach a file.")
        attachment = ctx.message.attachments[0]
        file_bytes = await attachment.read()
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            await webhook.send(file=discord.File(file_bytes, filename=attachment.filename))
            await ctx.send("file sent via webhook.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookclone(self, ctx: commands.Context, source_webhook_url: str, target_channel: discord.TextChannel):
        """7. clone a webhook to a different channel."""
        async with aiohttp.ClientSession() as session:
            source = discord.Webhook.from_url(source_webhook_url, session=session)
            try:
                w = await source.fetch()
                new_hook = await target_channel.create_webhook(name=w.name, avatar=await w.avatar.read() if w.avatar else None)
                await ctx.send(f"cloned webhook to {target_channel.mention}. new url: {new_hook.url}")
            except Exception as e:
                await ctx.send(f"error: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookbroadcast(self, ctx: commands.Context, *, message: str):
        """8. send a message through every webhook in the server."""
        count = 0
        for channel in ctx.guild.text_channels:
            try:
                hooks = await channel.webhooks()
                for hook in hooks:
                    await hook.send(message)
                    count += 1
                    await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"broadcast through {count} webhooks.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hooktoken(self, ctx: commands.Context, webhook_url: str):
        """9. extract the webhook id and token from a url."""
        parts = webhook_url.split("/")
        if len(parts) >= 2:
            hook_id = parts[-2]
            hook_token = parts[-1]
            await ctx.send(f"id: {hook_id}\ntoken: {hook_token}")
        else:
            await ctx.send("invalid webhook url format.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hooksave(self, ctx: commands.Context):
        """10. save all webhook urls to a json file categorized by channel."""
        data = {}
        for channel in ctx.guild.text_channels:
            try:
                hooks = await channel.webhooks()
                if hooks:
                    data[channel.name] = [{"name": h.name, "url": h.url} for h in hooks]
            except:
                pass
        filepath = os.path.join(WEBHOOK_DIR, f"{ctx.guild.id}_hooks.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"saved webhooks from {len(data)} channels.", file=discord.File(filepath))


async def setup(bot: commands.Bot):
    await bot.add_cog(WebhookAdvanced(bot))
