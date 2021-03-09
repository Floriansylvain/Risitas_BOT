from private import TOKEN_BOT
from time import time
from datetime import datetime
from discord.ext import commands
import discord


bot = commands.Bot(command_prefix='$')
startup_extensions = ["cmd_other", "cmd_lol", "cmd_osu", "cmd_twitch"]
time_s = time()
print('Loading started')


@bot.event
async def on_ready():
    default_activity = discord.Activity(type=discord.ActivityType.listening, name='$help')
    await bot.change_presence(activity=default_activity)
    print('Logged in as ' + str(bot.user) +
        ' in ' + str(round(time() - time_s, 2)) + 's.')


@bot.event
async def on_command_error(ctx, error):
    print(datetime.now().strftime("[%H:%M:%S]") + ' \'' + str(error) + '\' from ' + str(ctx.author) + ' on ' + ctx.message.guild.name + '.')
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


if __name__ == "__main__":
    for extension in startup_extensions:
        bot.load_extension('ext.' + extension)
        print('Extension "' + str(extension) + '" loaded.')
    bot.run(TOKEN_BOT)
