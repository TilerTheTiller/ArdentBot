import discord
import json
import index
import datetime
import requests
from discord.ext import commands


class General(commands.Cog):
    """General Commands"""

    def __init__(self, client):
        self.client = client

    # Ping
    @commands.command()
    @commands.check(index.InBotsChannel)
    @commands.guild_only()
    async def ping(self, ctx):
        """Pong! (get the bots ping)"""
        embed = discord.Embed(title=':ping_pong:  Pong!',
                              color=index.PrimaryColor)
        embed.add_field(name='Ping', value=f'{round(self.client.latency * 1000)}ms')
        await ctx.send(embed=embed)

    # Creator
    @commands.command()
    @commands.check(index.InBotsChannel)
    @commands.guild_only()
    async def creator(self, ctx):
        """Gets information about the creator of the bot"""
        embed = discord.Embed(title='Bot Creator',
                              color=index.PrimaryColor)
        embed.description = f'**This bot was created by DriedSponge#4730**\nMy Website: https://driedsponge.net\nMy Steam: https://steamcommunity.com/id/driedsponge/\n\n**Feel free to reach out if you would like your own bot!**'
        await ctx.send(embed=embed)

    # Status Command
    @commands.command()
    @commands.check(index.InBotsChannel)
    @commands.guild_only()
    async def status(self, ctx):
        """Get the status of the server"""
        with open('scoreboard.json') as fole:
            midon = json.load(fole)
        URL = f'https://driedsponge.net/api/source-query/info?'
        PARAMS = {'api_token': index.data['apikey'], 'server_ip': midon['ip'], 'server_port': midon['port']}
        r = requests.get(url=URL, params=PARAMS).json()
        if r['success']:
            data = r['data']['server_info']
            embed = discord.Embed(title=data["HostName"], color=0x43B581)
            embed.description = f'Connect: steam://connect/{midon["ip"]}:{midon["port"]}'
            embed.set_thumbnail(url=index.LogoURL)
            embed.add_field(name='Players', value=f'**`{data["Players"]}/{data["MaxPlayers"]}`**')
            embed.add_field(name='Map', value=f'**`{data["Map"]}`**')
            embed.add_field(name='Gamemode', value=f'**`{data["ModDesc"]}`**')
            embed.timestamp = datetime.datetime.utcnow()
        else:
            embed = discord.Embed(title="Server Offline", color=0xF04747)
            embed.description = f'Could not connect to server'
            embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(General(client))
