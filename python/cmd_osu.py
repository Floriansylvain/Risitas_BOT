import discord
import asyncio
from discord.ext import commands
from api_osu import *


class OsuCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def osu_profile(self, ctx, username, x=None):
        if x is None:
            lst = await ask_osu_profile(username)
            if lst == 1:
                await ctx.send('The username you entered is unknown.')
            else:
                embed = discord.Embed(title=username, url='https://osu.ppy.sh/users/' + str(lst[0]))
                embed.set_author(name='Osu! - Profile', url='https://osu.ppy.sh/home',
                    icon_url=r'https://upload.wikimedia.org/wikipedia/commons/4/44/Osu%21Logo_%282019%29.png')
                embed.set_thumbnail(url='https://a.ppy.sh/' + str(lst[0]))
                embed.add_field(name='Global Ranking',  value='#'+str('{:,}'.format(lst[8])))
                embed.add_field(name='Total Play Time', value=
                    str("%.0f" % ((lst[6] % (86400 * 30)) / 86400))+'d '+
                    str("%.0f" % ((lst[6] % 86400) / 3600))+'h '+
                    str("%.0f" % ((lst[6] % 3600) / 60))+'m ')
                embed.add_field(name='|', value='|')
                embed.add_field(name='Level',        value=str("%.0f" % lst[7]))
                embed.add_field(name='Ranked Score', value=str('{:,}'.format(lst[1])))
                embed.add_field(name='Hit Accuracy', value=str("%.2f" % lst[2])+'%')
                embed.add_field(name='Play Count',   value=str('{:,}'.format(lst[3])))
                embed.add_field(name='Total Score',  value=str('{:,}'.format(lst[4])))
                embed.add_field(name='Total Hits',   value=str('{:,}'.format(lst[5])))
                await ctx.send(embed=embed)
        else:
            await ctx.send('If you are trying to use a username with spaces, please surround it with quotes.')


    @commands.command()
    async def osu_lastgame(self, ctx, username, x=None):
        if x is None:
            lst = await ask_osu_last_game(username)
            if lst == 1:
                await ctx.send('The player you entered is unknown or didn\'t played any game recently.')
            else:
                embed = discord.Embed(title=str(lst[1]) + ' by ' + str(lst[2]), url='https://osu.ppy.sh/beatmapsets/' + str(lst[0]),
                    description='BPM: ' + str("%.0f" % lst[3]) + ' ; Stars: ' + str("%.1f" % lst[4]) +
                    ' ; CS: ' + str(lst[5]) + ' ; AR: ' +  str(lst[7]) +
                    ' ; OD: ' + str(lst[6]) + ' ; HP: ' + str(lst[8]))
                embed.set_author(name='Osu! - Last game', url='https://osu.ppy.sh/home',
                    icon_url=r'https://upload.wikimedia.org/wikipedia/commons/4/44/Osu%21Logo_%282019%29.png')
                embed.set_thumbnail(url='https://b.ppy.sh/thumb/' + str(lst[0]) + 'l.jpg')
                embed.add_field(name='Rank',      value=str(lst[11]))
                embed.add_field(name='Score',     value=str('{:,}'.format(lst[9])))
                embed.add_field(name='Max Combo', value=str(lst[10]))
                embed.add_field(name='300',       value=str(lst[12]))
                embed.add_field(name='Geki',      value=str(lst[17]))
                embed.add_field(name='Accuracy',
                    value=str("%.2f" % (((lst[12]*300)+(lst[13]*100)+(lst[14]*50))/(sum(lst[12:16])*300)*100) + '%'))
                embed.add_field(name='100',       value=str(lst[13]))
                embed.add_field(name='Katu',      value=str(lst[16]))
                embed.add_field(name='Player :',  value=str(username))
                embed.add_field(name='50',        value=str(lst[14]))
                embed.add_field(name='Miss',      value=str(lst[15]))
                embed.add_field(name='|', value='|')
                await ctx.send(embed=embed)
        else:
            await ctx.send('If you are trying to use a username with spaces, please surround it with quotes.')


    @commands.command()
    async def osu_acc(self, ctx, username, x=None):
        if x is None:
            test_acc = await ask_osu_acc(username)
            if test_acc:
                embed = discord.Embed()
                embed.set_author(name='Osu! - Accuracy', icon_url=r'https://upload.wikimedia.org/wikipedia/commons/4/44/Osu%21Logo_%282019%29.png')
                embed.set_image(url="attachment://acc.jpeg")
                await ctx.send(embed=embed, file=discord.File('acc.jpeg'))
            else:
                await ctx.send('The player you entered is unknown or didn\'t played any game recently.')
        else:
            await ctx.send('If you are trying to use a username with spaces, please surround it with quotes.')


def setup(bot):
    bot.add_cog(OsuCmds(bot))