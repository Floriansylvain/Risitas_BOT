import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

CD_ISSOU = 0

class OtherCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    async def issou(self, ctx, username: discord.User = None):
        if username is not None:
            user = username
        else:
            user = ctx.message.author
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        try:
            voice_channel = user.voice.channel
        except AttributeError:
            voice_channel = None

        if voice_channel is not None:
            voice = await voice_channel.connect()
            voice.play(discord.FFmpegPCMAudio('../assets/issou.mp3'))
            if voice.is_playing():
                await asyncio.sleep(1)
            await voice.disconnect()
            global CD_ISSOU
            CD_ISSOU = 0
        else:
            await ctx.send('You or the targeted person are not connected to any channel.')


    @issou.error
    async def issou_error(self, ctx, error):
        global CD_ISSOU
        if isinstance(error, commands.CommandOnCooldown) and not CD_ISSOU:
            await ctx.send(f'Please wait at least 2 seconds between each $issou.')
            CD_ISSOU = 1


def setup(bot):
    bot.add_cog(OtherCmds(bot))