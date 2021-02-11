import asyncio
import socket
import re
import discord
from private import *
from osu_api import *
from discord.ext import tasks, commands
from riot_api import rank_track, WATCHER, REGION
from riotwatcher import ApiError
from emoji import demojize
from twitch import TwitchClient

bot = commands.Bot(command_prefix='$')
twitch_client = TwitchClient(client_id=ID_TWITCH, oauth_token=TOKEN_TWITCH)
chats = dict()


class ChatObj:
    def __init__(self, twitch_user, discord_channel):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.twitch_user = twitch_user
        self.discord_channel = discord_channel
        chats[discord_channel] = self

    def chat_init(self):
        try:
            self.sock.connect((SERVER, PORT))
            self.sock.send(f'PASS {TOKEN_TWITCH}\n'.encode('utf-8'))
            self.sock.send(f'NICK {NICKNAME}\n'.encode('utf-8'))
            self.sock.send(f"JOIN {'#' + self.twitch_user}\n".encode('utf-8'))
            self.sock.settimeout(0.0)
            self.sock.setblocking(False)
            return 1
        except OSError:
            return 0

    @tasks.loop(seconds=1)
    async def twitch(self):
        await bot.wait_until_ready()
        try:
            resp = self.sock.recv(2048).decode('utf-8')
        except socket.error:
            resp = ''

        if resp.startswith('PING'):
            self.sock.send('PONG\n'.encode('utf-8'))

        elif len(resp) > 0:
            try:
                chain = re.search(r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', demojize(resp))
                username = chain.group(1)
                message = chain.group(3)
                msg = f'**__{username}__ :** {message}'
                await self.discord_channel.send(msg)
            except discord.DiscordException:
                pass
            except AttributeError:
                pass

    @twitch.after_loop
    async def after_twitch(self):
        self.sock.shutdown(1)
        try:
            self.sock.close()
        except OSError:
            pass


def check_user(name):
    user = twitch_client.users.translate_usernames_to_ids([name])
    if not user:
        return False
    return True


async def del_message(ctx):
    try:
        await ctx.message.delete()
    except discord.errors.Forbidden:
        pass


@bot.event
async def on_ready():
    default_activity = discord.Activity(type=discord.ActivityType.listening, name='$help')
    await bot.change_presence(activity=default_activity)
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def chat_set(ctx, arg1):
    await del_message(ctx)
    what_channel = ctx.channel
    if what_channel in list(chats):
        await ctx.send("```A chat is already active, you have to stop it before with the cmd $chat_stop !```")
    else:
        if check_user(arg1):
            obj = ChatObj(arg1, what_channel)
            if obj.chat_init():
                await ctx.send(f'```Now connected to {arg1}\'s twitch channel !```')
                obj.twitch.start()
            else:
                await ctx.send('```Something went wrong when trying to access Twitch IRC.```')
        else:
            await ctx.send('```This twitch channel doesn\'t seems to exist.```')


@bot.command()
async def chat_stop(ctx):
    await del_message(ctx)
    chan = ctx.channel
    if chan in list(chats):
        chats[chan].twitch.stop()
        del chats[chan]
        await asyncio.sleep(1)
        message = '```The chat was successfully stopped !```'
    else:
        message = '```There is no active chat in this channel.```'
    await ctx.send(message)


@bot.command()
async def rank(ctx, arg, argf=None):
    await del_message(ctx)
    if argf is None:
        try:
            player = WATCHER.summoner.by_name(REGION, arg)
            ranks = rank_track(player)
            embed = discord.Embed(title=arg, url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/11.2.1/img/profileicon/' + str(
                player['profileIconId']) + '.png')
            embed.set_author(name='League Of Legend', url='https://euw.leagueoflegends.com/en-gb/',
                icon_url='https://static.wikia.nocookie.net/leagueoflegends/images/0/07/' + 
                'League_of_Legends_icon.png/revision/latest?cb=20191018194326')
            if isinstance(ranks, list):
                for rank_s in ranks:
                    embed.add_field(name=rank_s[0], value=str(rank_s[1]) + ' ' + str(rank_s[2]) + ' ' + str(
                        rank_s[3]) + ' LP' + '\n' + str(rank_s[4]) + 'W/' + str(rank_s[5]) + 'L', inline=False)
            else:
                embed.description = ranks
            await ctx.send(embed=embed)
        except ApiError:
            await ctx.send('The username you entered is unknown.')
    else:
        await ctx.send('If you are trying to use a username you entered with spaces, please surround it with quotes.')


@bot.command()
async def issou(ctx, arg1: discord.User = None):
    if arg1 is not None:
        user = arg1
    else:
        user = ctx.message.author
    await del_message(ctx)
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
    else:
        await ctx.send('You or the targeted person are not connected to any channel.')


@bot.command()
async def osu_profile(ctx, arg):
    await del_message(ctx)
    lst = await ask_osu_profile(arg)
    if lst == 1:
        await ctx.send('The username you entered is unknown.')
    else:
        embed = discord.Embed(title=arg, url='https://osu.ppy.sh/users/' + str(lst[0]))
        embed.set_author(name='Osu!', url='https://osu.ppy.sh/home',
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


@bot.command()
async def osu_lastgame(ctx, arg):
    await del_message(ctx)
    lst = await ask_osu_last_game(arg)
    if lst == 1:
        await ctx.send('The player you entered is unknown or didn\'t played any game recently.')
    else:
        embed = discord.Embed(title=str(lst[1]) + ' by ' + str(lst[2]), url='https://osu.ppy.sh/beatmapsets/' + str(lst[0]),
            description='BPM: ' + str("%.0f" % lst[3]) + ' ; Stars: ' + str("%.1f" % lst[4]) +
            ' ; CS: ' + str(lst[5]) + ' ; OD: ' +  str(lst[6]) +
            ' ; AR: ' + str(lst[7]) + ' ; HP: ' + str(lst[8]))
        embed.set_author(name='Osu!', url='https://osu.ppy.sh/home',
            icon_url=r'https://upload.wikimedia.org/wikipedia/commons/4/44/Osu%21Logo_%282019%29.png')
        embed.set_thumbnail(url='https://b.ppy.sh/thumb/' + str(lst[0]) + 'l.jpg')
        embed.add_field(name='Rank',      value=str(lst[11]))
        embed.add_field(name='Score',     value=str('{:,}'.format(lst[9])))
        embed.add_field(name='Max Combo', value=str(lst[10]))
        embed.add_field(name='300',       value=str(lst[12]))
        embed.add_field(name='100',       value=str(lst[13]))
        embed.add_field(name='Accuracy',
            value=str("%.2f" % ((lst[12]/(lst[12]+lst[13]+lst[14]+lst[15]))*100)) + '%')
        embed.add_field(name='50',        value=str(lst[14]))
        embed.add_field(name='Miss',      value=str(lst[15]))
        embed.add_field(name='Player :',  value=str(arg))
        await ctx.send(embed=embed)


bot.run(TOKEN_BOT)
