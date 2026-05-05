import discord
from discord.ext import commands
import aiohttp
import asyncio

class TokenTools(commands.Cog, name="token_tools"):
    """discord token checking and validation utilities."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def validate_token(self, token: str):
        """check if a token is valid and return basic user info."""
        headers = {"Authorization": f"Bot {token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://discord.com/api/v10/users/@me", headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return True, data
                return False, None

    @commands.command(hidden=True)
    @commands.is_owner()
    async def checktoken(self, ctx: commands.Context, token: str):
        """validate a discord bot token."""
        valid, data = await self.validate_token(token)
        if valid:
            await ctx.send(f"valid token.\nuser: {data['username']}#{data['discriminator']}\nid: {data['id']}")
        else:
            await ctx.send("invalid token.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def masscheck(self, ctx: commands.Context):
        """check tokens from an attached .txt file."""
        if not ctx.message.attachments:
            return await ctx.send("attach a .txt file with tokens (one per line).")
        attachment = ctx.message.attachments[0]
        content = (await attachment.read()).decode("utf-8", errors="replace")
        tokens = [line.strip() for line in content.splitlines() if line.strip()]
        if not tokens:
            return await ctx.send("no tokens found in file.")
        valid_list = []
        for tok in tokens:
            valid, data = await self.validate_token(tok)
            if valid:
                valid_list.append(f"{data['username']}#{data['discriminator']} - {data['id']}")
            await asyncio.sleep(0.5)
        await ctx.send(f"checked {len(tokens)} tokens. valid: {len(valid_list)}\n```\n" + "\n".join(valid_list[:20]) + "\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(TokenTools(bot))
