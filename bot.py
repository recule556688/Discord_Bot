import discord
import os
import valorant
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Create bot and client with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)

# Create command tree
tree = app_commands.CommandTree(client)


# Check if the user is the owner of the server
def is_owner():
    def predicate(interaction: discord.Interaction):
        return interaction.user.id == interaction.guild.owner.id

    return app_commands.check(predicate)



# Define commands
@bot.tree.command(name="ping", description="Returns the bot's latency")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong! {round(bot.latency * 1000)}ms", ephemeral=True
    )


@bot.tree.command(
    name="owner", description="This command is only for the owner of the server"
)
@is_owner()
async def owner_slash(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Hello, {interaction.user.mention} (:", ephemeral=True
    )





@bot.tree.command(name="valorant_agent_picker", description="Pick a Valorant agent")
async def valorant_agent_picker(interaction: discord.Interaction):
    pass


# Define events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print(f"{bot.user.name}_BOT is ready to go !")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


# Run the bot
bot_token = os.getenv("BOT_TOKEN")
if bot_token is None:
    print("Bot token is not set in the environment variables.")
else:
    bot.run(bot_token)
