import discord
from discord.ext import commands
import random
# from Utilities import reaction_menu



class LionelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def reaction_menu(self, ctx, question, *choices: str):
        choice_number = 1
        message_text = question + "```"
        for choice in list(choices):
            message_text += "%s️⃣ %s \n" % (choice_number, choice)
            choice_number += 1
        message_text += "```"
        message = await ctx.send(message_text)
        reaction_number = 1
        for choice in list(choices):
            await message.add_reaction("%s️⃣" % reaction_number)
            reaction_number += 1
        def check(reaction, user):
            return user == ctx.author
        reaction = await self.bot.wait_for("reaction_add", check=check, timeout=None)
        return [list(reaction)[0].emoji[0], choices[int(list(reaction)[0].emoji[0])-1]]

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

    @commands.command(name="testmenu")
    async def test_menu(self, ctx):
        choice = await self.reaction_menu(ctx, "Choisis une option :",  "La première",
                                                                        "Peut-être la deuxième",
                                                                        "Qui sait, pourquoi pas la troisième",
                                                                        "La réponse D")
        await ctx.send("Tu as choisi l'option %s : %s" % (choice[0], choice[1]))

def setup(bot):
    bot.add_cog(LionelCog(bot))
