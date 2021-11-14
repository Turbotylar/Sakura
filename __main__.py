#Import all required libraries
from __future__ import unicode_literals
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
    "cogs.error",
    "cogs.manage",
    "cogs.music",
    "cogs.redditgive",
    "cogs.tenorget",
    "cogs.misc",
    "cogs.interactions",
    "cogs.moderation",
    "cogs.stats"
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

@bot.command()
async def eatan(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/815655064953552896/901593012130422824/Remini20211009110734720.jpg")

#If perks speaks, mute him for 20 seconds
@bot.listen()
async def on_message(message):    
    if str(message.author) == 'PerksOCE#7956':
        author = message.author
        muted = message.guild.get_role(875284225111248917)
        await author.add_roles(muted)
        await asyncio.sleep(20)
        await author.remove_roles(muted)


    

with open("config.json") as f:
        bot.config = json.load(f)

bot.run(bot.config["bot_api_key"])
