import discord
from discord.ext import commands
from LionelUtils import *
import json


class HighlightCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    data = {}
    add_message = None

    @commands.group(name="hl")
    async def hl(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Ouais, highlight.")

    @hl.command(name="add")
    async def add_word(self, ctx, *, word):
        print(str(ctx.channel.type))
        if str(ctx.channel.type) == "private":
            mutual_guilds = await get_mutual_guilds(self.bot, ctx.author)
            if len(mutual_guilds) > 1:
                options = {}
                for number, guild in enumerate(mutual_guilds):
                    options["%i️⃣" % (number + 1)] = guild.name
                guild_choice = await reaction_menu(self.bot, ctx, "Dans quel serveur tu veux surveiller le mot `%s` ?" % word, options)
        else:
            guild_choice = ctx.guild  # TODO Incorporer le choix de guilde dans data (en-dessous)


        # Ajouter un mot à la liste de hl words de la personne
        try:  # Si un set de hl words existe déjà
            self.data[ctx.author].add(word)
            await ctx.send("J'ai ajouté %s à ta liste de mots" % word)
        except KeyError:  # Si la personne n'a pas encore de hl words
            self.data[ctx.author] = {word}
            await ctx.send("Tu seras maintenant highlighté pour %s" % word)

        global add_message
        add_message = ctx.message

    @commands.Cog.listener()
    async def on_message(self, message):
        global add_message
        if message.author == self.bot.user or (message == add_message):  # TODO wtf
            return
        for user, words in self.data.items():
            for word in words:
                if word in message.content:
                    await user.send("Quelqu'un a dit `%s` ici : \n"
                                    " %s" % (word, message.jump_url))




def setup(bot):
    bot.add_cog(HighlightCog(bot))
