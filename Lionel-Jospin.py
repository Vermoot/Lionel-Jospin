import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
bot = commands.Bot(command_prefix='!')

# Load Cogs
init_cogs = ['cogs.Roles',
             'cogs.Lionel']
for cog in init_cogs:
    bot.load_extension(cog)


@bot.event
async def on_ready():
    print("Bot lancé.")


@bot.command(name="repeat")
async def repeat(ctx, *, message):
    await ctx.send(message)


bot.run(TOKEN)
