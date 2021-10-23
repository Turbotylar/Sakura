from __future__ import unicode_literals
import os
import discord
from praw_ import praw_login
import datetime
#from discord.ext.commands.core import has_permissions, has_any_role
from discord.ext import commands
import asyncio
from youtube_search import YoutubeSearch


#Declare intents
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>')


@bot.event
async def on_ready():
    print(f"Now logged in as {bot.user.name}")
    bot.load_extension("cogs.music")

@bot.command()
async def give(ctx, arg):
    try:
        if arg == 'loli':
            praw_login('cutelittlefangs')
            await ctx.send("Here is your loli: <:Lozic:854911358114332683>")
            await ctx.send(file=discord.File('image.png'))
        elif arg == 'cat':
            praw_login('cat')
            await ctx.send("Here is your cat:")
            await ctx.send(file=discord.File('image.png'))
        elif arg == 'kat':
            praw_login('KatarinaMains')
            await ctx.send("Here is your cat:")
        elif arg == 'yuumi':
            praw_login('YuumiMains')
            await ctx.send("Here is your cat:")
            await ctx.send(file=discord.File('image.png')) 
    except Exception as e:
        await ctx.send(e)

@bot.command()
async def today(ctx):
    day = datetime.date.today()
    await ctx.send(day.strftime("%A %B %d %Y"))    

@bot.listen()
async def on_message(message):    
    #If perks speaks, mute him for 20 seconds
    if str(message.author) == 'PerksOCE#7956':
        author = message.author
        muted = message.guild.get_role(875284225111248917)
        await author.add_roles(muted)
        await asyncio.sleep(20)
        await author.remove_roles(muted)

@bot.command()
async def find(ctx, arg):
    search = str(arg)
    results = YoutubeSearch(str(search), max_results=1).to_dict()
    for v in results:
        await ctx.send('https://www.youtube.com' + v['url_suffix'])
    

bot.run(os.environ.get("DISCORD_API_KEY"))
