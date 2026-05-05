import discord
from discord.ext import commands
import asyncio
import datetime

class InviteTools(commands.Cog, name="invite_tools"):
    """58-65: invite manipulation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def createinvite(self, ctx: commands.Context, channel: discord.TextChannel = None, max_uses: int = 0):
        """58. create an invite with specified max uses."""
        channel = channel or ctx.channel
        invite = await channel.create_invite(max_uses=max_uses, max_age=0)
        await ctx.send(f"invite: {invite.url}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleteinvites(self, ctx: commands.Context):
        """59. delete all invites in the server."""
        invites = await ctx.guild.invites()
        count = 0
        for inv in invites:
            try:
                await inv.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} invites.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def inviterace(self, ctx: commands.Context):
        """60. find who joined from whose invite."""
        invites = await ctx.guild.invites()
        info = [f"{i.code} - {i.uses} uses - inviter: {i.inviter}" for i in invites]
        await ctx.send("\n".join(info) or "no invites.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vanitysnag(self, ctx: commands.Context):
        """61. display the vanity url if configured."""
        if "VANITY_URL" in ctx.guild.features:
            vanity = await ctx.guild.vanity_invite()
            await ctx.send(f"vanity: {vanity.url}")
        else:
            await ctx.send("no vanity url.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def massinvite(self, ctx: commands.Context, count: int = 10):
        """62. create multiple invites across channels."""
        urls = []
        for i, channel in enumerate(ctx.guild.text_channels[:count]):
            try:
                inv = await channel.create_invite(max_uses=0, max_age=0)
                urls.append(inv.url)
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send("\n".join(urls) or "failed.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def inviteinfo(self, ctx: commands.Context, code: str):
        """63. detailed info on an invite."""
        try:
            inv = await self.bot.fetch_invite(code)
            info = f"guild: {inv.guild.name}\nchannel: {inv.channel.name}\ninviter: {inv.inviter}\nuses: {inv.uses}\nmax uses: {inv.max_uses}\nexpires: {inv.expires_at}"
            await ctx.send(f"```\n{info}\n```")
        except Exception as e:
            await ctx.send(f"error: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def fakeinvite(self, ctx: commands.Context, guild_name: str, channel_name: str):
        """64. generate a fake-looking invite embed."""
        embed = discord.Embed(
            title=f"invite to {guild_name}",
            description=f"you have been invited to join **{guild_name}**\nchannel: #{channel_name}",
            color=discord.Color.green(),
        )
        embed.set_footer(text="accept invite")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def revokeinvite(self, ctx: commands.Context, code: str):
        """65. revoke a specific invite by code."""
        invites = await ctx.guild.invites()
        for inv in invites:
            if inv.code == code:
                await inv.delete()
                return await ctx.send(f"revoked invite {code}.", delete_after=5)
        await ctx.send("invite not found.")


async def setup(bot: commands.Bot):
    await bot.add_cog(InviteTools(bot))
