import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from api_riot import rank_track, what_player, last_match

CD_LOLRANK = 0

class LolCmds(commands.Cog, name='League of Legend commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(ignore_extra=False)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def lol_rank(self, ctx, invocator_name):
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


    @commands.command(ignore_extra=False)
    async def lol_lastgame(self, ctx, invocator_name):
        player = what_player(invocator_name)
        if player != 0:
            lst = last_match(player)
            lst_p = lst[0]
            maximum = lst_p[0][1]
            for stat in lst_p:
                if stat[1] > maximum:
                    maximum = stat[1]
            tab, players, kda = [], [], []
            for stat in lst_p:
                pourcent = round(100*stat[1]/maximum)
                equals = int(round(float(pourcent)/3.3))
                hyphen = 30 - equals
                tab.append('[' + '='*equals + ' '*hyphen +']\n')
                players.append(stat[0][:15] + '\n')
                kda.append(str(stat[2]) + '/' + str(stat[3]) + '/' + str(stat[4]) + '\n')
            embed = discord.Embed(title=invocator_name, url='https://bit.ly/3biTekM', 
                description='Date: ' + lst[2] + '\nLength: ' + lst[3])
            embed.set_author(name='League Of Legend - Last Game', url='https://euw.leagueoflegends.com/en-gb/',
                icon_url='https://static.wikia.nocookie.net/leagueoflegends/images/0/07/' + 
                'League_of_Legends_icon.png/revision/latest?cb=20191018194326')
            await ctx.send(embed=embed)
            for i in range(0, -2, -1):
                embed = discord.Embed(title='Team 1' if not i else 'Team 2', colour=
                    discord.Colour.green() if lst[1][0][i] == 'Win' else discord.Colour.red(), description=
                        (':drop_of_blood: First blood\n' if len(lst[1][1]) != 0 and lst[1][1][i] else '') +
                        (':tokyo_tower: First tower\n' if len(lst[1][2]) != 0 and lst[1][2][i] else '') +
                        (':dragon_face: First dragon\n' if len(lst[1][3]) != 0 and lst[1][3][i] else ''))
                embed.add_field(name='Players', 
                    value='```\n' + ''.join(players[:5] if not i else players[5:]) + '```')
                embed.add_field(name='Total damage dealt to champions', 
                    value='```\n' + ''.join(tab[:5] if not i else tab[5:]) + '```')
                embed.add_field(name='K / D / A', 
                    value='```\n' + ''.join(kda[:5] if not i else kda[5:]) + '```')
                await ctx.send(embed=embed)
        else:
            await ctx.send('The username you entered is unknown.')


def setup(bot):
    bot.add_cog(LolCmds(bot))
