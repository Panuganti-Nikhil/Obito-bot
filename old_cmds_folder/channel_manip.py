import discord
from discord.ext import commands
import asyncio
import random

class ChannelManip(commands.Cog, name="channel_manip"):
    """41-50: channel manipulation and chaos."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clonechannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """41. clone a channel with a new name."""
        channel = channel or ctx.channel
        new_ch = await channel.clone(name=f"{channel.name}-clone")
        await ctx.send(f"cloned to {new_ch.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def renamechannel(self, ctx: commands.Context, channel: discord.TextChannel, *, name: str):
        """42. rename any channel."""
        await channel.edit(name=name)
        await ctx.send(f"renamed to {name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def movechannel(self, ctx: commands.Context, channel: discord.TextChannel, position: int):
        """43. move a channel to a specific position."""
        await channel.edit(position=position)
        await ctx.send(f"moved {channel.name} to position {position}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def categorybomb(self, ctx: commands.Context, count: int = 20):
        """44. create many categories filled with channels."""
        for i in range(count):
            cat = await ctx.guild.create_category(f"cat-{i}")
            for j in range(3):
                await cat.create_text_channel(f"chaos-{i}-{j}")
                await asyncio.sleep(0.1)
        await ctx.send(f"created {count} categories with channels.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def permfuck(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """45. randomize channel permissions."""
        channel = channel or ctx.channel
        perms = discord.Permissions()
        perms.update(**{k: random.choice([True, False]) for k in dir(perms) if k[0].isalpha() and not k.startswith("_")})
        overwrite = discord.PermissionOverwrite.from_pair(discord.Permissions(), perms)
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"randomized permissions on {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def swapnames(self, ctx: commands.Context):
        """46. swap channel names in pairs."""
        channels = ctx.guild.text_channels
        for i in range(0, len(channels) - 1, 2):
            n1, n2 = channels[i].name, channels[i+1].name
            await channels[i].edit(name=f"tmp-{i}")
            await channels[i+1].edit(name=n1)
            await channels[i].edit(name=n2)
            await asyncio.sleep(0.5)
        await ctx.send("swapped channel names.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reversechannels(self, ctx: commands.Context):
        """47. reverse the order of all channels."""
        ch_list = list(ctx.guild.channels)
        for i, ch in enumerate(reversed(ch_list)):
            try:
                await ch.edit(position=i)
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send("channel order reversed.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hidechannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """48. hide a channel from everyone."""
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=False)
        await ctx.send(f"hid {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unhidechannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """49. make a hidden channel visible."""
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=True)
        await ctx.send(f"revealed {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def syncperms(self, ctx: commands.Context, source: discord.TextChannel, target: discord.TextChannel):
        """50. copy permissions from one channel to another."""
        await target.edit(overwrites=source.overwrites)
        await ctx.send(f"synced permissions from {source.name} to {target.name}.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelManip(bot))
