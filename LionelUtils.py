async def reaction_menu(bot, ctx, question, choices):
    message_text = question
    if isinstance(choices, dict):
        message_text += "```"
        for emoji, choice in choices.items():
            message_text += "%s️ %s \n" % (emoji, choice)
        message_text += "```"
    message = await ctx.send(message_text)
    for emoji in choices:
        await message.add_reaction(emoji)
    def check(reaction, user): return user == ctx.author
    reaction = await bot.wait_for("reaction_add", check=check)
    return list(reaction)[0].emoji


async def yes_or_no(bot, ctx, question):
    answer = await reaction_menu(bot, ctx, question, ["👍", "👎"])
    return answer == "👍"
