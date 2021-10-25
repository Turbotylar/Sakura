import discord
from discord.ext import commands
from discord import *
from __main__ import bot
from discord_components import *

class MemberInteractions(commands.Cog, name="Member Interactions"):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def question(self, ctx):
        msg_with_selects = await ctx.send('How are you feeling today?', components=[
            [
                    Select(custom_id='_select_it', options=[
                    SelectOption(emoji='😋', label='Sad', value='1', description='The sadness envelopes you'),
                    SelectOption(emoji='😋', label='Cheerful', value='2', description='Laughter is contagious'),
                    SelectOption(emoji='😋', label='Happy', value='3', description='Happiness is they key to a good life'),
                    SelectOption(emoji='😋', label='Embarrased', value='4', description='We all feel it sometimes')],
                            placeholder='Select some Options', max_values=1)
                ]])

        def check_selection(i: discord.Interaction, select_menu):
            return i.author == ctx.author and i.message == msg_with_selects

        interaction, select_menu = await bot.wait_for('selection_select', check=check_selection)

        embed = discord.Embed(title='You have chosen:',
                                description=f"You have chosen "+'\n'.join([f'\nOption Nr° {o}' for o in select_menu.values]),
                                color=discord.Color.random())
        await interaction.respond(embed=embed)


def setup(bot):
    bot.add_cog(MemberInteractions(bot))