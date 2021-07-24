import discord

from discord.ext import commands


class Groups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listgroups(self, ctx):
        """List the available server groups"""

        # Reload config file to obtain current roles
        # This is a little kludgy. Should improve later.
        self.bot.config = self.bot.get_config()

        detailed_group_list = ""
        for group_name, details in self.bot.config['roles']['groups'].items():
            detailed_group_list = detailed_group_list + f"\n- {group_name}\n\t{details['description']}"

        ###
        # Uncomment this block of code if we decide we want to do fancy embeds for responses
        ###
        # embed = discord.Embed(
        #     description=f"These groups are available to join:{response_text}")
        # )
        #
        # await ctx.send(embed=embed)

        await ctx.send(f"These groups are available to join:```{detailed_group_list}```")

    @commands.command()
    async def joingroup(self, ctx, group_name):
        """Join a specified group"""
        if group_name not in self.bot.config['roles']['groups'].keys():
            await ctx.send("That group does not exist. Remember: groups are case-sensitive!")
            await ctx.invoke(self.bot.get_command('listgroups'))
        else:
            role = discord.utils.get(ctx.guild.roles, name=self.bot.config['roles']['groups'][group_name]['role_name'])
            if role in ctx.author.roles:
                await ctx.send(f"User [{ctx.author.name}] already is a member of group [{group_name}].")
            else:
                await ctx.author.add_roles(role)
                await ctx.send(f"User [{ctx.author.name}] successfully joined group [{group_name}].")

    @commands.command()
    async def leavegroup(self, ctx, group_name):
        """Leave a specified group"""
        if group_name not in self.bot.config['roles']['groups'].keys():
            await ctx.send("That group does not exist. Remember: groups are case-sensitive!")
            await ctx.invoke(self.bot.get_command('listgroups'))
        else:
            role = discord.utils.get(ctx.guild.roles, name=self.bot.config['roles']['groups'][group_name]['role_name'])
            if role not in ctx.author.roles:
                await ctx.send(f"User [{ctx.author.name}] already is not a member of group [{group_name}].")
            else:
                await ctx.author.remove_roles(role)
                await ctx.send(f"User [{ctx.author.name}] successfully left group [{group_name}].")
