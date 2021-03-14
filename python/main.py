from private import TOKEN_BOT
from time import time
from datetime import datetime
from discord.ext import commands
from miscellaneous import spellchecker
import logging
import os, sys
import discord


print('Loading started')

bot = commands.Bot(command_prefix='$')
startup_extensions = ["cmd_other", "cmd_lol", "cmd_osu", "cmd_twitch"]

startup_date = datetime.now()
time_s = time()

formatter = logging.Formatter('%(message)s')
handler = logging.FileHandler('logs.txt')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


@bot.event
async def on_ready():
    default_activity = discord.Activity(type=discord.ActivityType.listening, name='$help')
    await bot.change_presence(activity=default_activity)
    print('Logged in as ' + str(bot.user) +
        ' in ' + str(round(time() - time_s, 2)) + 's.')


@bot.event
async def on_command_error(ctx, error):
    logger.info(datetime.now().strftime("[%d-%m-%y][%H:%M:%S]") +
        ' \'' + str(error) +  '\' from ' +str(ctx.author) + ' on ' +
        (ctx.message.guild.name if ctx.message.guild is not None else 'DMs') + '.')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(spellchecker(str(ctx.message.content)[1:]))
    else:
        await ctx.send(error)


@bot.command(hidden=True, ignore_extra=False)
@commands.is_owner()
async def loadext(ctx, extension):
    bot.load_extension(extension)
    await ctx.send("Extension loaded.")


@bot.command(hidden=True, ignore_extra=False)
@commands.is_owner()
async def unloadext(ctx, extension):
    bot.unload_extension(extension)
    await ctx.send("Extension unloaded.")


@bot.command(hidden=True)
@commands.is_owner()
async def update(ctx):
    result = str(os.popen('git pull').read())
    await ctx.send('``' + result + '``')
    if 'Already up to date' not in result:
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 


@bot.command(hidden=True)
@commands.is_owner()
async def getlogs(ctx):
    await ctx.send('Logs since ' + startup_date.strftime("``[%d-%m-%y | %H:%M:%S]``"),
        file=discord.File('logs.txt'))


if __name__ == "__main__":
    for extension in startup_extensions:
        bot.load_extension('ext.' + extension)
        print('Extension "' + str(extension) + '" loaded.')
    bot.run(TOKEN_BOT)
