from discord.ext import commands
from difflib import SequenceMatcher


def is_similar(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio() > 0.5


class RolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_role(self, ctx, user_input, scope):
        for role in scope:
            # Si le rôle existe (indépendant de la casse)
            if user_input.lower() == role.name.lower():
                return role

        for role in scope:  # En deux boucles pour que les rôles existants soient bien prioritaires

            # Si un rôle ressemblant existe
            if is_similar(user_input, role.name):
                def check(m):
                    return m.author == ctx.author
                await ctx.send("Est-ce que tu veux dire \"%s\" ?" % role.name)
                while True:
                    answer = await self.bot.wait_for("message", check=check, timeout=10)
                    if answer.content.lower().startswith("oui"):
                        return role
                    elif answer.content.lower().startswith("non"):
                        await ctx.send("Donc tu veux bien dire %s ?" % user_input)
                        while True:
                            answer = await self.bot.wait_for("message", check=check, timeout=10)
                            if answer.content.lower().startswith("oui"):
                                return user_input
                            elif answer.content.lower().startswith("non"):
                                await ctx.send("Ouais ben reviens me voir quand tu seras décidé alors hein. Merde.")
                                return None
                            else:
                                await ctx.send("Oui ou non, bordel.")
                    else:
                        await ctx.send("Oui ou non, bordel.")

        # Si le rôle n'existe pas
        return user_input  # ATTENTION c'est une string

    @commands.group(name="role")
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Non là t'as merdé mon coco.")

    # S'attribuer un rôle avec !role add rôle
    @role.command(name="add")
    async def add_role(self, ctx, *, role_name):
        new_role = await self.get_role(ctx, role_name, ctx.guild.roles)
        if new_role is None:
            return
        elif isinstance(new_role, str):
            role = await ctx.guild.create_role(name=new_role, mentionable=True)
            await ctx.author.add_roles(role)
            await ctx.send("Voilà %s, tu as maintenant le rôle %s ! Tu es le premier, invite tes copains!" % (
                ctx.author.display_name, role.name))
        elif ctx.author in new_role.members:
            await ctx.send("Tu as déjà le rôle %s, couillon." % new_role.name)
            return
        else:
            await ctx.author.add_roles(new_role)
            await ctx.send(
                "Voilà %s, tu as maintenant le rôle %s ! Vous êtes %i. Je crois. Mais je suis pas fort en math." % (
                    ctx.author.display_name, new_role.name, len(new_role.members)))
            return

    # S'enlever un rôle avec !role remove rôle
    @role.command(name="remove")
    async def remove_role(self, ctx, *, role_name):
        role_to_remove = await self.get_role(ctx, role_name, ctx.author.roles)
        if role_to_remove is None:
            return
        elif role_to_remove in ctx.author.roles:
            await ctx.author.remove_roles(role_to_remove)
            if len(role_to_remove.members) == 0:
                await role_to_remove.delete()
                await ctx.send(
                    "Voilà %s, tu n'as maintenant plus le rôle %s. Plus personne ne l'a, d'ailleurs. Je le ferme." % (
                        ctx.author.display_name, role_to_remove.name))
                return
            else:
                await ctx.send(
                    "Voilà %s, tu n'as maintenant plus le rôle %s." % (ctx.author.display_name, role_to_remove.name))
                return
        else:
            await ctx.send("Tu n'as pas le rôle %s, andouille." % role_to_remove)

    # Voir la liste des rôles avec !role list /// Voir les membres d'un rôle avec !role list rôle
    @role.command(name="list")
    async def list_roles(self, ctx, *, role=None):
        if role is None:
            roles_list = ""
            for role in ctx.guild.roles:
                roles_list = roles_list + ("%s (%i membres)\n" % (role.name, len(role.members)))
            await ctx.send("Voici la liste des rôles qui existent ici :\n```\n%s\n```" % str(roles_list))
        else:
            in_role = await self.get_role(ctx, role, ctx.guild.roles)
            if isinstance(in_role, str):
                await ctx.send("Le rôle %s n'existe pas." % in_role)
            elif in_role is None:
                return
            else:
                members_list = ""
                for member in in_role.members:
                    members_list = members_list + member.display_name + "\n"
                await ctx.send("Voici la liste des gens dans %s :\n```\n%s\n```" % (in_role.name, members_list))

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
