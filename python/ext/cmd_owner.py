from discord.ext import commands
from datetime import datetime
from __main__ import startup_date
import discord
import asyncio


class OwnerCmds(commands.Cog, name='Owner commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, ignore_extra=False)
    @commands.is_owner()
    async def loadext(self, ctx, extension):
        bot.load_extension(extension)
        await ctx.send("Extension loaded.")


    @commands.command(hidden=True, ignore_extra=False)
    @commands.is_owner()
    async def unloadext(self, ctx, extension):
        bot.unload_extension(extension)
        await ctx.send("Extension unloaded.")


    @commands.command(hidden=True)
    @commands.is_owner()
    async def update(self, ctx):
        result = str(os.popen('git pull').read())
        await ctx.send('``' + result + '``')
        if 'Already up to date' not in result:
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 


    @commands.command(hidden=True)
    @commands.is_owner()
    async def getlogs(self, ctx):
        await ctx.send('Logs since ' + startup_date.strftime("``[%d-%m-%y | %H:%M:%S]``"),
            file=discord.File('logs.txt'))


def setup(bot):
    bot.add_cog(OwnerCmds(bot))
