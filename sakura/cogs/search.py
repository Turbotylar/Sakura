import discord
from discord.ext import commands
from sakura.utils.secrets import get_secret
import TenGiphPy
import asyncpraw
import sakura
from youtube_search import YoutubeSearch
import urbandict


t = TenGiphPy.Tenor(get_secret("tenor", "api_key"))


class Search(commands.Cog, name="Search"):
    """
    Search related commands
    """
    def __init__(self, client):
        self.client = client

        self.previously_sent = []

        self.praw = asyncpraw.Reddit(
            client_id = get_secret("praw", "client_id"),
            client_secret = get_secret("praw", "client_secret"),

            username = get_secret("praw", "username"),
            password = get_secret("praw", "password"),

            user_agent = sakura.USER_AGENT
        )


    @commands.command(
        name="tenor",
        breif="Get a gif from tenor"
    )    
    
    async def tenor(self, ctx, *args):
        """Get a gif from tenor."""
        url=t.random(str(args))
        
        embed = discord.Embed(title=(str(args)), color=0xeb34cf)
        embed.set_image(url)
        await ctx.send(embed=embed)
        

    @commands.command(
        name="reddit",
        breif="Retrieve an image from reddit"
    )    
    async def reddit(self, ctx, arg):
        """Retrieve an image from reddit"""

        async with ctx.typing():
            subreddit = await self.praw.subreddit(str(arg))

            imgurl = None
            title = None

            async for submission in subreddit.hot():
                if submission.permalink not in self.previously_sent:
                    imgurl = submission.url
                    title = submission.title

            if imgurl is None or title is None:
                await ctx.send("Couldn't find any new posts on r/" + arg)
            else:
                embed = discord.Embed(title=("Here you go:"), color=0xeb34cf)
                embed.set_image(url=imgurl)
                embed.add_field(name=str(title), value=imgurl, inline=False)

                await ctx.send(embed=embed)


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

    
    @commands.command(
        name="urban",
        breif="Search urban dictionary"
    )
    async def urban(self, ctx, *args):
        """Searches for a word on urban dictionary"""
        definition = urbandict.define(str(args))
        word = definition[0]["word"]
        define = definition[0]["def"]
        example = definition[0]["example"]
        embed = discord.Embed(title=(f"Definition if {word}:"), color=0xeb34cf)
        embed.add_field(name=("Definition"), value=define, inline=False)
        embed.add_field(name=("Example"), value=example, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Search(bot))