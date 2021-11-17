import discord
from discord.ext import commands
from praw_ import praw_login

class Reddit(commands.Cog, name="Reddit"):
    """
    Get images from reddit
    """
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="reddit",
        breif="Retrieve an image from reddit"
    )    
    async def reddit(self, ctx, arg):
        """Retrieve an image from reddit"""
        try:
            async with ctx.typing():
                imgurl, title = await (praw_login(str(arg)))
                embed = discord.Embed(title=("Here you go:"), color=0xeb34cf)
                embed.set_image(url=imgurl)
                embed.add_field(name=str(title), value=imgurl, inline=False)
                await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("That isn't an option, if you think this is a mistake contact Turbotylar#7714")
            await ctx.send(e)

def setup(bot):
    bot.add_cog(Reddit(bot))
