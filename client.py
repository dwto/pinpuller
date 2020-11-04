# bot.py
import os
import discord 
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='archiveChannel', help='Archives current channel pins to immortan-joe-pins')
async def archive(ctx):
    archiveChannelName = 'immortan-joe-pins'
    guild = ctx.guild
    channel = ctx.channel

    message_header = 'https://cdn.discordapp.com/attachments/773308045840875524/773355611983052830/unknown.png'
    message_footer = 'https://cdn.discordapp.com/attachments/773325088866041876/773356754485510194/unknown.png'

    print(f'guild: {guild.id}')
    print(f'channel: {channel.id}')

    # Check if archive channel exists
    existing_archive_channel = discord.utils.get(guild.channels, name=archiveChannelName)
    if not existing_archive_channel:
        print(f'Channel doesnt exist: {archiveChannelName}')
        await ctx.send(f'Channel doesnt exist: {archiveChannelName}')

    pins = await channel.pins() 
    print(pins)

    message_url_head = 'https://discord.com/channels'

    for pin in pins[::-1]:
        # message link = https://discord.com/channels/guild_id/channel_id/message_id
        print(f'id: {pin.id} content:{pin.content} url:{message_url_head}/{guild.id}/{channel.id}/{pin.id}')
        message_url = "{}/{}/{}/{}".format(message_url_head, guild.id, channel.id, pin.id)
        #archive_message = "> {}\n<@{}> in channel <#{}> on {}UTC\n{}".format(pin.content, pin.author.id, pin.channel.id, pin.created_at, message_url)
        archive_message = "> {}\n@{} in channel #{} on {}UTC\n{}".format(pin.content, pin.author.id, pin.channel.id, pin.created_at, message_url)
        print(f'{archive_message}')
        #await existing_archive_channel.send(message_header)
        await existing_archive_channel.send(archive_message)
        #await existing_archive_channel.send(message_footer)
    print(f'DONE:{channel.name}')
        

@bot.command(name='archiveAllChannels', help='Archives all text channel pins to immortan-joe-pins')
async def archive(ctx):
    archiveChannelName = 'immortan-joe-pins'
    guild = ctx.guild
    print(f'{guild.id}')

    message_header = 'https://cdn.discordapp.com/attachments/773308045840875524/773355611983052830/unknown.png'
    message_footer = 'https://cdn.discordapp.com/attachments/773325088866041876/773356754485510194/unknown.png'

    # Check if archive channel exists
    existing_archive_channel = discord.utils.get(guild.channels, name=archiveChannelName)
    if not existing_archive_channel:
        print(f'Channel doesnt exist: {archiveChannelName}')
        await ctx.send(f'Channel doesnt exist: {archiveChannelName}')

    for channel in guild.text_channels:
        message_url_head = 'https://discord.com/channels'
        print(f'Pins for {channel.name}')

        pins = await channel.pins() 
        print(pins)

        for pin in pins[::-1]:
            # message link = https://discord.com/channels/guild_id/channel_id/message_id
            print(f'id: {pin.id} content:{pin.content} url:{message_url_head}/{guild.id}/{channel.id}/{pin.id}')
            message_url = "{}/{}/{}/{}".format(message_url_head, guild.id, channel.id, pin.id)
            #archive_message = "> {}\n<@{}> in channel <#{}> on {}UTC\n".format(pin.content, pin.author.id, pin.channel.id, pin.created_at, message_url)
            archive_message = "> {}\n@{} in channel #{} on {}UTC\n".format(pin.content, pin.author.id, pin.channel.id, pin.created_at, message_url)
            print(f'{archive_message}')
            #await existing_archive_channel.send(message_header)
            await existing_archive_channel.send(archive_message)
            #await existing_archive_channel.send(message_footer)
        print('')

    print(f'DONE:{channel.name}')
        

bot.run(TOKEN)