import asyncio
import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("bot")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents, owner_id=OWNER_ID, help_command=None)

@bot.check
async def globally_restrict_to_owner(ctx):
    """ensure that only the bot owner can use ANY command."""
    if ctx.author.id != bot.owner_id:
        return False
    return True

@bot.event
async def on_ready():
    log.info(f"logged in as {bot.user} (ID: {bot.user.id})")
    log.info(f"owner ID: {bot.owner_id}")
    log.info(f"loaded {len(bot.cogs)} categories from cmds.py")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | !help")
    )

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.NotOwner):
        await ctx.send("this command is restricted to the bot owner.", delete_after=5)
        return
    log.error(f"command error from {ctx.author}: {error}")
    await ctx.send(f"error: {error}", delete_after=10)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    log.info(f"Received message: '{message.content}' from {message.author.name} (Length: {len(message.content)})")
    await bot.process_commands(message)

async def main():
    try:
        await bot.load_extension("cmds")
        log.info("successfully loaded master cmds.py file")
    except Exception as e:
        log.error(f"failed to load cmds.py: {e}")
    
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())
