import discord
from discord.ext import commands
import asyncio
import re

class MessageManip(commands.Cog, name="message_manip"):
    """11-20: message content manipulation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def editmsg(self, ctx: commands.Context, message_id: int, *, new_content: str):
        """11. edit any message sent by the bot."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            if msg.author == self.bot.user:
                await msg.edit(content=new_content)
                await ctx.send("message edited.", delete_after=5)
            else:
                await ctx.send("that message was not sent by me.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def pinmsg(self, ctx: commands.Context, message_id: int):
        """12. pin any message by id."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            await msg.pin()
            await ctx.send("message pinned.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unpinmsg(self, ctx: commands.Context, message_id: int):
        """13. unpin any message by id."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            await msg.unpin()
            await ctx.send("message unpinned.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def pinspam(self, ctx: commands.Context, count: int = 20):
        """14. send and pin many messages rapidly."""
        pinned = 0
        for i in range(count):
            msg = await ctx.send(f"pin spam {i}")
            try:
                await msg.pin()
                pinned += 1
            except:
                pass
            await asyncio.sleep(0.5)
        await ctx.send(f"pinned {pinned} messages.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unpinall(self, ctx: commands.Context):
        """15. unpin all pinned messages."""
        pins = await ctx.channel.pins()
        count = 0
        for msg in pins:
            try:
                await msg.unpin()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"unpinned {count} messages.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def replaceall(self, ctx: commands.Context, old: str, new: str):
        """16. find and replace text in recent bot messages."""
        count = 0
        async for msg in ctx.channel.history(limit=100):
            if msg.author == self.bot.user and old in msg.content:
                try:
                    await msg.edit(content=msg.content.replace(old, new))
                    count += 1
                    await asyncio.sleep(0.5)
                except:
                    pass
        await ctx.send(f"replaced '{old}' with '{new}' in {count} messages.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletemsg(self, ctx: commands.Context, message_id: int):
        """17. delete a specific message by id."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            await msg.delete()
            await ctx.send("message deleted.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleteuser(self, ctx: commands.Context, target: discord.Member, limit: int = 100):
        """18. delete recent messages from a specific user."""
        count = 0
        async for msg in ctx.channel.history(limit=limit):
            if msg.author == target:
                try:
                    await msg.delete()
                    count += 1
                    await asyncio.sleep(0.3)
                except:
                    pass
        await ctx.send(f"deleted {count} messages from {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletecontains(self, ctx: commands.Context, *, keyword: str):
        """19. delete all recent messages containing a keyword."""
        count = 0
        async for msg in ctx.channel.history(limit=200):
            if keyword.lower() in msg.content.lower():
                try:
                    await msg.delete()
                    count += 1
                    await asyncio.sleep(0.3)
                except:
                    pass
        await ctx.send(f"deleted {count} messages containing '{keyword}'.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def quotemsg(self, ctx: commands.Context, message_id: int):
        """20. quote a message with an embed."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            embed = discord.Embed(
                description=msg.content or "[no text content]",
                color=msg.author.color if msg.author.color.value else discord.Color.blurple(),
                timestamp=msg.created_at,
            )
            embed.set_author(name=str(msg.author), icon_url=msg.author.display_avatar.url)
            embed.set_footer(text=f"#{msg.channel.name}")
            if msg.attachments:
                embed.set_image(url=msg.attachments[0].url)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageManip(bot))
