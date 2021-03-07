import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from private import TOKEN_RIOT
from api_riot import rank_track, what_player


class LolCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def lol_rank(self, ctx, invocator_name, x=None):
        if x is None:
            player = what_player(invocator_name)
            if player != 0:
                ranks = rank_track(player)
                embed = discord.Embed(title=invocator_name, url='https://bit.ly/3biTekM')
                embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/11.2.1/img/profileicon/' + str(
                    player['profileIconId']) + '.png')
                embed.set_author(name='League Of Legend - Rank', url='https://euw.leagueoflegends.com/en-gb/',
                    icon_url='https://static.wikia.nocookie.net/leagueoflegends/images/0/07/' + 
                    'League_of_Legends_icon.png/revision/latest?cb=20191018194326')
                if isinstance(ranks, list):
                    for rank_s in ranks:
                        embed.add_field(name=rank_s[0], value=str(rank_s[1]) + ' ' + str(rank_s[2]) + ' ' + str(
                            rank_s[3]) + ' LP' + '\n' + str(rank_s[4]) + 'W/' + str(rank_s[5]) + 'L', inline=False)
                else:
                    embed.description = ranks
                await ctx.send(embed=embed)
            else:
                await ctx.send('The username you entered is unknown.')
        else:
            await ctx.send('If you are trying to use a username with spaces, please surround it with quotes.')


    @lol_rank.error
    async def issou_error(self, ctx, error):
        global CD_LOLRANK
        if isinstance(error, commands.CommandOnCooldown) and not CD_LOLRANK:
            await ctx.send(f'Please wait at least 2 seconds between each $lol_rank.')
            CD_LOLRANK = 1
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Please enter an invocator name (EUW) after $lol_rank.')


def setup(bot):
    bot.add_cog(LolCmds(bot))