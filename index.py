import json
import discord
import requests
from discord.ext import tasks
import datetime
import os
from discord.ext import commands

with open('botinfo.json') as file:
    data = json.load(file)

client = commands.Bot(command_prefix=data['prefix'])

client.remove_command('help')

PrimaryColor = 0xFF69B4

LogoURL = "https://i.driedsponge.net/images/png/kTyZc.png"

roles = {'Updates':
             {'name': '🔔', 'id': '\U0001f514'},
         'Polls':
             {'name': '🗳', 'id': '\U0001f5f3'},
         'Server Updates':
             {'name': '🎮', 'id': '\U0001f3ae'},
         'Events':
             {'name': '📆', 'id': '\U0001f4c6'}
         }


async def InBotsChannel(ctx):
    with open('config.json') as fole:
        midon = json.load(fole)
    botcmds = client.get_channel(midon['bot-cmd-channel'])
    if botcmds:
        if ctx.channel.id == midon['bot-cmd-channel']:
            return True
        else:
            await ctx.send(f'{ctx.author.mention} Please use the {botcmds.mention} channel')
            return False
    else:
        embed = discord.Embed(title='Configuration Error', color=0xFF4040)
        embed.description = f'There is no bot commands channel set, or the current channel is invalid. Please run `{data["prefix"]}botcmds` in the desired channel to set it as the bot commands channel!'
        await ctx.send(embed=embed)


def UTag(member):
    return f'{member.name}#{member.discriminator}'


for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')
        print(f'{filename} loaded!')

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        client.load_extension(f'events.{filename[:-3]}')
        print(f'{filename} loaded!')


@client.event
async def on_message(message):
    if not message.author.bot:
        with open('config.json') as fole:
            midon = json.load(fole)
        if message.channel.id == midon['suggestion-channel']:
            embed = discord.Embed(title='Suggestion', color=PrimaryColor, description=message.content)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Suggested by {UTag(message.author)}', icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
            await message.delete()
        await client.process_commands(message)


@tasks.loop(seconds=300)
async def update():
    with open('botinfo.json') as file:
        dataa = json.load(file)
    with open('scoreboard.json') as fole:
        midon = json.load(fole)
    channel = client.get_channel(midon['channel'])
    if channel is not None:
        URL = f'https://driedsponge.net/api/source-query/all'
        PARAMS = {'api_token': dataa['apikey'], 'server_ip': midon['ip'], 'server_port': midon['port']}
        req = requests.get(url=URL, params=PARAMS)
        r = req.json()
        status = req.status_code
        max_players = 10
        try:
            print('message not found')
            message = await channel.fetch_message(midon['message'])
            if r['success']:
                stats = r['data']['server_info']
                embed = discord.Embed(title=stats["HostName"], color=0x43B581)
                embed_desc = f'Connect: steam://connect/{midon["ip"]}:{midon["port"]}\n\nShowing **{max_players}** players\n\n'
                loop_count = 0
                for x in r['data']['server_players']:
                    if loop_count <= max_players:
                        loop_count += 1
                        embed_desc += f'**{x["Name"]}**\nKills: **{x["Frags"]}**\nSession Time: **{x["TimeF"]}**\n--------------------------\n'
                    else:
                        additional = stats["Players"] - 10
                        embed_desc += f'Along with **{additional}** other players'
                        break
                embed.description = embed_desc
                embed.set_thumbnail(url=LogoURL)
                embed.add_field(name='Players', value=f'**`{stats["Players"]}/{stats["MaxPlayers"]}`**')
                embed.add_field(name='Map', value=f'**`{stats["Map"]}`**')
                embed.add_field(name='Gamemode', value=f'**`{stats["ModDesc"]}`**')
            else:
                embed = discord.Embed(title="Server Offline", color=0xF04747)
                embed.description = f'Could not connect to server'
            embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=embed)
        except discord.errors.HTTPException:
            if r['success']:
                stats = r['data']['server_info']
                embed = discord.Embed(title=stats["HostName"], color=0x43B581)
                embed_desc = f'Connect: steam://connect/{midon["ip"]}:{midon["port"]}\n\nShowing **{max_players}** players\n\n'
                loop_count = 0
                for x in r['data']['server_players']:
                    if loop_count <= max_players:
                        loop_count += 1
                        embed_desc += f'**{x["Name"]}**\nKills: **{x["Frags"]}**\nSession Time: **{x["TimeF"]}**\n--------------------------\n'
                    else:
                        additional = stats["Players"] - 10
                        embed_desc += f'Along with **{additional}** other players'
                        break
                embed.description = embed_desc
                embed.set_thumbnail(url=LogoURL)
                embed.add_field(name='Players', value=f'**`{stats["Players"]}/{stats["MaxPlayers"]}`**')
                embed.add_field(name='Map', value=f'**`{stats["Map"]}`**')
                embed.add_field(name='Gamemode', value=f'**`{stats["ModDesc"]}`**')
            else:
                embed = discord.Embed(title="Server Offline", color=0xF04747)
                embed.description = f'Could not connect to server'
            embed.timestamp = datetime.datetime.utcnow()
            message = await channel.send(embed=embed)
            NewChannel = {
                "channel": midon['channel'],
                "port": midon['port'],
                "ip": midon['ip'],
                "message": message.id,
            }
            with open('scoreboard.json', 'w') as json_file:
                json.dump(NewChannel, json_file)


update.start()


@client.event
async def on_ready():
    print('Bot is ready')


client.run(data['token'])
