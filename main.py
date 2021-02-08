import asyncio, socket, re, discord
from discord.ext import tasks, commands
from private import *
from riot_api import rank_track, watcher, region
from riotwatcher import ApiError
from emoji import demojize
from twitch import TwitchClient
import gc

bot = commands.Bot(command_prefix='$')
twitch_client = TwitchClient(client_id = id_twitch, oauth_token = token_twitch)
chats = dict()

class ChatObj(object):
    
    def __init__(self, twitch_chan, discord_chan):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.twitch_chan = twitch_chan
        self.discord_chan = discord_chan
        chats[discord_chan] = self

    def __del__(self):
        print("test ssvp")
        del self

    def chat_init(self):
        try:
            self.sock.connect((server, port))
            self.sock.send(f"PASS {token_twitch}\n".encode('utf-8'))
            self.sock.send(f"NICK {nickname}\n".encode('utf-8'))
            self.sock.send(f"JOIN {'#'+self.twitch_chan}\n".encode('utf-8'))
            self.sock.settimeout(0.0)
            self.sock.setblocking(0)
            return 1
        except OSError as test:
            return 0

    @tasks.loop(seconds=1)
    async def twitch(self):
        await bot.wait_until_ready()
        try:
            resp = self.sock.recv(2048).decode('utf-8')
        except socket.error:
            resp = ''
        
        if resp.startswith('PING'):
            self.sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0:
            try:
                username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', demojize(resp)).groups()
                msg = f"**__{username}__ :** {message}"
                await self.discord_chan.send(msg)
            except Exception:
                pass

    @twitch.after_loop
    async def after_slow_count():
        self.sock.shutdown(1)
        self.sock.close()

def check_user(name):
    user = twitch_client.users.translate_usernames_to_ids([name])
    if user == []:
        return False
    return True

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"$help"))
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def chat_set(ctx, arg1):
    chan = ctx.channel
    if chan in list(chats):
        await ctx.send("```A chat is already active, you have to stop it before with the cmd $chat_stop !```")
    else:
        if check_user(arg1):
            obj = ChatObj(arg1, chan)
            if obj.chat_init():
                await ctx.send(f'```Now connected to {arg1}\'s twitch channel !```')
                obj.twitch.start()
            else:
                await ctx.send('```Something went wrong when trying to access Twitch IRC.```')
        else:
            return('```This twitch channel doesn\'t seems to exist.```')

@bot.command()
async def chat_stop(ctx):
    chan = ctx.channel
    if chan in list(chats):
        chats[chan].twitch.stop()
        del chats[chan]
        await ctx.send('```The chat was successfully stopped !```')
    else:
        await ctx.send('```There is no active chat in this channel.```')

@bot.command()
async def rank(ctx, arg, argF=None):
    if argF is None:
        try:
            player = watcher.summoner.by_name(region, arg)
            ranks = rank_track(player)
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
            await ctx.send("The nickname is unknow.")
    else:
        await ctx.send("If you are trying to use a nickname with spaces, please surround it with quotes.")

@bot.command()
async def issou(ctx, arg1:discord.User=None):
    if arg1 is not None:
        user = arg1
    else:
        user = ctx.message.author
    await ctx.message.delete()
    try:
        voice_channel = user.voice.channel
    except AttributeError:
        voice_channel = None

    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio('issou.mp3'))
        if vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()
    else:
        await ctx.send('You or the targeted person are not connected to any channel.')

bot.run(token_bot)