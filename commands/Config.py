import discord
import json
import index
import datetime
from discord.ext import commands


class Config(commands.Cog, name='Config'):
    """All things configuration!"""

    def __init__(self, client):
        self.client = client

    # Set scoreboard channel
    @commands.command(aliases=['set-scoreboard', 'score-channel'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setscoreboard(self, ctx):
        """Set the scoreboard channel"""
        with open('scoreboard.json') as fole:
            midon = json.load(fole)
        NewChannel = {
            "channel": ctx.channel.id,
            "ip": midon['ip'],
            "port": midon['port'],
            "message": midon['message'],
        }
        with open('scoreboard.json', 'w') as json_file:
            index.json.dump(NewChannel, json_file)
        await ctx.message.delete()
        response = await ctx.send(f'{ctx.channel.mention} set as scoreboard channel!')
        await response.delete(delay=4)

    # Set bot cmds channel
    @commands.command(aliases=['set-botcmds', 'bot-cmds'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def botcmds(self, ctx):
        """Set the bot commands channel"""
        with open('config.json') as fole:
            midon = json.load(fole)
        NewChannel = {
            "bot-cmd-channel": ctx.channel.id,
            "suggestion-channel": midon['suggestion-channel']
        }
        with open('config.json', 'w') as json_file:
            index.json.dump(NewChannel, json_file)
        await ctx.send(f'{ctx.channel.mention} has been set as bot commands channel!')

    # Set suggestions channel channel
    @commands.command(aliases=['set-suggestions', 'set-suggestions-channel'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setsuggestions(self, ctx):
        """Set the suggestions channel"""
        with open('config.json') as fole:
            midon = json.load(fole)
        NewChannel = {
            "suggestion-channel": ctx.channel.id,
            "bot-cmd-channel": midon['bot-cmd-channel']
        }
        with open('config.json', 'w') as json_file:
            index.json.dump(NewChannel, json_file)
        await ctx.send(f'{ctx.channel.mention} has been set as suggestions channel!')

    # Set roles channel channel
    @commands.command(aliases=['set-roles', 'set-roles-channel'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def roles(self, ctx):
        """Sends the embed for role reactions to the current"""
        await ctx.message.delete()
        embed = discord.Embed(title="Please react with the following for a role:", color=index.PrimaryColor)
        desc = ''
        for k, v in index.roles.items():
            desc += f'{v["id"]} - {k}\n'
        embed.description = desc
        roles = await ctx.send(embed=embed)
        NewChannel = {
            "channel": roles.channel.id,
            "message": roles.id,
        }
        for k, v in index.roles.items():
            role = discord.utils.get(ctx.message.guild.roles, name=k)
            if role is None:
                await ctx.message.guild.create_role(name=k)
            await roles.add_reaction(v['id'])
        with open('reaction.json', 'w') as json_file:
            index.json.dump(NewChannel, json_file)

    # Set scoreboard ip
    @commands.command(aliases=['set-ip'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setip(self, ctx, ip):
        """Set the server ip"""
        with open('scoreboard.json') as fole:
            midon = json.load(fole)
        NewChannel = {
            "channel": midon['channel'],
            "ip": ip,
            "port": midon['port'],
            "message": midon['message'],
        }
        with open('scoreboard.json', 'w') as json_file:
            index.json.dump(NewChannel, json_file)
        await ctx.send(f'The server IP has been set as: **{ip}**')

    @setip.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention} Please specify an IP!')

    # Set scoreboard port
    @commands.command(aliases=['set-port'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setport(self, ctx, port='27015'):
        """Set the server port"""
        with open('scoreboard.json') as fole:
            midon = json.load(fole)
        NewChannel = {
            "channel": midon['channel'],
            "port": port,
            "ip": midon['ip'],
            "message": midon['message'],
        }
        with open('scoreboard.json', 'w') as json_file:
            index.json.dump(NewChannel, json_file)
        await ctx.send(f'The server port has been set as: **{port}**')

    @setport.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention} Please specify a port!')


def setup(client):
    client.add_cog(Config(client))
