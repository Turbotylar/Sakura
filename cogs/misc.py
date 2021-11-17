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
        name="find",
        breif="Miscellaneous commands",
        description="Miscellaneous commands"
        )
    async def find(self, ctx, *args):
        """ Searches for a video on YouTube """
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
        if ctx.author.bot:
            return
        if ctx.content.startswith("wait"):
                await ctx.channel.send("Too late!")
        elif ctx.content.startswith("^"):
                await ctx.channel.send("^")
    
    @commands.command()
    async def ping(self, ctx):
	    await ctx.send(f'Pong! {round(self.client.latency * 1000)}')

    @commands.command()
    async def test(self, ctx):
        server = ctx.message.guild
        perms = discord.Permissions(manage_events=True)
        await self.create_role(server, name='Test', permissions=perms)

def setup(bot):
    bot.add_cog(Misc(bot))
