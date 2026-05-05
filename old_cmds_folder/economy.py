import discord
from discord.ext import commands
import json
import os
import random
import asyncio

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


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
