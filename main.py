import discord
import asyncio
from time import sleep
from discord.ext import commands
from private import token_bot
from riot_api import rank_track, watcher, region
from riotwatcher import ApiError

print("Loading...")
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def rank(ctx, arg, argF=None):
    if argF is None:
        try:
            player = watcher.summoner.by_name(region, arg)
            ranks = rank_track(arg, player)

            embed = discord.Embed(title = arg, url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            embed.set_thumbnail(url = "http://ddragon.leagueoflegends.com/cdn/11.2.1/img/profileicon/" + str(player['profileIconId']) + ".png")

            if type(ranks) is list:
                for i in range(len(ranks)):
                    text = str(ranks[i][1]) + ' ' +  str(ranks[i][2]) + ' ' +  str(ranks[i][3]) + ' LP' + '\n' + str(ranks[i][4]) + 'W/' + str(ranks[i][5]) + 'L'
                    embed.add_field(name = ranks[i][0], value = text, inline = False)
            else:
                embed.description = ranks

            await ctx.send(embed = embed)

        except ApiError:
            await ctx.send("Le pseudo est inconnu.")
    else:
        await ctx.send("Si vous essayez d'entrer un pseudo aved des espaces, veillez à l'entourer avec des guillemets.")

@bot.command()
async def issou(ctx):
    user = ctx.message.author
    await ctx.message.delete()
    voice_channel = ctx.message.author.voice.channel
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio('issou.mp3'))
        if vc.is_playing():
            sleep(1)
        await vc.disconnect()
    else:
        await ctx.send('Vous n\'êtes connecté à aucun salon.')

bot.run(token_bot)