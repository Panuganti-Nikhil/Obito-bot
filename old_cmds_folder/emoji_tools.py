import discord
from discord.ext import commands
import asyncio
import aiohttp
import base64
import re

class EmojiTools(commands.Cog, name="emoji_tools"):
    """66-73: emoji and sticker manipulation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleteemojis(self, ctx: commands.Context):
        """66. delete all custom emojis."""
        count = 0
        for emoji in ctx.guild.emojis:
            try:
                await emoji.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} emojis.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def renameemoji(self, ctx: commands.Context, emoji: discord.Emoji, *, name: str):
        """67. rename an emoji."""
        await emoji.edit(name=name)
        await ctx.send(f"renamed to {name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exportemoji(self, ctx: commands.Context, emoji: discord.Emoji):
        """68. export an emoji as an image file."""
        await ctx.send(emoji.url)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def emojibomb(self, ctx: commands.Context, count: int = 20):
        """69. upload many emojis from attached images."""
        if not ctx.message.attachments:
            return await ctx.send("attach images.")
        created = 0
        for i, attachment in enumerate(ctx.message.attachments[:count]):
            try:
                img = await attachment.read()
                await ctx.guild.create_custom_emoji(
                    name=f"bomb-{i}",
                    image=img,
                )
                created += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"created {created} emojis.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def emojisteal(self, ctx: commands.Context, message_id: int):
        """70. steal all emojis from a message."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            emojis = re.findall(r"<(a?):(\w+):(\d+)>", msg.content)
            stolen = 0
            for animated, name, eid in emojis:
                ext = "gif" if animated else "png"
                url = f"https://cdn.discordapp.com/emojis/{eid}.{ext}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            img = await resp.read()
                            await ctx.guild.create_custom_emoji(
                                name=name,
                                image=img,
                            )
                            stolen += 1
                            await asyncio.sleep(0.5)
            await ctx.send(f"stole {stolen} emojis.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stickerinfo(self, ctx: commands.Context):
        """71. list all stickers in the guild."""
        stickers = ctx.guild.stickers
        info = [f"{s.name} - {s.id}" for s in stickers]
        await ctx.send("\n".join(info) or "no stickers.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletestickers(self, ctx: commands.Context):
        """72. delete all stickers."""
        count = 0
        for s in ctx.guild.stickers:
            try:
                await s.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} stickers.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def emojify(self, ctx: commands.Context, *, text: str):
        """73. convert text into emoji letters."""
        mapping = {chr(i): f":regional_indicator_{chr(i)}:" for i in range(ord('a'), ord('z')+1)}
        result = " ".join(mapping.get(c.lower(), c) for c in text if c.isalpha())
        await ctx.send(result or text)


async def setup(bot: commands.Bot):
    await bot.add_cog(EmojiTools(bot))
