import discord
from discord.ext import commands
from praw_ import praw_login

class RedditGive(commands.Cog, name="Reddit Give"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="give",
        breif="give a image from reddit",
        description="give a image from reddit"
    )    
    async def give(self, ctx, arg):
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
    bot.add_cog(RedditGive(bot))
