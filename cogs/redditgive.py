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
            if arg == 'loli':
                await (praw_login('cutelittlefangs'))
                await ctx.send("Here is your loli: <:Lozic:854911358114332683>")
                await ctx.send(file=discord.File('image.png'))
            elif arg == 'cat':
                await praw_login('cat')
                await ctx.send("Here is your cat:")
                await ctx.send(file=discord.File('image.png'))
            elif arg == 'kat':
                await praw_login('KatarinaMains')
                await ctx.send("Here is your cat:")
            elif arg == 'yuumi':
                await praw_login('YuumiMains')
                await ctx.send("Here is your cat:")
                await ctx.send(file=discord.File('image.png')) 
            elif arg == 'astolfo':
                await praw_login('astolfo')
                await ctx.send("One trap coming right up!:")
                await ctx.send(file=discord.File('image.png')) 
            elif arg == 'eyebleach':
                await praw_login('eyebleach')
                await ctx.send("Something to fix your vision cumming up!:")
                await ctx.send(file=discord.File('image.png')) 
           
            else:
                await ctx.send("That isn't an option, if you think this is a mistake contact Turbotylar#7714")
        except Exception as e:
            await ctx.send(e)

def setup(bot):
    bot.add_cog(RedditGive(bot))
