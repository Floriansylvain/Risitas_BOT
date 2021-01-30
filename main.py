import discord
import asyncio
from discord.ext import commands
from private import token_bot
from riot_api import rank_track, watcher, region
from riotwatcher import ApiError

client = discord.Client()
bot = commands.Bot(command_prefix='$')
print("Loading...")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')


# @bot.command()
# async def test(ctx, arg):
#     await ctx.send(arg)

@bot.command()
async def rank(ctx, arg):
    try:
        player = watcher.summoner.by_name(region, arg)
        text = rank_track(arg, player)
        embed= discord.Embed(title=arg, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description=text)
        embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/11.2.1/img/profileicon/" + str(player['profileIconId']) + ".png")
        await ctx.send(embed=embed)
    except ApiError:
        await ctx.send("Le pseudo est inconnu ou un problème est survenu. (ma gestion des erreurs est à chier, déso pas déso)")

@bot.command()
async def aled(ctx):
    await ctx.send("Tapez $rank suivit de votre pseudo League of Legend EUW pour connaître vos classements.")

bot.run(token_bot)