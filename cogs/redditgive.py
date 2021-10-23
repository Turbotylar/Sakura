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
    async def give(ctx, arg):
        try:
            if arg == 'loli':
                praw_login('cutelittlefangs')
                await ctx.send("Here is your loli: <:Lozic:854911358114332683>")
                await ctx.send(file=discord.File('image.png'))
            elif arg == 'cat':
                praw_login('cat')
                await ctx.send("Here is your cat:")
                await ctx.send(file=discord.File('image.png'))
            elif arg == 'kat':
                praw_login('KatarinaMains')
                await ctx.send("Here is your cat:")
            elif arg == 'yuumi':
                praw_login('YuumiMains')
                await ctx.send("Here is your cat:")
                await ctx.send(file=discord.File('image.png')) 
        except Exception as e:
            await ctx.send(e)

def setup(bot):
    bot.add_cog(RedditGive(bot))