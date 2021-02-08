import asyncio
import socket
import re
import discord
from private import *
from discord.ext import tasks, commands
from riot_api import rank_track, WATCHER, REGION
from riotwatcher import ApiError
from emoji import demojize
from twitch import TwitchClient

bot = commands.Bot(command_prefix='$')
twitch_client = TwitchClient(client_id=ID_TWITCH, oauth_token=TOKEN_TWITCH)
chats = dict()


class ChatObj:
    def __init__(self, twitch_chan, discord_chan):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.twitch_chan = twitch_chan
        self.discord_chan = discord_chan
        chats[discord_chan] = self

    def chat_init(self):
        try:
            self.sock.connect((SERVER, PORT))
            self.sock.send(f"PASS {TOKEN_TWITCH}\n".encode('utf-8'))
            self.sock.send(f"NICK {NICKNAME}\n".encode('utf-8'))
            self.sock.send(f"JOIN {'#' + self.twitch_chan}\n".encode('utf-8'))
            self.sock.settimeout(0.0)
            self.sock.setblocking(0)
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
            self.sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0:
            try:
                chain = re.search(r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', demojize(resp))
                username = chain.group(1)
                message = chain.group(3)
                msg = f"**__{username}__ :** {message}"
                await self.discord_chan.send(msg)
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


@bot.event
async def on_ready():
    default_activity = discord.Activity(type=discord.ActivityType.listening, name="$help")
    await bot.change_presence(activity=default_activity)
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def chat_set(ctx, arg1):
    await ctx.message.delete()
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
            await ctx.send('```This twitch channel doesn\'t seems to exist.```')


@bot.command()
async def chat_stop(ctx):
    await ctx.message.delete()
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
    await ctx.message.delete()
    if argf is None:
        try:
            player = WATCHER.summoner.by_name(REGION, arg)
            ranks = rank_track(player)
            embed = discord.Embed(title=arg, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/11.2.1/img/profileicon/" + str(
                player['profileIconId']) + ".png")
            if isinstance(ranks, list):
                for rank_s in ranks:
                    embed.add_field(name=rank_s[0], value=str(rank_s[1]) + ' ' + str(rank_s[2]) + ' ' + str(
                        rank_s[3]) + ' LP' + '\n' + str(rank_s[4]) + 'W/' + str(rank_s[5]) + 'L', inline=False)
            else:
                embed.description = ranks
            await ctx.send(embed=embed)
        except ApiError:
            await ctx.send("The nickname is unknow.")
    else:
        await ctx.send("If you are trying to use a nickname with spaces, please surround it with quotes.")


@bot.command()
async def issou(ctx, arg1: discord.User = None):
    if arg1 is not None:
        user = arg1
    else:
        user = ctx.message.author
    await ctx.message.delete()
    try:
        voice_channel = user.voice.channel
    except AttributeError:
        voice_channel = None

    if voice_channel is not None:
        voice = await voice_channel.connect()
        voice.play(discord.FFmpegPCMAudio('issou.mp3'))
        if voice.is_playing():
            await asyncio.sleep(1)
        await voice.disconnect()
    else:
        await ctx.send('You or the targeted person are not connected to any channel.')


bot.run(TOKEN_BOT)
