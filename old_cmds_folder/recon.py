import discord
from discord.ext import commands
import asyncio

class Recon(commands.Cog, name="recon"):
    """reconnaissance and information gathering."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx: commands.Context, target: discord.Member = None):
        """get detailed information about a user."""
        target = target or ctx.author
        embed = discord.Embed(color=target.color, title=f"user info: {target}")
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="id", value=target.id)
        embed.add_field(name="display name", value=target.display_name)
        embed.add_field(name="created at", value=target.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="joined at", value=target.joined_at.strftime("%Y-%m-%d %H:%M:%S") if target.joined_at else "N/A")
        embed.add_field(name="roles", value=", ".join([r.mention for r in target.roles[1:]]) or "none")
        embed.add_field(name="bot", value=target.bot)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx: commands.Context):
        """get detailed information about the server."""
        guild = ctx.guild
        embed = discord.Embed(color=discord.Color.blurple(), title=f"server info: {guild.name}")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="id", value=guild.id)
        embed.add_field(name="owner", value=str(guild.owner))
        embed.add_field(name="created at", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="members", value=guild.member_count)
        embed.add_field(name="channels", value=len(guild.channels))
        embed.add_field(name="roles", value=len(guild.roles))
        embed.add_field(name="emojis", value=len(guild.emojis))
        embed.add_field(name="boost level", value=guild.premium_tier)
        embed.add_field(name="boost count", value=guild.premium_subscription_count)
        await ctx.send(embed=embed)

    @commands.command()
    async def roleinfo(self, ctx: commands.Context, *, role: discord.Role):
        """get information about a role."""
        embed = discord.Embed(color=role.color, title=f"role info: {role.name}")
        embed.add_field(name="id", value=role.id)
        embed.add_field(name="created at", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="position", value=role.position)
        embed.add_field(name="mentionable", value=role.mentionable)
        embed.add_field(name="hoist", value=role.hoist)
        embed.add_field(name="managed", value=role.managed)
        embed.add_field(name="permissions", value=f"`{role.permissions.value}`")
        member_count = len(role.members)
        embed.add_field(name="members", value=member_count)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Recon(bot))
