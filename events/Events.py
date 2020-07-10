import discord
import random
import datetime
import index
import json
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcomech = member.guild.system_channel
        embed = discord.Embed(title='User Joined',
                              description=f'{member.mention} joined {member.guild.name}, Welcome brother!',
                              color=0x166CD4)
        await welcomech.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcomech = member.guild.system_channel
        embed = discord.Embed(title='User Left',
                              description=f'{member.mention} left {member.guild.name}, **_Traitor_**',
                              color=0xFF4040)
        await welcomech.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f'Please use this command in the server')
        # if isinstance(error, commands.CommandNotFound):
        #     response = await ctx.send(f'{ctx.author.mention} That command does not exist')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} You do not have permission to use that command')
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'{ctx.author.mention} I do not have permission to do this')
        if isinstance(error, commands.NotOwner):
            await ctx.send(f'{ctx.author.mention} You must be the owner of the bot to perform this action')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        with open('reaction.json') as fole:
            midon = json.load(fole)
        message_id = payload.message_id
        channel_id = payload.channel_id
        if message_id == midon['message']:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
            found = False
            for k, v in index.roles.items():
                if payload.emoji.name == v['name']:
                    role = discord.utils.get(guild.roles, name=k)
                    if role is None:
                        role = await guild.create_role(name=k)
                    found = True
                    break
            if not found:
                return print('No roles to be assigned')
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if not member.bot:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        with open('reaction.json') as fole:
            midon = json.load(fole)
        if payload.message_id == midon['message']:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
            found = False
            for k, v in index.roles.items():
                if payload.emoji.name == v['name']:
                    role = discord.utils.get(guild.roles, name=k)
                    found = True
                    break
            if not found:
                return print('No roles to be removed')
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if not member.bot:
                    await member.remove_roles(role)


def setup(client):
    client.add_cog(Events(client))
