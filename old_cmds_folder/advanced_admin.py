import discord
from discord.ext import commands
import asyncio
import datetime
import json
import os
import re

class AdvancedAdmin(commands.Cog, name="advanced_admin"):
    """1-10: advanced administrative controls."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def lockchannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """1. lock a channel by removing send permissions for everyone."""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"locked {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unlockchannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """2. unlock a previously locked channel."""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"unlocked {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def lockdown(self, ctx: commands.Context):
        """3. lockdown the entire server by locking all channels."""
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
        await ctx.send(f"locked down {count} channels.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unlockall(self, ctx: commands.Context):
        """4. unlock all channels in the server."""
        count = 0
        for channel in ctx.guild.text_channels:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            try:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send(f"unlocked {count} channels.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def slowmode(self, ctx: commands.Context, seconds: int, channel: discord.TextChannel = None):
        """5. set slowmode on a channel."""
        channel = channel or ctx.channel
        await channel.edit(slowmode_delay=seconds)
        await ctx.send(f"slowmode set to {seconds}s on {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def setnsfw(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """6. toggle a channel as nsfw."""
        channel = channel or ctx.channel
        await channel.edit(nsfw=not channel.nsfw)
        await ctx.send(f"{channel.mention} nsfw set to {not channel.nsfw}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def archive(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """7. archive a channel by removing all permissions."""
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
        await ctx.send(f"archived {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def voicemute(self, ctx: commands.Context, target: discord.Member):
        """8. server mute a member in voice."""
        await target.edit(mute=True)
        await ctx.send(f"voice muted {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def voiceunmute(self, ctx: commands.Context, target: discord.Member):
        """9. server unmute a member in voice."""
        await target.edit(mute=False)
        await ctx.send(f"voice unmuted {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def voicedeafen(self, ctx: commands.Context, target: discord.Member):
        """10. server deafen a member in voice."""
        await target.edit(deafen=True)
        await ctx.send(f"voice deafened {target.mention}.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(AdvancedAdmin(bot))
