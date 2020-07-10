import discord
import json
import index
import datetime
import requests
from discord.ext import commands


class Administration(commands.Cog):
    """Administration Commands"""

    def __init__(self, client):
        self.client = client

    # Dev Log Command
    @commands.command(aliases=['dev-log', 'dlog'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def devlog(self, ctx, title: str = 'New Development Log', *, msg: str = 'No Changes'):
        """Create a new dev log"""
        embed = discord.Embed(title=title,
                              color=index.PrimaryColor)
        embed.description = msg
        embed.set_author(name=f'New Dev Log From {ctx.author.name}', icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        role = discord.utils.get(ctx.message.guild.roles, name='Server Updates')
        if role is None:
            role = await ctx.message.guild.create_role(name='Server Updates')
        await ctx.message.delete()
        await ctx.send(content=role.mention, embed=embed)

    # Dev Log Command
    @commands.command(aliases=['events'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def event(self, ctx, title: str = 'New Event', *, msg=None):
        """Announce an event"""
        embed = discord.Embed(title=title,
                              color=index.PrimaryColor)
        if msg is not None:
            embed.description = msg
        embed.set_author(name=f'{ctx.author.name} - New Event', icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        role = discord.utils.get(ctx.message.guild.roles, name='Events')
        if role is None:
            role = await ctx.message.guild.create_role(name='Events')
        await ctx.message.delete()
        await ctx.send(content=role.mention, embed=embed)

    # Poll Command
    @commands.command(aliases=['new-poll'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def poll(self, ctx, title: str = 'New Poll', *, msg: str = None):
        """Open a poll where users can vote"""
        embed = discord.Embed(title=title,
                              color=index.PrimaryColor)
        embed.description = msg
        embed.set_footer(text=f'Opened by {index.UTag(ctx.author)}', icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.message.delete()
        role = discord.utils.get(ctx.message.guild.roles, name='Polls')
        if role is None:
            role = await ctx.message.guild.create_role(name='Polls')
        poll = await ctx.send(content=role.mention, embed=embed)
        await poll.add_reaction('\U00002705')
        await poll.add_reaction('\U0001f6ab')


def setup(client):
    client.add_cog(Administration(client))
