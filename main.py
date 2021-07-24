import discord
import logging
import os
import traceback
import yaml

from discord.ext import commands
from discord.ext.commands import CommandNotFound
from logging.handlers import RotatingFileHandler

from cogs.cosmetic import Cosmetic
from cogs.groups import Groups
from cogs.nsfw import NSFW


CONFIG_FILE_PATH = os.environ['BCB_DISCORD_BOT_CONFIG_PATH']


def get_config():
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as ymlfile:
        return yaml.safe_load(ymlfile)


config = get_config()

TOKEN = config['bot']['token']
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), config['logging']['directory'], config['logging']['filename'])

logging.basicConfig(
    handlers=[RotatingFileHandler(LOG_FILE_PATH, maxBytes=5000, backupCount=10)],
    level=logging.getLevelName(config['logging']['level'].upper()),
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt='%Y-%m-%dT%H:%M:%S'
)

intents = discord.Intents.default()
bot = commands.Bot(
    command_prefix=config['bot']['command_prefix'],
    description=config['bot']['description'],
    intents=intents,
    help_command=commands.DefaultHelpCommand(no_category='Other Commands')
)
bot.config = config  # Do this so we can access config values from Cogs
bot.get_config = get_config


@bot.event
async def on_ready():
    logging.info('This bot has logged in as {0}'.format(bot.user.name))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Invalid command. Try `?help` to see the available commands.")
    else:
        raise error


@bot.event
async def on_error(error, *args, **kwargs):
    # TODO: Include some way of informing admins that error has occurred
    logging.error(traceback.format_exc())
    await args[0].send("An error has occurred. Please check the logs.")


bot.add_cog(Groups(bot))
bot.add_cog(NSFW(bot))
bot.add_cog(Cosmetic(bot))
bot.run(TOKEN)
