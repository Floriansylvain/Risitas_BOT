from private import TOKEN_BOT
from discord.ext import commands
import discord

bot = commands.Bot(command_prefix='$')
startup_extensions = ["cmd_other", "cmd_lol", "cmd_osu", "cmd_twitch"]

@bot.event
async def on_ready():
    default_activity = discord.Activity(type=discord.ActivityType.listening, name='$help')
    await bot.change_presence(activity=default_activity)
    print('We have logged in as ' + bot.user.name + '.')


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)
    bot.run(TOKEN_BOT)
