import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
guild = os.getenv("DISCORD_GUILD")
bot = commands.Bot(command_prefix='!')

print("Bot lancé.")


@bot.group(name="role")
async def role(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Non là t'as merdé mon coco.")


@role.command(name="add")  # TODO gérer les presque-doublons avec la casse
async def addRole(ctx, *, roleName):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=roleName)

    if not role:
        role = await ctx.guild.create_role(name=roleName, mentionable=True)

    if ctx.author in role.members:
        await ctx.send("Tu as déjà le rôle %s, couillon." % role.name)
    else:
        await ctx.author.add_roles(role)
        await ctx.send("Voilà %s, tu as maintenant le rôle %s ! Vous êtes %d." % (ctx.author.display_name, role.name, len(role.members)))

@role.command(name="remove")
async def remRole(ctx, *, roleName):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=roleName)
    if role == None or ctx.author not in role.members:
        await ctx.send("Tu n'as pas le rôle %s, couillon." % roleName)
    else:
        await ctx.author.remove_roles(role)
        if len(role.members) == 0:
            await role.delete()
            await ctx.send("Voilà %s, tu n'as maintenant plus le rôle %s. Plus personne ne l'a, d'ailleurs. Je le ferme." % (ctx.author.display_name, role.name))
        else:
            await ctx.send(
                "Voilà %s, tu n'as maintenant plus le rôle %s." % (ctx.author.display_name, role.name))
            print(len(role.members))

@role.command(name="list")  # TODO Pouvoir demander qui a le rôle X
async def listRoles(ctx):
    rolesList = ""
    for role in ctx.guild.roles:
        rolesList = rolesList + ("%s (%d membres)\n" % (role.name, len(role.members)))
    await ctx.send("Voici la liste des rôles qui existent ici :\n```\n%s\n```" % str(rolesList))


@bot.command(name="lionel")
async def test(ctx):
    await ctx.send("Oui oui je suis bien là.")

@bot.command(name="repeat")
async def repeat(ctx, *, message):
    await ctx.send(message)

bot.run(token)