import discord
from discord.ext import commands
import asyncio

class Cloner(commands.Cog, name="cloner"):
    """server cloning tools."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def cloneroles(self, ctx: commands.Context, source_guild_id: int):
        """clone roles from another server the bot is in."""
        source = self.bot.get_guild(source_guild_id)
        if not source:
            return await ctx.send("source guild not found.")
        for role in reversed(source.roles):
            if role.is_default() or role.managed:
                continue
            try:
                await ctx.guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable,
                )
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send("roles cloned.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clonechannels(self, ctx: commands.Context, source_guild_id: int):
        """clone channels from another server."""
        source = self.bot.get_guild(source_guild_id)
        if not source:
            return await ctx.send("source guild not found.")
        for category in source.categories:
            new_cat = await ctx.guild.create_category(category.name)
            for channel in category.channels:
                try:
                    await new_cat.create_text_channel(channel.name)
                    await asyncio.sleep(0.3)
                except:
                    pass
        for channel in source.channels:
            if channel.category:
                continue
            try:
                await ctx.guild.create_text_channel(channel.name)
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send("channels cloned.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Cloner(bot))
