import discord
import logging

from asyncio import TimeoutError
from discord.ext import commands


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shownsfw(self, ctx):
        """Assign the role required to view NSFW channels to yourself"""

        def check(reaction, user):
            return user == ctx.author \
                   and str(reaction.emoji) == self.bot.config['bot']['confirmation_emoji'] \
                   and reaction.message == message

        role = discord.utils.get(ctx.guild.roles, name=self.bot.config['roles']['nsfw'])

        if role in ctx.author.roles:
            await ctx.send(f"User [{ctx.author.name}] already has access to NSFW channels.")
        else:
            message = await ctx.send("React to this message with {0} to confirm you have read the #rules.".format(
                self.bot.config['bot']['confirmation_emoji']
            ))
            await message.add_reaction(self.bot.config['bot']['confirmation_emoji'])
            try:
                confirmation = await self.bot.wait_for('reaction_add', check=check,
                                                       timeout=self.bot.config['bot']['message_response_timeout'])
                if confirmation:
                    await ctx.author.add_roles(role)
                    await ctx.send(f"User [{ctx.author.name}] now has access to NSFW channels.")
                    logging.info(f"User [{ctx.author.name}] now has access to NSFW channels.")
            except TimeoutError:
                logging.info(f"User [{ctx.author.name}] failed to respond to the rules confirmation prompt in time.")
            await message.delete()

    @commands.command()
    async def hidensfw(self, ctx):
        """Revoke the role required to view NSFW channels from yourself"""
        role = discord.utils.get(ctx.guild.roles, name=self.bot.config['roles']['nsfw'])
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.send(f"User [{ctx.author.name}] no longer has access to NSFW channels.")
        else:
            await ctx.send(f"User [{ctx.author.name}] already does not have access to NSFW channels.")
