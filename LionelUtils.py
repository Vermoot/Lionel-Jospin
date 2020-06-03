import asyncio
from difflib import SequenceMatcher


def is_similar(str1, str2):
    '''Compares two strings and returns True if they're similar.'''
    return SequenceMatcher(None, str1, str2).ratio() > 0.5


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
    def check(react, user): return user == ctx.author and react.message.id == message.id
    reaction = await bot.wait_for("reaction_add", check=check)
    return list(reaction)[0].emoji


async def yes_or_no(bot, ctx, question):
    answer = await reaction_menu(bot, ctx, question, ["👍", "👎"])
    return answer == "👍"


async def cancellable_question(bot, ctx, question):
    '''
        To be used with :
            try:
                action
            except AttributeError:
                return
                                    '''
    def check(m): return m.author == ctx.author
    pending_tasks = [reaction_menu(bot, ctx, question, "❌"),
                     bot.wait_for("message", check=check)]
    done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending_tasks:
        task.cancel()
    result = done_tasks.pop().result()
    if isinstance(result, str):
        await ctx.send("Ok j'annule, bye.")
        return None
    return result.content

async def sponge(bot, ctx, message, edit_text):
    await message.add_reaction("🧽")

    def check(react, user):
        return user == ctx.author and react.message.id == message.id

    sponge_react = await bot.wait_for("reaction_add", check=check)
    if list(sponge_react)[0].emoji == "🧽":
        await message.edit(content=edit_text)

async def me_too(bot, ctx, message):
    pass