import discord
from discord.ext import commands
from difflib import SequenceMatcher


def isSimilar(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio() > 0.5


class RolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def getRole(self, ctx, userInput, scope):
        for role in scope:
            # Si le rôle existe (indépendant de la casse)
            if userInput.lower() == role.name.lower():
                return role

        for role in scope: # En deux boucles pour que les rôles existants soient bien prioritaires

            # Si un rôle ressemblant existe
            if isSimilar(userInput, role.name):
                def check(m):
                    return m.author == ctx.author
                await ctx.send("Est-ce que tu veux dire \"%s\" ?" % role.name)
                while True:
                    answer = await self.bot.wait_for("message", check=check, timeout=10)
                    if answer.content.lower().startswith("oui"):
                        return role
                    elif answer.content.lower().startswith("non"):
                        await ctx.send("Donc tu veux bien dire %s ?" % userInput)
                        while True:
                            answer = await self.bot.wait_for("message", check=check, timeout=10)
                            if answer.content.lower().startswith("oui"):
                                return userInput
                            elif answer.content.lower().startswith("non"):
                                await ctx.send("Ouais ben reviens me voir quand tu seras décidé alors hein. Merde.")
                                return None
                            else:
                                await ctx.send("Oui ou non, bordel.")
                    else:
                        await ctx.send("Oui ou non, bordel.")

        # Si le rôle n'existe pas
        return userInput # ATTENTION c'est une string



    @commands.group(name="role")
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Non là t'as merdé mon coco.")

    # S'attribuer un rôle avec !role add rôle
    @role.command(name="add")
    async def addRole(self, ctx, *, roleName):
        newRole = await self.getRole(ctx, roleName, ctx.guild.roles)
        if newRole is None:
            return
        elif isinstance(newRole, str):
            role = await ctx.guild.create_role(name=newRole, mentionable=True)
            await ctx.author.add_roles(role)
            await ctx.send("Voilà %s, tu as maintenant le rôle %s ! Tu es le premier, invite tes copains!" % (
                ctx.author.display_name, role.name))
        elif ctx.author in newRole.members:
            await ctx.send("Tu as déjà le rôle %s, couillon." % newRole.name)
            return
        else:
            await ctx.author.add_roles(newRole)
            await ctx.send(
                "Voilà %s, tu as maintenant le rôle %s ! Vous êtes %i. Je crois. Mais je suis pas fort en math." % (
                    ctx.author.display_name, newRole.name, len(newRole.members)))
            return

    # S'enlever un rôle avec !role remove rôle
    @role.command(name="remove")
    async def remRole(self, ctx, *, roleName):
        roleToRemove = await self.getRole(ctx, roleName, ctx.author.roles)
        if roleToRemove is None:
            return
        elif roleToRemove in ctx.author.roles:
            await ctx.author.remove_roles(roleToRemove)
            if len(roleToRemove.members) == 0:
                await roleToRemove.delete()
                await ctx.send(
                    "Voilà %s, tu n'as maintenant plus le rôle %s. Plus personne ne l'a, d'ailleurs. Je le ferme." % (
                        ctx.author.display_name, roleToRemove.name))
                return
            else:
                await ctx.send(
                    "Voilà %s, tu n'as maintenant plus le rôle %s." % (ctx.author.display_name, roleToRemove.name))
                return
        else:
            await ctx.send("Tu n'as pas le rôle %s, andouille." % roleToRemove)

    # Voir la liste des rôles avec !role list /// Voir les membres d'un rôle avec !role list rôle
    @role.command(name="list")
    async def listRoles(self, ctx, *, role=None):
        if role is None:
            rolesList = ""
            for role in ctx.guild.roles:
                rolesList = rolesList + ("%s (%i membres)\n" % (role.name, len(role.members)))
            await ctx.send("Voici la liste des rôles qui existent ici :\n```\n%s\n```" % str(rolesList))
        else:
            inRole = await self.getRole(ctx, role, ctx.guild.roles)
            if isinstance(inRole, str):
                await ctx.send("Le rôle %s n'existe pas." % inRole)
            elif inRole is None:
                return
            else:
                membersList = ""
                for member in inRole.members:
                    membersList = membersList + member.display_name + "\n"
                await ctx.send("Voici la liste des gens dans %s :\n```\n%s\n```" % (inRole.name, membersList))

    # Drôle
    @role.command(name="ass")
    async def ass(self, ctx):
        await ctx.send("Non mais là c'est indécent. Autocorrect ou pas autocorrect.")

    # Rappel
    @commands.command(name="add")
    async def add(self, ctx):
        await ctx.send("Non c'est `!role add`.")

    # Pour Sam
    @commands.command(name="roll")
    async def add(self, ctx):
        await ctx.send("ROLE bordel, pas roll. Fais un effort marde.")


def setup(bot):
    bot.add_cog(RolesCog(bot))
