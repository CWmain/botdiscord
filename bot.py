from discord import FFmpegOpusAudio
from discord.ext import commands
from discord.opus import load_opus
from json import load, dump
from discord.player import FFmpegPCMAudio
from discord.utils import get
from time import sleep
from help import allSoundsString
from ping import incrementPing, allPings
from theme import themeSong, themeUpdate, themeCurrent
import HexToAscii as h
import botInfo

TOKEN = botInfo.BOTSTRING

CONNECTED = {'channel': None, 'voice_client': None}
CURRENT_USERS = {}
QUEUE = []

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('Bot is ready.')


# @client.event
# async def on_socket_raw_receive(msg):
#     print(msg)
#     print("The above was recieved!")

@client.event
async def on_voice_state_update(token, before, after):
    global CONNECTED
    global CURRENT_USERS

    user = str(token)

    #If its the bot, do nothing
    if user == 'FunnySounds#5784':
        return

    previous_channel = before.channel
    channel = after.channel


    #If user is joinging channel None, it means that they left the voice channel
    if channel == None:
        #Attempt to remove them from CURRENT_USERS
        #If this fails, it means they were already in the server when the bot was turned on
        try:
            CURRENT_USERS[previous_channel].remove(user)
            print(f"User {user} left {previous_channel}")
        except:
            print(f"User {user} wasn't already joined")
       
        return

    print(f'{user} joined {channel}')
    #If a new channel is entered, add a new dict entry
    if channel not in CURRENT_USERS.keys():
        CURRENT_USERS[channel] = []

    #If user is already in channel do nothing
    if user in CURRENT_USERS[channel]:
        print(f'{user} already in channel')
        return
    #Else
    #Removes from previously joined channel if it exsists
    try:
        CURRENT_USERS[previous_channel].remove(user)
    except:
        print(f"User {user} didn't move between channels")
    #Adds them to currently joined channel
    CURRENT_USERS[channel].append(user)


    #Attempts to join a voice channel, if this fails disconnects and trys again
    print(f"Joining channel {channel}")

    print("Attempting to connect")
    voice_client = await channel.connect()
    
    toPlay = themeSong(user)
    
    print("Creating FFmpegPCMAudio")
    voice_client.play(FFmpegPCMAudio(source=toPlay))

    print(f'Started Playing {toPlay} for {user}')
    
    while voice_client.is_playing() == True:
        sleep(1)
    print(f'Finished Playing {toPlay} for {user}')
    
    sleep(5)
    
    for v_client in client.voice_clients:
        await v_client.disconnect(force=True)
    
    print(f"Bot has left {channel}")

    return

@client.command()
async def ping(ctx, *args):

    user = str(ctx.author)
    incrementPing(user, 1)


    print(f'Ping request from {user}')

    if len(args) == 0:
        await ctx.send('pong')
        return

    for argv in args:
        incrementPing(user, 1)
        msg = 'pong ' + argv
        await ctx.send(msg)

@client.command()
async def theme(ctx, *args):
    user = str(ctx.author)

    #If no arguments are given, send users current theme
    if len(args) == 0:
        print(f"Sending {user} their current theme")
        message = 'Your theme is: ' + themeCurrent(user)
        await ctx.send(message)
        return

    #If the second argument is help, send all current sounds
    if args[0] == 'help':
        print(f"{user} is requesting all sounds")
        message = allSoundsString()
        await ctx.send(message)
        return

    #If the second argument is set, 3rd argument is the theme name to be set
    if args[0] == 'set':
        if len(args) == 1:
            print(f"{user} didn't give theme to set")
            message = 'theme set requires an argument'
            await ctx.send(message)
            return
        #If theme set if giving more than two arguments, prints error message than close
        if len(args) > 2:
            print(f"{user}'s gave theme set to many arguments")
            message = 'theme set only takes one argument'
            await ctx.send(message)
            return

        #Attempts to update theme, if KeyError('Sound dosen't exsist), send error and exit
        try:
            themeUpdate(user, args[1])
            print(f"Updated {user}'s theme to {args[1]}")
            message = user + "'s theme was updated to " + args[1]

        except KeyError:
            print(f"Attempted to update {user}'s theme to {args[1]}, {args[1]} isn't a valid sound")
            message = args[1] + " isn't a valid sound"

        await ctx.send(message)
        return

    print(f"{user} used .theme wrong (like an idiot)")
    message = 'You did it wrong'
    await ctx.send(message)
    return

@client.command()
async def score(ctx):

    SCORES = allPings()

    msg = 'The current ping count is:\n'
    for i in SCORES:
        temp =  str(SCORES[i]) + ': '
        temp = temp.rjust(15)
        msg += temp + '**' + str(i) + '**' + '\n'

    print(msg)
    await ctx.send(msg)

@client.command()
async def quirk(ctx):
    await ctx.send('All might')

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    for c in ctx.guild.voice_channels:
        print(c)
    await channel.connect()


@client.command()
async def prank(ctx):
    user = ctx.author
    print(f"{user} is pranking someone!")
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    source = await FFmpegOpusAudio.from_probe("sounds/hello.mp3")
    voice_client.play(source)

    i = 0
    while i < 3:

        if voice_client.is_playing() is False:
            source = await FFmpegOpusAudio.from_probe("sounds/hello.mp3")
            voice_client.play(source)

        sleep(3)
        i += 1

    sleep(5)
    await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, audio):

    user = ctx.author

    if audio == 'help':
        print(f"{user} is requesting all sounds")
        message = allSoundsString()
        await ctx.send(message)
        return


    print(f"{user} is playing {audio}.mp3")
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    to_probe = 'sounds\\' + audio + '.mp3'
    try:
        source = await FFmpegOpusAudio.from_probe(to_probe)
        voice_client.play(source)
    except:
        print('File does not exsist')

    while voice_client.is_playing() is True:
        sleep(1)
    sleep(10)
    await ctx.voice_client.disconnect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()



client.run(TOKEN)
