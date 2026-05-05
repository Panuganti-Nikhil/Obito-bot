import discord
from discord.ext import commands
import asyncio
import datetime
from collections import Counter

class ServerAnalyzer(commands.Cog, name="server_analyzer"):
    """41-50: deep server analysis and statistics."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def activitymap(self, ctx: commands.Context):
        """42. generate an activity heatmap of channel usage."""
        data = {}
        for channel in ctx.guild.text_channels:
            try:
                count = 0
                async for _ in channel.history(limit=500):
                    count += 1
                data[channel.name] = count
            except:
                data[channel.name] = 0
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        result = [f"{name}: {count} msgs" for name, count in sorted_data]
        await ctx.send("**channel activity:**\n```\n" + "\n".join(result[:15]) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def topchatters(self, ctx: commands.Context, limit: int = 100):
        """43. find the most active users in recent history."""
        counter = Counter()
        for channel in ctx.guild.text_channels[:5]:
            try:
                async for msg in channel.history(limit=limit):
                    counter[str(msg.author)] += 1
            except:
                continue
        result = [f"{name}: {count}" for name, count in counter.most_common(20)]
        await ctx.send("**top chatters:**\n```\n" + "\n".join(result) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def mostusedwords(self, ctx: commands.Context, limit: int = 500):
        """44. find the most commonly used words."""
        counter = Counter()
        stopwords = {"the", "a", "an", "is", "in", "it", "of", "to", "and", "that", "for", "on", "with", "as", "this", "was", "be", "at", "by", "or", "not"}
        for channel in ctx.guild.text_channels[:5]:
            try:
                async for msg in channel.history(limit=limit):
                    words = msg.content.lower().split()
                    for word in words:
                        clean = ''.join(c for c in word if c.isalpha())
                        if clean and len(clean) > 3 and clean not in stopwords:
                            counter[clean] += 1
            except:
                continue
        result = [f"{word}: {count}" for word, count in counter.most_common(30)]
        await ctx.send("**most used words:**\n```\n" + "\n".join(result) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def joinorder(self, ctx: commands.Context):
        """45. list members in order of join date."""
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at or datetime.datetime.min)
        result = [f"{i+1}. {m.name} - {m.joined_at.strftime('%Y-%m-%d') if m.joined_at else 'unknown'}" for i, m in enumerate(members[:30])]
        await ctx.send("**join order:**\n```\n" + "\n".join(result) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rolebreakdown(self, ctx: commands.Context):
        """46. see how many members have each role."""
        result = []
        for role in ctx.guild.roles:
            if role.is_default():
                continue
            result.append(f"{role.name}: {len(role.members)}")
        await ctx.send("**role breakdown:**\n```\n" + "\n".join(result[:30]) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def inactive(self, ctx: commands.Context, days: int = 30):
        """47. find members who have not sent a message in n days."""
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
        active = set()
        for channel in ctx.guild.text_channels:
            try:
                async for msg in channel.history(after=cutoff, limit=50):
                    active.add(msg.author.id)
            except:
                continue
        inactive_members = [m for m in ctx.guild.members if m.id not in active and not m.bot]
        result = [f"{m.name} (joined: {m.joined_at.strftime('%Y-%m-%d') if m.joined_at else 'unknown'})" for m in inactive_members[:30]]
        await ctx.send(f"**inactive members ({days} days):**\n```\n" + "\n".join(result) + "\n```" if result else "everyone is active.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def boosters(self, ctx: commands.Context):
        """48. list all server boosters."""
        boosters = [m for m in ctx.guild.members if m.premium_since is not None]
        result = [f"{m.name} - boosting since {m.premium_since.strftime('%Y-%m-%d')}" for m in boosters]
        await ctx.send("**boosters:**\n```\n" + "\n".join(result) + "\n```" if result else "no boosters.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def permissionscan(self, ctx: commands.Context, target: discord.Member):
        """49. scan all permissions a user has in every channel."""
        result = []
        for channel in ctx.guild.channels:
            perms = channel.permissions_for(target)
            granted = [p for p, v in perms if v and p not in ("create_instant_invite", "change_nickname", "read_messages", "read_message_history", "view_channel")]
            if granted:
                result.append(f"#{channel.name}: {', '.join(granted[:5])}")
        await ctx.send(f"**permissions for {target.name}:**\n```\n" + "\n".join(result[:25]) + "\n```" if result else "no special permissions found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def securityaudit(self, ctx: commands.Context):
        """50. audit server security settings."""
        issues = []
        guild = ctx.guild
        if guild.default_notifications == discord.NotificationLevel.all_messages:
            issues.append("default notifications set to all messages")
        if guild.verification_level == discord.VerificationLevel.none:
            issues.append("no verification level set")
        if guild.explicit_content_filter == discord.ContentFilter.disabled:
            issues.append("explicit content filter disabled")
        for role in guild.roles:
            if role.permissions.administrator and not role.managed and role != guild.default_role:
                issues.append(f"admin role exists: {role.name} ({len(role.members)} members)")
        admin_count = sum(1 for m in guild.members if m.guild_permissions.administrator)
        issues.append(f"total administrators: {admin_count}")
        if "COMMUNITY" not in guild.features:
            issues.append("server is not a community server")
        await ctx.send("**security audit:**\n```\n" + "\n".join(issues) + "\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerAnalyzer(bot))
