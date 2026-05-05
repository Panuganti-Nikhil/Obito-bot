import discord
from discord.ext import commands
import asyncio

class ReactionAbuse(commands.Cog, name="reaction_abuse"):
    """21-30: reaction and emoji abuse."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reactspam(self, ctx: commands.Context, message_id: int, *emojis):
        """21. spam reactions on a message."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            for emoji in emojis:
                for _ in range(5):
                    await msg.add_reaction(emoji)
                    await asyncio.sleep(0.2)
            await ctx.send("reaction spam complete.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reactall(self, ctx: commands.Context, message_id: int):
        """22. react with all server emojis on a message."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            count = 0
            for emoji in ctx.guild.emojis[:20]:
                try:
                    await msg.add_reaction(emoji)
                    count += 1
                    await asyncio.sleep(0.3)
                except:
                    pass
            await ctx.send(f"added {count} emoji reactions.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def removereact(self, ctx: commands.Context, message_id: int, emoji: str, target: discord.Member = None):
        """23. remove a specific reaction."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            if target:
                await msg.remove_reaction(emoji, target)
            else:
                await msg.clear_reaction(emoji)
            await ctx.send("reaction removed.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clearreacts(self, ctx: commands.Context, message_id: int):
        """24. clear all reactions from a message."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            await msg.clear_reactions()
            await ctx.send("all reactions cleared.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reactusers(self, ctx: commands.Context, message_id: int, emoji: str):
        """25. see who reacted with a specific emoji."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            for reaction in msg.reactions:
                if str(reaction.emoji) == emoji:
                    users = [u.name async for u in reaction.users()]
                    await ctx.send(f"users who reacted with {emoji}: {', '.join(users[:30])}" if users else "no users.")
                    return
            await ctx.send("emoji not found on that message.")
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reactbomb(self, ctx: commands.Context, target: discord.Member, count: int = 50):
        """26. spam a user's last message with reactions."""
        async for msg in ctx.channel.history(limit=50):
            if msg.author == target:
                emojis = ["👍", "👎", "❤️", "🔥", "😂", "😮", "😢", "😡"]
                for i in range(count):
                    await msg.add_reaction(emojis[i % len(emojis)])
                    await asyncio.sleep(0.2)
                await ctx.send(f"reaction bombed {target.mention}.", delete_after=5)
                return
        await ctx.send("no recent message from that user found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def pollrig(self, ctx: commands.Context, message_id: int, emoji: str, count: int = 10):
        """27. rig a poll by adding many reactions with the specified emoji."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            for _ in range(count):
                await msg.add_reaction(emoji)
                await asyncio.sleep(0.3)
            await ctx.send(f"poll rigged with {count} {emoji} reactions.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reactchain(self, ctx: commands.Context, message_id: int, *emojis):
        """28. create a chain reaction pattern on a message."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            for emoji in emojis:
                await msg.add_reaction(emoji)
                await asyncio.sleep(0.5)
            for emoji in reversed(emojis):
                await msg.clear_reaction(emoji)
                await asyncio.sleep(0.5)
            await ctx.send("reaction chain complete.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reactioninfo(self, ctx: commands.Context, message_id: int):
        """29. get reaction statistics for a message."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            info = []
            for reaction in msg.reactions:
                info.append(f"{reaction.emoji}: {reaction.count} (me: {reaction.me})")
            await ctx.send("\n".join(info) or "no reactions.")
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def massreact(self, ctx: commands.Context, emoji: str, limit: int = 20):
        """30. add a reaction to many recent messages."""
        count = 0
        async for msg in ctx.channel.history(limit=limit):
            try:
                await msg.add_reaction(emoji)
                count += 1
                await asyncio.sleep(0.4)
            except:
                pass
        await ctx.send(f"reacted to {count} messages with {emoji}.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(ReactionAbuse(bot))
