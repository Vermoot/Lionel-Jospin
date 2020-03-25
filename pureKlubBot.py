import os
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
bot = commands.Bot(command_prefix='!')


def isSimilar(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio() > 0.5

@bot.event
async def on_ready():
    print("Bot lancé.")

@bot.command(name="add")
async def add(ctx, machin):
    await ctx.send("Non c'est `!role add`.")

@bot.command(name="roll")
async def add(ctx, machin):
    await ctx.send("ROLE bordel, pas roll. Fais un effort marde.")


@bot.group(name="role")
async def role(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Non là t'as merdé mon coco.")


@role.command(name="add")  # TODO gérer les presque-doublons avec la casse
async def addRole(ctx, *, roleName):
    guild = ctx.guild
    roleList = guild.roles
    for role in roleList:

# Si le rôle demandé existe (insensible à la casse)
        if roleName.lower() == role.name.lower():
            if ctx.author in role.members:
                await ctx.send("Tu as déjà le rôle %s, couillon." % role.name)
                return
            else:
                await ctx.author.add_roles(role)
                await ctx.send("Voilà %s, tu as maintenant le rôle %s ! Vous êtes %i. Je crois. Mais je suis pas fort en math." % (
                ctx.author.display_name, role.name, len(role.members)))
                return

# Si le rôle demandé ressemble à un rôle qui existe
        elif isSimilar(roleName, role.name):
            def check(m):
                return m.author == ctx.author
            await ctx.send("Est-ce que tu veux dire \"%s\" ?" % role.name)

    # Oui c'est bien ce que je voulais dire
            while True:
                answer = await bot.wait_for("message", check=check, timeout=10)
                if answer.content.lower().startswith("oui"):
                    if ctx.author in role.members:
                        await ctx.send("Tu as déjà le rôle %s, couillon." % role.name)
                        return
                    else:
                        await ctx.author.add_roles(role)
                        await ctx.send("Alors ok, tu as maintenant le rôle %s ! Vous êtes %i. Je crois. Mais je suis pas fort en math." % (
                                        role.name, len(role.members)))
                        return

        # Non c'est pas ce que je voulais dire
                elif answer.content.lower().startswith("non"):
                    await ctx.send("Alors tu veux effectivement le rôle \"%s\" ?" % roleName)
                    while True:
                        answer = await bot.wait_for("message", check=check, timeout=10)

            # Oui je veux précisément le rôle que j'ai demandé au début même s'il ressemble à un autre
                        if answer.content.lower().startswith("oui"):
                            newRole = await ctx.guild.create_role(name=roleName, mentionable=True)
                            await ctx.author.add_roles(newRole)
                            await ctx.send("Ok, tu l'auras voulu. Tu as maintenant le rôle %s. Vous êtes %i. Je crois. Mais je suis pas fort en math." % (newRole.name, len(newRole.members)))
                            return

            # Non je ne veux pas le rôle demandé au départ
                        elif answer.content.lower().startswith("non"):
                            await ctx.send("Ouais ben reviens me voir quand tu seras décidé alors hein. Merde.")
                            return
                        else:
                            await ctx.send("Oui ou non, bordel.")
                else:
                    await ctx.send("Oui ou non, bordel.")

# Si le rôle demandé ne ressemble pas à un rôle pré-existant
    newRole = await ctx.guild.create_role(name=roleName, mentionable=True)
    await ctx.author.add_roles(newRole)
    await ctx.send("Voilà %s, tu as maintenant le rôle %s ! Tu es le premier, invite tes copains!" % (
    ctx.author.display_name, newRole.name))


@role.command(name="remove")
async def remRole(ctx, *, roleName):
    guild = ctx.guild
    userRoles = ctx.author.roles
    for role in userRoles:

# Si la personne a effectivement ce rôle
        if roleName.lower() == role.name.lower():
            await ctx.author.remove_roles(role)
            if len(role.members) == 0:
                await role.delete()
                await ctx.send(
                    "Voilà %s, tu n'as maintenant plus le rôle %s. Plus personne ne l'a, d'ailleurs. Je le ferme." % (
                    ctx.author.display_name, role.name))
                return
            else:
                await ctx.send(
                    "Voilà %s, tu n'as maintenant plus le rôle %s." % (ctx.author.display_name, role.name))
                return

# Si la personne a un rôle qui ressemble
        elif isSimilar(roleName, role.name):

            def check(m):
                return m.author == ctx.author

            await ctx.send("Est-ce que tu veux dire \"%s\" ?" % role.name)
            while True:
                answer = await bot.wait_for("message", check=check, timeout=10)
    # Oui c'est bien ce que je voulais dire
                if answer.content.lower().startswith("oui"):
                    await ctx.author.remove_roles(role)
                    if len(role.members) == 0:
                        await role.delete()
                        await ctx.send(
                            "Voilà %s, tu n'as maintenant plus le rôle %s. Plus personne ne l'a, d'ailleurs. Je le ferme." % (
                            ctx.author.display_name, role.name))
                    else:
                        await ctx.send(
                            "Voilà %s, tu n'as maintenant plus le rôle %s." % (ctx.author.display_name, role.name))
                    return

    # Non c'est pas ce que je voulais dire
                elif answer.content.lower().startswith("non"):
                    await ctx.send("Bon ben j'ai pas bien compris alors. Exprime toi mieux.")
                    return
                else:
                    await ctx.send("Oui ou non, bordel.")

# Si la personne n'a pas de rôle qui ressemble
    await ctx.send("Tu n'as pas le rôle %s, andouille." % roleName)


@role.command(name="list")
async def listRoles(ctx, *, role=None):
    guild = ctx.guild
    if role is None:
        rolesList = ""
        for role in ctx.guild.roles:
            rolesList = rolesList + ("%s (%i membres)\n" % (role.name, len(role.members)))
        await ctx.send("Voici la liste des rôles qui existent ici :\n```\n%s\n```" % str(rolesList))
    else:
        membersList = ""
        inRole = discord.utils.get(guild.roles, name=role)
        for member in inRole.members:
            membersList = membersList + member.display_name + "\n"
        await ctx.send("Voici la liste des gens dans %s :\n```\n%s\n```" % (inRole, membersList))

@role.command(name="ass")
async def ass(ctx):
    await ctx.send("Non mais là c'est indécent. Autocorrect ou pas autocorrect.")


@bot.group(name="lionel")
async def lionel(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(random.choice(["Oui oui je suis bien là.",
                                      "Oui ?",
                                      "Quoi ?",
                                      "Je suis là.",
                                      "Dis moi tout.",
                                      "Qu'est-ce que ?",
                                      "Présent !"]))

@lionel.command(name="help")
async def help(ctx):
    discord.ext.commands.HelpCommand(ctx)

@bot.command(name="repeat")
async def repeat(ctx, *, message):
    await ctx.send(message)


bot.run(TOKEN)
