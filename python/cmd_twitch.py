import discord
import asyncio
import socket
import re
from private import ID_TWITCH, TOKEN_TWITCH, SERVER, PORT, NICKNAME
from discord.ext import tasks, commands
from discord.ext.commands.cooldowns import BucketType
from emoji import demojize
from twitch import TwitchClient


twitch_client = TwitchClient(client_id=ID_TWITCH, oauth_token=TOKEN_TWITCH)
chats = dict()


def check_user(name):
    user = twitch_client.users.translate_usernames_to_ids([name])
    if not user:
        return False
    return True


class ChatObj:
    def __init__(self, twitch_user, discord_channel, bot):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.twitch_user = twitch_user
        self.discord_channel = discord_channel
        self.bot = bot
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
        await self.bot.wait_until_ready()
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


class TwitchCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chat_set(self, ctx, arg1):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        what_channel = ctx.channel
        if what_channel in list(chats):
            await ctx.send("```A chat is already active, you have to stop it before with the cmd $chat_stop !```")
        else:
            if check_user(arg1):
                obj = ChatObj(arg1, what_channel, self.bot)
                if obj.chat_init():
                    await ctx.send(f'```Now connected to {arg1}\'s twitch channel !```')
                    obj.twitch.start()
                else:
                    await ctx.send('```Something went wrong when trying to access Twitch IRC.```')
            else:
                await ctx.send('```This twitch channel doesn\'t seems to exist.```')


    @commands.command()
    async def chat_stop(self, ctx):
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        chan = ctx.channel
        if chan in list(chats):
            chats[chan].twitch.stop()
            del chats[chan]
            await asyncio.sleep(1)
            message = '```The chat was successfully stopped !```'
        else:
            message = '```There is no active chat in this channel.```'
        await ctx.send(message)


def setup(bot):
    bot.add_cog(TwitchCmds(bot))