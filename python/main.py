from private import TOKEN_BOT
from time import time
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


@bot.command(hidden=True)
@commands.is_owner()
async def loadext(ctx, extension):
    try:
        bot.load_extension(extension)
        await ctx.send(str(extension) + ' successfully loaded.')
    except discord.ext.commands.ExtensionNotFound:
        await ctx.send('Extension not found.')
    except discord.ext.commands.ExtensionAlreadyLoaded:
        await ctx.send('Extension already loaded.')
    except discord.ext.commands.NoEntryPointError as a:
        await ctx.send(a)
    except ExtensionFailed as b:
        await ctx.send(b)


@bot.command(hidden=True)
@commands.is_owner()
async def unloadext(ctx, extension):
    try:
        bot.unload_extension(extension)
        await ctx.send(str(extension) + ' successfully unloaded.')
    except discord.ext.commands.ExtensionNotFound:
        await ctx.send('Extension not found.')
    except discord.ext.commands.ExtensionNotLoaded:
        await ctx.send('Extension not loaded.')


if __name__ == "__main__":
    for extension in startup_extensions:
        bot.load_extension(extension)
        print('Extension "' + str(extension) + '" loaded.')
    bot.run(TOKEN_BOT)
