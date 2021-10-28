import discord
from discord.ext import commands
from discord_components import DiscordComponents, Select, SelectOption, Button, ButtonStyle
from discord.utils import get

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print('Connected')

@bot.command()
async def sm(ctx):
    if ctx.author.id == 670325098598629377 or 426376741028888576:
        await ctx.send(
    '>>> Text',
    components = [
    Select(
        placeholder = 'SelectMenu',
        options = [
            SelectOption(label="SelectMenu1", value="value1"),
            SelectOption(label="SelectMenu2", value="value2"),
            SelectOption(label="SelectMenu3", value="value3"),
            SelectOption(label = "SelectMenu4", value = "value4"),
            SelectOption(label="SelectMenu5", value="value5"),
            SelectOption(label="SelectMenu6", value="value6"),
            SelectOption(label = "SelectMenu7", value = "value7"),
            SelectOption(label = "SelectMenu8", value = "value8")
            ])])

@bot.event
async def on_select_option(interaction):
    if interaction.message.id == 891587821368905728: #Message id(not obligatory)
        await interaction.respond(type=6)
        if interaction.values[0] == "value1":
            await interaction.author.send("Menu 1")
        elif interaction.values[0] == "value2":
            await interaction.author.send("Menu 2")