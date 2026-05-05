import discord
from discord.ext import commands
import asyncio

class Scraper(commands.Cog, name="scraper"):
    """user and server data scraping."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def memberlist(self, ctx: commands.Context):
        """get a list of all member ids and names."""
        members = [f"{m.id} | {m.name}" for m in ctx.guild.members]
        if not members:
            return await ctx.send("no members found.")
        chunks = [members[i:i+30] for i in range(0, len(members), 30)]
        for chunk in chunks:
            await ctx.send("```\n" + "\n".join(chunk) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def scrapeavatar(self, ctx: commands.Context, target: discord.Member = None):
        """get all avatar urls for a user."""
        target = target or ctx.author
        urls = []
        if target.avatar:
            urls.append(f"standard: {target.avatar.url}")
        if target.display_avatar:
            urls.append(f"display: {target.display_avatar.url}")
        if target.guild_avatar:
            urls.append(f"guild: {target.guild_avatar.url}")
        await ctx.send("\n".join(urls) or "no avatars.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def scrapestatus(self, ctx: commands.Context):
        """scrape online status of all members."""
        statuses = {"online": [], "idle": [], "dnd": [], "offline": []}
        for m in ctx.guild.members:
            statuses[str(m.status)].append(m.name)
        msg = []
        for s, names in statuses.items():
            if names:
                msg.append(f"{s}: {', '.join(names[:10])}{'...' if len(names)>10 else ''}")
        await ctx.send("\n".join(msg))


async def setup(bot: commands.Bot):
    await bot.add_cog(Scraper(bot))
