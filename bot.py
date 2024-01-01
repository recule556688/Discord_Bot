import discord
import os
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
import datetime

# Load .env file
load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def is_owner():
    def predicate(interaction: discord.Interaction):
        if interaction.user.id == interaction.guild.owner.id:
            return True

    return app_commands.check(predicate)


@bot.tree.command(
    guild=discord.Object(id=1190690413598744577),
    name="ping",
    description="Returns the bot's latency",
)
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong! {round(bot.latency * 1000)}ms", ephemeral=True
    )


@bot.tree.command(
    guild=discord.Object(id=1190690413598744577),
    name="owner",
    description="this command is only for the owner of the server",
)
@is_owner()
async def owner_slash(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Hello, {interaction.user.mention} (:", ephemeral=True
    )


# Create a global variable to store the user, message, and time
scheduled_message = {"user": None, "message": "", "time": ""}


@tasks.loop(seconds=60)  # Check every minute
async def check_time():
    global scheduled_message
    if scheduled_message["user"] is not None:
        # Get the current date and time
        now = datetime.datetime.now()
        # Get the scheduled date and time
        scheduled_time = datetime.datetime.strptime(
            scheduled_message["time"], "%Y-%m-%d %H:%M"
        )
        # Check if the current date and time match or are later than the scheduled date and time
        if now >= scheduled_time:
            try:
                await scheduled_message["user"].send(scheduled_message["message"])
                print(f"Successfully sent message to {scheduled_message['user'].name}.")
                # Reset the scheduled message
                scheduled_message = {"user": None, "message": "", "time": ""}
            except discord.Forbidden:
                print(
                    f"Failed to send a DM to {scheduled_message['user'].name}. They might have DMs disabled or the bot doesn't share a server with them."
                )


@bot.tree.command(
    guild=discord.Object(id=1190690413598744577),
    name="dm",
    description="Send a DM to a user",
)
async def dm_slash(
    interaction: discord.Interaction,
    user: discord.User,
    times: int,
    message: str,
    time: str = None,
):
    if time is not None:
        # Check if the time string contains a date
        if " " not in time:
            # Prepend today's date to the time
            today = datetime.date.today().strftime("%Y-%m-%d")
            time = f"{today} {time}"
        # Schedule the message
        global scheduled_message
        scheduled_message["user"] = user
        scheduled_message["message"] = message
        scheduled_message["time"] = time
        await interaction.response.send_message(
            f"Message to {user.name} scheduled for {time}.", ephemeral=True
        )
    else:
        # Send the message immediately
        for _ in range(times):
            try:
                await user.send(message)
            except discord.Forbidden:
                await interaction.response.send_message(
                    f"Failed to send a DM to {user.name}. They might have DMs disabled or the bot doesn't share a server with them.",
                    ephemeral=True,
                )
                return
        await interaction.response.send_message(
            f"Successfully sent {times} message(s) to {user.name}, at {scheduled_message}.",
            ephemeral=True,
        )


@bot.tree.command(
    guild=discord.Object(id=1190690413598744577),
    name="cancel_dm",
    description="Cancel a scheduled DM",
)
async def cancel_dm_slash(interaction: discord.Interaction):
    global scheduled_message
    if scheduled_message["user"] is not None:
        # Reset the scheduled message
        scheduled_message = {"user": None, "message": "", "time": ""}
        await interaction.response.send_message(
            "Scheduled message cancelled.", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "No message is currently scheduled.", ephemeral=True
        )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print(f"{bot.user.name}_BOT is ready to go !")
    check_time.start()

    try:
        synced = await bot.tree.sync(guild=discord.Object(id=1190690413598744577))
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


# Use the bot token from .env file
bot_token = os.getenv("BOT_TOKEN")
if bot_token is None:
    print("Bot token is not set in the environment variables.")
else:
    bot.run(bot_token)
