import discord
from discord.ext import commands
import asyncio

class Spammer(commands.Cog, name="spammer"):
    """message spamming utilities."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def spam(self, ctx: commands.Context, count: int, *, message: str):
        """spam a message in the current channel."""
        for _ in range(count):
            await ctx.send(message)
            await asyncio.sleep(0.5)
        await ctx.send(f"spammed {count} messages.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def fastspam(self, ctx: commands.Context, count: int, *, message: str):
        """spam without delays."""
        for _ in range(count):
            await ctx.send(message)
        await ctx.send(f"fast spammed {count} messages.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dmspam(self, ctx: commands.Context, target: discord.Member, count: int, *, message: str):
        """spam a user's dms."""
        for _ in range(count):
            try:
                await target.send(message)
                await asyncio.sleep(1)
            except:
                break
        await ctx.send(f"dm spammed {target.name}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Spammer(bot))
