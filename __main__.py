#Import all required libraries
from __future__ import unicode_literals
import discord
import datetime
from discord.ext import commands
import asyncio
from youtube_search import YoutubeSearch
import json

#Declare intents
intents = discord.Intents.default()
intents.members = True

#Get Prefix from config
def get_prefix(bot, message):
    prefixes = bot.config["prefixes"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

#List of cogs
startup_cogs = [
    "cogs.error",
    "cogs.manage",
    "cogs.music",
    "cogs.redditgive",
    "cogs.tenorget"
]

#Setup bot with prefix and intents
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

#On startup print bots name and set presence
@bot.event
async def on_ready():
    print(f"Now logged in as {bot.user.name}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("https://github.com/Turbotylar/LoliBot"))


#Load Extentions and commands
if __name__ == "__main__":
    for ext in startup_cogs:
        bot.load_extension(ext)
    
    for cog_name in bot.cogs:
        cog = bot.get_cog(cog_name)
        for command in cog.get_commands():
            print(command)

#>today returns current day in NZT
@bot.command()
async def today(ctx):
    day = datetime.date.today()
    await ctx.send(day.strftime("%A %B %d %Y"))    

#If perks speaks, mute him for 20 seconds
@bot.listen()
async def on_message(message):    
    if str(message.author) == 'PerksOCE#7956':
        author = message.author
        muted = message.guild.get_role(875284225111248917)
        await author.add_roles(muted)
        await asyncio.sleep(20)
        await author.remove_roles(muted)

#>find will search for a related video on youtube
@bot.command()
async def find(ctx, arg):
    search = str(arg)
    results = YoutubeSearch(str(search), max_results=1).to_dict()
    for v in results:
        await ctx.send('https://www.youtube.com' + v['url_suffix'])
    

with open("config.json") as f:
        bot.config = json.load(f)

bot.run(bot.config["bot_api_key"])