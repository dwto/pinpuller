# bot.py
import os
import discord 
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

archive_channel_name = "immortan-joe-pins"

##############
# Events 
##############

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Watches for new pins, ignore unpinning 
@bot.event
async def on_guild_channel_pins_update(channel, last_pin):
    if not last_pin:
        print(f'message was unpinned')
        return 

    print('Pin updated')

    pins = await channel.pins()
    await generate_archive(channel.guild, channel, [pins[-1]])

##############
# Commands 
##############

@bot.command(name="getArchiveChannel", help="get the name of the archive channel")
async def getArchiveChannel(ctx):
    print(f'Archive Channel: {archive_channel_name}')
    await ctx.channel.send(f"Archive Channel: {archive_channel_name}")

@bot.command(name="setArchiveChannel", help="set the name of the archive channel")
async def setArchiveChannel(ctx, name):
    global archive_channel_name 
    archive_channel_name = name
    print(f'Archive Channel: {archive_channel_name}')
    await ctx.channel.send(f"Set Archive Channel: {archive_channel_name}")

@bot.command(name='archiveChannel', help='Archives current text channel pins to archive_channel')
async def archive(ctx):
    guild = ctx.guild
    print(f'!archiveChannel guild: {guild.id} channel: {ctx.channel.id} archive: {archive_channel_name}')

    await check_channel(guild)

    pins = await ctx.channel.pins() 
    print(pins)

    await generate_archive(guild, ctx.channel, pins)

    print(f'DONE:{ctx.channel.name}')
        

@bot.command(name='archiveAllChannels', help='Archives all text channel pins to archive_channel')
async def archive(ctx):
    guild = ctx.guild
    print(f'!archiveAllChannels guild: {guild.id} archive: {archive_channel_name}')

    await check_channel(guild)

    for channel in guild.text_channels:
        print(f'Pins for {channel.name}')

        pins = await channel.pins() 
        print(pins)

        await generate_archive(guild, channel, pins)
        print('')

    print(f'DONE:{channel.name}')

##############
# Functions 
##############

# Check if guild has channel name archive_channel_name
async def check_channel(guild):
    existing_archive_channel = discord.utils.get(guild.channels, name=archive_channel_name)
    if not existing_archive_channel:
        print(f'Channel doesnt exist: {archive_channel_name}')
        await ctx.send(f'Channel doesnt exist: {archive_channel_name}')

# Generate Archive message and send it to archive_channel_name
async def generate_archive(guild, channel, pins):

    print(f'pins: {pins}')

    if not pins:
        print(f'no pins in Channel: {channel.name}')
        return 


    message_header = 'https://cdn.discordapp.com/attachments/773308045840875524/773355611983052830/unknown.png'
    message_footer = 'https://cdn.discordapp.com/attachments/773325088866041876/773356754485510194/unknown.png'
    archive_channel = discord.utils.get(guild.channels, name=archive_channel_name)

    for pin in pins[::-1]:
        print(f'id: {pin.id} content:{pin.content} url: https://discord.com/channels/{guild.id}/{channel.id}/{pin.id}')
        message_url = "https://discord.com/channels/{}/{}/{}".format(guild.id, channel.id, pin.id)

        # enable mentions 
        #archive_message = "> {}\n<@{}> in channel <#{}> on {}UTC\n{}".format(pin.content, pin.author.id, pin.channel.id, pin.created_at, message_url)
        archive_message = "> {}\n@{} in channel #{} on {}UTC\n{}".format(pin.content, pin.author.id, pin.channel.id, pin.created_at, message_url)

        print(f'{archive_message}')
        await archive_channel.send(message_header)
        await archive_channel.send(archive_message)
        await archive_channel.send(message_footer)

# TODO:
# Remove pin from channel 
# async def remove_pin 

# TODO:
# Use pins in archive_channel to manage state of last pin in each channel
# Check if there are newer pins than latest and start archiving from there
# Max # of channels able to manage would be 50 

bot.run(TOKEN)