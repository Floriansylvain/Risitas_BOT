import asyncio, socket, re, discord
from discord.ext import tasks, commands
from private import *
from riot_api import rank_track, watcher, region
from riotwatcher import ApiError
from emoji import demojize
from twitch import TwitchClient

bot = commands.Bot(command_prefix='$')
TASK = None
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
twitch_client = TwitchClient(client_id = id_twitch, oauth_token = token_twitch)

def check_user(name):
    user = twitch_client.users.translate_usernames_to_ids([name])
    if user == []:
        return False
    return True

def chat_init(twitch_chan):
    global SOCK
    if check_user(twitch_chan):
        try:
            SOCK.connect((server, port))
            SOCK.send(f"PASS {token_twitch}\n".encode('utf-8'))
            SOCK.send(f"NICK {nickname}\n".encode('utf-8'))
            SOCK.send(f"JOIN {'#'+twitch_chan}\n".encode('utf-8'))
            SOCK.settimeout(0.0)
            SOCK.setblocking(0)
            return 1
        except OSError:
            return('```Impossible de se connecter au chat IRC de Twitch.```')
    return('```Cette chaine n\'existe pas. Verifiez l\'orthographe ou la syntaxe.```')

def get_msg():
    try:
        resp = SOCK.recv(2048).decode('utf-8')
    except socket.error:
        resp = ''

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    
    elif len(resp) > 0:
        try:
            username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', demojize(resp)).groups()
            return f"**__{username}__ :** {message}"
        except Exception:
            pass

async def twitch(discord_chan):
    await bot.wait_until_ready()
    while bot.is_ready:
        msg = get_msg()
        if msg != None:
            await discord_chan.send(msg)
        await asyncio.sleep(1)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

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
            await ctx.send("Le pseudo est inconnu.")
    else:
        await ctx.send("Si vous essayez d'entrer un pseudo aved des espaces, veillez à l'entourer avec des guillemets.")

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
        await ctx.send('Vous ou la personne ciblée n\'êtes connecté à aucun salon.')

@bot.command()
async def chat_set(ctx, arg1, argF=None):
    global TASK
    if argF is None:
        if TASK is None:
            test = chat_init(arg1)
            if type(test) is int and test == 1:
                await ctx.send(f'```Connection à la chaine {arg1} réussie !```')
                TASK = bot.loop.create_task(twitch(ctx))
            else:
                await ctx.send(test)
        else:
            await ctx.send('```Désactivez le chat avec " $chat_stop " avant d\'en créer un nouveau !```')
    else:
        await ctx.send('```Les espaces ne sont pas tolérés. Veuillez récupérer le nom de chaine dans le lien de celle-ci, par ex "andhefallen" pour "twitch.tv/andhefallen."```')

@bot.command()
async def chat_stop(ctx):
    global TASK
    global SOCK
    if TASK is None:
        await ctx.send('```Aucun chat n\'est en cours d\'éxécution.```')
    else:
        TASK.cancel()
        TASK = None
        SOCK.shutdown(1)
        SOCK.close()
        SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await ctx.send('```Le chat a été arrêté !```')

bot.run(token_bot)