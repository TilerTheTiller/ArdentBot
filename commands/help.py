import discord
import index
from discord.ext import commands


class Help(commands.Cog):
    """Get all modules and commands"""
    def __init__(self, client):
        self.client = client

    # commands
    @commands.command()
    @commands.check(index.InBotsChannel)
    @commands.guild_only()
    async def help(self, ctx, *cog):
        if not cog:
            embed = discord.Embed(color=index.PrimaryColor)
            cog_desc = ''
            embed.set_author(name=f'{self.client.user.name} Help', icon_url=self.client.user.avatar_url, url='https://driedsponge.net')
            skipped = ['Events', 'Help']
            for x in self.client.cogs:
                if x in skipped:
                    continue
                embed.add_field(name=f'**{x}**', value=f'**`{index.data["prefix"]}help {x}`**')
            # cog_desc += f'**{x}** - {self.client.cogs[x].__doc__}\n'
            await ctx.send(embed=embed)
        else:
            if len(cog) > 1:
                embed = discord.Embed(title='Error', description='Too may cogs!')
                await ctx.send('', embed=embed)
            else:
                found = False
                for x in self.client.cogs:
                    for y in cog:
                        if x == y:
                            embed = discord.Embed(title=f'{y} Module', color=index.PrimaryColor)
                            scog_desc = ''
                            for c in self.client.get_cog(y).get_commands():
                                if not c.hidden:
                                    scog_desc += f'**`{index.data["prefix"]}{c.qualified_name} {c.signature}`** - {c.help}\n\n'
                                    # embed.add_field(name=f'`!{c.qualified_name} {c.signature}`', value=f'{c.help}',
                                    # inline=False)
                            found = True
                            embed.set_author(name='DriedSponge.net Help', icon_url=self.client.user.avatar_url, url='https://driedsponge.net')
                            embed.description = scog_desc
                if not found:
                    for x in self.client.cogs:
                        for c in self.client.get_cog(x).get_commands():
                            if c.name == cog[0]:
                                embed = discord.Embed(title=f'{c.name} command', color=index.PrimaryColor)
                                embed.description = f'**`{index.data["prefix"]}{c.qualified_name} {c.signature}`** - {c.help}\n\n'
                                # embed.add_field(name=f'{c.name} - {c.help}', value=f'Proper Syntax: !{
                                # c.qualified_name} {c.signature}')
                                embed.set_author(name='DriedSponge.net Help', icon_url=self.client.user.avatar_url,
                                                 url='https://driedsponge.net')
                        found = True
                        if not found:
                            embed = discord.Embed(description='Broken')
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
