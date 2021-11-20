import sakura
import discord
from discord.ext import commands
import asyncpraw

class Reddit(commands.Cog, name="Reddit"):
    """
    Get images from reddit
    """
    def __init__(self, client):
        self.client = client

        self.previously_sent = []

        praw_conf = self.client.config["praw"]

        self.praw = asyncpraw.Reddit(
            client_id = praw_conf["client_id"],
            client_secret = praw_conf["client_secret"],

            username = praw_conf["username"],
            password = praw_conf["password"],

            user_agent = sakura.USER_AGENT
        )

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

def setup(bot):
    bot.add_cog(Reddit(bot))
