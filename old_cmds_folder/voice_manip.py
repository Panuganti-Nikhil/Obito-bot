import discord
from discord.ext import commands
import asyncio

class VoiceManip(commands.Cog, name="voice_manip"):
    """51-57: voice channel manipulation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcmove(self, ctx: commands.Context, target: discord.Member, channel: discord.VoiceChannel):
        """51. force move a member to a different voice channel."""
        await target.move_to(channel)
        await ctx.send(f"moved {target.mention} to {channel.name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vckick(self, ctx: commands.Context, target: discord.Member):
        """52. disconnect a member from voice."""
        await target.move_to(None)
        await ctx.send(f"disconnected {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcdisconnectall(self, ctx: commands.Context):
        """53. disconnect all members from all voice channels."""
        count = 0
        for vc in ctx.guild.voice_channels:
            for member in vc.members:
                try:
                    await member.move_to(None)
                    count += 1
                    await asyncio.sleep(0.2)
                except:
                    pass
        await ctx.send(f"disconnected {count} members.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcmuteall(self, ctx: commands.Context):
        """54. mute all members in voice."""
        count = 0
        for vc in ctx.guild.voice_channels:
            for member in vc.members:
                try:
                    await member.edit(mute=True)
                    count += 1
                    await asyncio.sleep(0.1)
                except:
                    pass
        await ctx.send(f"muted {count} members.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcdeafenall(self, ctx: commands.Context):
        """55. deafen all members in voice."""
        count = 0
        for vc in ctx.guild.voice_channels:
            for member in vc.members:
                try:
                    await member.edit(deafen=True)
                    count += 1
                    await asyncio.sleep(0.1)
                except:
                    pass
        await ctx.send(f"deafened {count} members.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcspam(self, ctx: commands.Context, count: int = 10):
        """56. create and delete voice channels rapidly."""
        for i in range(count):
            vc = await ctx.guild.create_voice_channel(f"spam-vc-{i}")
            await vc.delete()
        await ctx.send(f"vc spam cycle complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vclimit(self, ctx: commands.Context, channel: discord.VoiceChannel, limit: int):
        """57. set user limit on a voice channel."""
        await channel.edit(user_limit=limit)
        await ctx.send(f"set {channel.name} limit to {limit}.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceManip(bot))
