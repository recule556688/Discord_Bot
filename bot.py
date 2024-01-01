import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print(f"{bot.user.name}_BOT is ready to go !")

    try:
        synced = await bot.tree.sync(guild=discord.Object(id=1190690413598744577))
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

def is_owner():
    def predicate(interaction: discord.Interaction):
        if interaction.user.id == interaction.guild.owner.id:
            return True
    return app_commands.check(predicate)

@bot.tree.command(guild=discord.Object(id=1190690413598744577), name="ping", description="Returns the bot's latency")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms", ephemeral=True)

@bot.tree.command(guild=discord.Object(id=1190690413598744577), name="owner", description="this command is only for the owner of the server")
@is_owner()
async def owner_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention} (:", ephemeral=True)

@bot.tree.command(guild=discord.Object(id=1190690413598744577), name="dm", description="Send a DM to a user")
async def dm_slash(interaction: discord.Interaction, user: discord.User, times: int, *, message: str):
    for _ in range(times):
        try:
            await user.send(message)
        except discord.Forbidden:
            await interaction.response.send_message(
                f"Failed to send a DM to {user.name}. They might have DMs disabled or the bot doesn't share a server with them.",
                ephemeral=True
            )
            return
    await interaction.response.send_message(f"Successfully sent {times} message(s) to {user.name}.", ephemeral=True)



# Use the bot token from .env file
bot_token = os.getenv("BOT_TOKEN")
if bot_token is None:
    print("Bot token is not set in the environment variables.")
else:
    bot.run(bot_token)
