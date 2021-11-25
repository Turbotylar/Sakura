import discord
from discord.ext import commands
import datetime
from youtube_search import YoutubeSearch
import requests


class Misc(commands.Cog, name="Miscellaneous"):
    """
    Commands that do not fit into their own categories.
    """

    
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="find",
        breif="Miscellaneous commands",
        description="Miscellaneous commands"
        )
    async def find(self, ctx, *args):
        """Searches for a video on YouTube."""
        results = YoutubeSearch(str(args), max_results=1).to_dict()
        for v in results:
            await ctx.send('https://www.youtube.com' + v['url_suffix'])
    
    @commands.command()
    async def inspire(self, ctx):
        """Get some ai generated inspiration."""
        link = "http://inspirobot.me/api?generate=true"
        f = requests.get(link)
        imgurl = f.text
        embed = discord.Embed(title=("Be Inspired!"), color=0xeb34cf)
        embed.set_image(url=imgurl)
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        if ctx.content.startswith("wait"):
                await ctx.channel.send("Too late!")
        elif ctx.content.startswith("^"):
                await ctx.channel.send("^")
        elif ctx.content.startswith.send("true"):
                await ctx.channel.send("Very true")

    
    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def test(self, ctx):
        """Random role for testing."""
        server = ctx.message.guild
        perms = discord.Permissions(manage_events=True)
        await self.create_role(server, name='Test', permissions=perms)
    
    @commands.command()
    async def eatan(self, ctx):
        embed = discord.Embed(color=0xeb34cf)
        embed.set_image(url="https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/aurora-bloom-2-jpg-1579817827.jpg")
        await ctx.send(embed=embed)
        
        
def setup(bot):
    bot.add_cog(Misc(bot))
