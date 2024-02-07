import discord
from discord import app_commands
from discord.ext import commands
import command_handler

intents = discord.Intents.default()
intents.message_content = True

# 614761798473613342 - alphas
# 590129164217221121 - gulag
guilds = [discord.Object(id=614761798473613342), discord.Object(id=590129164217221121)]
guild = discord.Object(id=614761798473613342)

client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="$", intents=intents)
# tree = app_commands.CommandTree(client)


@client.tree.command(
    name="help",
    description="911",
)
async def help(interaction: discord.interactions.Interaction):
    embed = discord.Embed(
        title="911",
        color=0xD62342,
        description="""
        If you ever want me to reply to your time, while writing your time, write it in this format: **^hour:minute^**. And that's it. Just make sure you write it in 24-hour format.\n
        But before you do that, make sure you set a region for yourself. Use /change-region for that. You can change it how many ever times you want, whenever you want.\n
        If you want to see current time for all regions, use /all-time.
        Well that's all. Pretty simple.\n
        If you still dont get it, you're a retard. Have fun :thumbsup:
        """,
    )
    await interaction.response.send_message(embed=embed)


@client.tree.command(
    name="all-time",
    description="Shows the current time at all time zones",
)
async def allTime(interaction):
    await interaction.response.send_message(f"```\n{command_handler.allTime()}\n```")


@client.tree.command(
    name="change-region",
    description="Change the user's time zone region. Choose from available options.",
)
@app_commands.describe(regions="Choose a region")
@app_commands.choices(
    regions=[
        app_commands.Choice(name="Canada", value="canada"),
        app_commands.Choice(name="USA", value="us"),
        app_commands.Choice(name="UK", value="uk"),
        app_commands.Choice(name="Kuwait", value="kuwait"),
        app_commands.Choice(name="India", value="india"),
    ]
)
async def changeRegion(
    interaction: discord.Interaction, regions: discord.app_commands.Choice[str]
):
    await interaction.response.send_message(
        command_handler.changeRegion(str(interaction.user.id), str(regions.value)),
        ephemeral=True,
    )


@client.event
async def on_ready():
    await client.tree.sync(guild=guild)
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.content.count("^") >= 2:
        time = command_handler.textParser(message.content)
        output = command_handler.timeConvert(time, str(message.author.id))
        await message.channel.send(f"```\n{output}\n```")


client.run(TOKEN)
