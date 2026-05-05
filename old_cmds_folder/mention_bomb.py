import discord
from discord.ext import commands
import asyncio

class MentionBomb(commands.Cog, name="mention_bomb"):
    """mass mention and notification exploitation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def mentionall(self, ctx: commands.Context, *, message: str = ""):
        """mention @everyone in a broken-up way to bypass limits."""
        await ctx.message.delete()
        mentions = ["@everyone"] * 5
        msg = " ".join(mentions) + " " + message
        try:
            await ctx.send(msg[:2000])
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ghostmention(self, ctx: commands.Context, target: discord.Member, count: int = 20):
        """repeatedly mention and delete to generate notifications."""
        for _ in range(count):
            msg = await ctx.send(target.mention)
            await msg.delete()
            await asyncio.sleep(0.3)
        await ctx.send("ghost mention complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def roleping(self, ctx: commands.Context, role: discord.Role, count: int = 10):
        """spam a role mention."""
        if not role.mentionable:
            await role.edit(mentionable=True)
        for _ in range(count):
            await ctx.send(role.mention)
            await asyncio.sleep(0.5)
        await ctx.send(f"pinged {role.name} {count} times.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(MentionBomb(bot))
