import discord
from discord.ext import commands
import datetime
import pytz
from youtube_search import YoutubeSearch
import requests


class Misc(commands.Cog, name="Miscellaneous"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="today",
        breif="Miscellaneous commands",
        description="Miscellaneous commands"
        )
    #>today returns current day in NZT
    async def today(self, ctx, arg):        
        day = datetime.datetime.now(pytz.timezone(str(arg)))
        await ctx.send(day.strftime("%A %B %d %Y \nTime: %H:%M:%S"))


    @commands.command(
        name="find",
        breif="Miscellaneous commands",
        description="Miscellaneous commands"
        )
    #>find will search for a related video on youtube
    async def find(self, ctx, *args):
        results = YoutubeSearch(str(args), max_results=1).to_dict()
        for v in results:
            await ctx.send('https://www.youtube.com' + v['url_suffix'])
    
    @commands.command()
    async def inspire(self, ctx):
        link = "http://inspirobot.me/api?generate=true"
        f = requests.get(link)
        imgurl = f.text
        await ctx.send(imgurl)
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content.startswith("^"):
            if not str(ctx.author) == "Loli Bot#6575":
                await ctx.channel.send("^")
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content.startswith("wait"):
            await ctx.channel.send("Too late!")
    
    @commands.command()
    async def ping(self, ctx):
	    await ctx.send(f'Pong! {round(self.client.latency * 1000)}')

def setup(bot):
    bot.add_cog(Misc(bot))