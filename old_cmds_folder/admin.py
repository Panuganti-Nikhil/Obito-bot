import discord
from discord.ext import commands
import os
import sys
import subprocess
import textwrap
import io
import contextlib
import asyncio

class Admin(commands.Cog, name="admin"):
    """administrative commands for bot management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def loadcog(self, ctx: commands.Context, *, cog: str):
        """load a command module."""
        try:
            await self.bot.load_extension(f"cmds.{cog}")
            await ctx.send(f"loaded `{cog}`.")
        except Exception as e:
            await ctx.send(f"failed: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unloadcog(self, ctx: commands.Context, *, cog: str):
        """unload a command module."""
        try:
            await self.bot.unload_extension(f"cmds.{cog}")
            await ctx.send(f"unloaded `{cog}`.")
        except Exception as e:
            await ctx.send(f"failed: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reloadcog(self, ctx: commands.Context, *, cog: str):
        """reload a command module."""
        try:
            await self.bot.reload_extension(f"cmds.{cog}")
            await ctx.send(f"reloaded `{cog}`.")
        except Exception as e:
            await ctx.send(f"failed: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def listcogs(self, ctx: commands.Context):
        """list all loaded cogs."""
        cogs = [c for c in self.bot.cogs]
        await ctx.send("```\n" + "\n".join(cogs) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context):
        """shut down the bot."""
        await ctx.send("shutting down.")
        await self.bot.close()

    @commands.command(hidden=True, name="exec")
    @commands.is_owner()
    async def execute_code(self, ctx: commands.Context, *, code: str):
        """execute arbitrary python code. returns stdout."""
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "discord": discord,
            "commands": commands,
            "os": os,
            "sys": sys,
        }
        code = textwrap.dedent(code).strip()
        if code.startswith("```") and code.endswith("```"):
            code = "\n".join(code.split("\n")[1:-1])
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(f"async def _exec():\n    {code}\n", env)
                await env["_exec"]()
            result = stdout.getvalue()
        except Exception as e:
            result = f"error: {e}"
        if len(result) > 1900:
            result = result[:1900] + "\n...truncated"
        await ctx.send(f"```py\n{result}\n```" if result else "```\n[no output]\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shell(self, ctx: commands.Context, *, command: str):
        """execute a shell command and return the output."""
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            output = (stdout + stderr).decode("utf-8", errors="replace")
            if len(output) > 1900:
                output = output[:1900] + "\n...truncated"
            await ctx.send(f"```\n{output}\n```" if output else "```\n[no output]\n```")
        except Exception as e:
            await ctx.send(f"error: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def guilds(self, ctx: commands.Context):
        """list all guilds the bot is in."""
        g_list = [f"{g.name} ({g.id}) - {g.member_count} members" for g in self.bot.guilds]
        chunks = [g_list[i:i+20] for i in range(0, len(g_list), 20)]
        for chunk in chunks:
            await ctx.send("```\n" + "\n".join(chunk) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def leaveguild(self, ctx: commands.Context, guild_id: int):
        """leave a guild by id."""
        guild = self.bot.get_guild(guild_id)
        if guild:
            await guild.leave()
            await ctx.send(f"left guild: {guild.name}")
        else:
            await ctx.send("guild not found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dmall(self, ctx: commands.Context, *, message: str):
        """dm all mutual guild members. use with caution."""
        count = 0
        seen = set()
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.id == self.bot.user.id or member.id in seen:
                    continue
                seen.add(member.id)
                try:
                    await member.send(message)
                    count += 1
                    await asyncio.sleep(1.5)
                except:
                    pass
        await ctx.send(f"messaged {count} unique users.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def setstatus(self, ctx: commands.Context, status_type: str, *, text: str):
        """set bot status. types: play, watch, listen, stream."""
        types = {
            "play": discord.ActivityType.playing,
            "watch": discord.ActivityType.watching,
            "listen": discord.ActivityType.listening,
            "stream": discord.ActivityType.streaming,
        }
        act_type = types.get(status_type.lower(), discord.ActivityType.playing)
        await self.bot.change_presence(activity=discord.Activity(type=act_type, name=text))
        await ctx.send("status updated.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def setavatar(self, ctx: commands.Context):
        """set bot avatar from attached image."""
        if not ctx.message.attachments:
            return await ctx.send("attach an image.")
        attachment = ctx.message.attachments[0]
        img_bytes = await attachment.read()
        await self.bot.user.edit(avatar=img_bytes)
        await ctx.send("avatar updated.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def setname(self, ctx: commands.Context, *, name: str):
        """change the bot's username."""
        await self.bot.user.edit(username=name)
        await ctx.send(f"username changed to {name}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
