#Import all required libraries
from __future__ import unicode_literals
from sqlalchemy import create_engine
import discord
from discord.ext import commands
import asyncio
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
    "cogs.database",
    "cogs.error",
    "cogs.manage",
    "cogs.music",
    "cogs.reddit",
    "cogs.tenor",
    "cogs.misc",
    "cogs.interactions",
    "cogs.moderation",
    "cogs.stats",
    "cogs.help",
    "cogs.weather"
]

#Setup bot with prefix and intents
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

#On startup print bots name and set presence
@bot.event
async def on_ready():
    print(f"Now logged in as {bot.user.name}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("https://github.com/Turbotylar/LoliBot"))


#Load Extentions and commands
if __name__ == "__main__":
    for ext in startup_cogs:
        try:
            bot.load_extension(ext)
        except Exception as e:
            print(e)
    
    for cog_name in bot.cogs:
        cog = bot.get_cog(cog_name)
        for command in cog.get_commands():
            print(command)
        

#If perks speaks, mute him for 20 seconds
@bot.listen()
async def on_message(message):    
    if str(message.author) == 'PerksOCE#7956':
        author = message.author
        muted = message.guild.get_role(bot.config["mute_role"])
        await author.add_roles(muted)
        await asyncio.sleep(20)
        await author.remove_roles(muted)

    

with open("config.json") as f:
    bot.config = json.load(f)

engine = create_engine("sqlite+pysqlite:///lolibot.db", echo=True)
bot.db_engine = engine

bot.run(bot.config["bot_api_key"])
