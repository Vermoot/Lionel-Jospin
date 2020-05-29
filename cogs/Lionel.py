import discord
from discord.ext import commands
import random


class LionelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="lionel")
    async def lionel(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(random.choice(["Oui oui je suis bien là.",
                                          "Oui ?",
                                          "Quoi ?",
                                          "Je suis là.",
                                          "Dis moi tout.",
                                          "Qu'est-ce que ?",
                                          "Présent !"]))

    @lionel.command(name="help")
    async def help(self, ctx):
        discord.ext.commands.HelpCommand(ctx)


def setup(bot):
    bot.add_cog(LionelCog(bot))
