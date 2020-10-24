import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


print(discord.__version__)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Load Cogs
init_cogs = ['cogs.Roles',
             'cogs.Lionel',
             'cogs.Highlight']
for cog in init_cogs:
    bot.load_extension(cog)


@bot.event
async def on_ready():
    print("Bot lancé.")


@bot.command(name="repeat")
async def repeat(ctx, *, message):
    await ctx.send(message)


@bot.command(name="reload")
async def reload(ctx, cog):
    print(ctx.author.id)
    await bot.unload_extension(cog)
    await bot.load_extension(cog)
    await ctx.send("Cog \"%s\n reloaded!")


bot.run(TOKEN)
