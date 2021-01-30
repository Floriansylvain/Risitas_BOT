import discord
import asyncio
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
async def aled(ctx):
    await ctx.send("Tapez $rank suivit de votre pseudo League of Legend EUW pour connaître vos classements.")

bot.run(token_bot)