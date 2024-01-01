import discord
from discord import Interaction
from discord.ext import commands
from dotenv import load_dotenv
import os
from discord_slash import SlashCommand, SlashContext

# Load .env file
load_dotenv()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print(f"{bot.user.name} is ready to go !")


@bot.command()
async def send_dm(ctx, user: discord.User, times: int, *, message):
    for _ in range(times):
        try:
            await user.send(message)
        except discord.Forbidden:
            await ctx.send(
                f"Failed to send a DM to {user.name}. They might have DMs disabled or the bot doesn't share a server with them."
            )
            return
    await ctx.message.delete()
    await ctx.send(f"Successfully sent {times} message(s) to {user.name}.")


# @bot.tree.command(name="ping", description="Pong!")
# async def ping(Interaction: Interaction):
#     await Interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command(name="ping", help="Returns the bot's latency")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


# Use the bot token from .env file
bot_token = os.getenv("BOT_TOKEN")
bot.run(bot_token)
