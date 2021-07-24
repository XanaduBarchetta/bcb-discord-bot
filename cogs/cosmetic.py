import discord

from discord.ext import commands


class Cosmetic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listroles(self, ctx):
        """List the available cosmetic roles"""

        # Reload config file to obtain current roles
        # This is a little kludgy. Should improve later.
        self.bot.config = self.bot.get_config()

        # NOTE: This does not account for the extreme case in which the full list of roles is >2000 characters
        cosmetic_role_list = ', '.join(sorted(self.bot.config['roles']['cosmetic']))

        await ctx.send(f"These cosmetic roles are available:```{cosmetic_role_list}```")

    @commands.command()
    async def getrole(self, ctx, role_name):
        """Get a specified cosmetic role"""
        if role_name not in self.bot.config['roles']['cosmetic']:
            await ctx.send("That role does not exist. Remember: roles are case-sensitive!")
            await ctx.invoke(self.bot.get_command('listroles'))
        else:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role in ctx.author.roles:
                await ctx.send(f"User [{ctx.author.name}] already has role [{role_name}].")
            else:
                await ctx.author.add_roles(role)
                await ctx.send(f"User [{ctx.author.name}] now has role [{role_name}].")

    @commands.command()
    async def removerole(self, ctx, role_name):
        """Remove a specified cosmetic role"""
        if role_name not in self.bot.config['roles']['cosmetic']:
            await ctx.send("That role does not exist. Remember: roles are case-sensitive!")
            await ctx.invoke(self.bot.get_command('listroles'))
        else:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role not in ctx.author.roles:
                await ctx.send(f"User [{ctx.author.name}] already does not have role [{role_name}].")
            else:
                await ctx.author.remove_roles(role)
                await ctx.send(f"User [{ctx.author.name}] no longer has role [{role_name}].")
