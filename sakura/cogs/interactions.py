from sakura.utils.secrets import get_secret
import discord
from discord.ext import commands
from discord import *
import TenGiphPy


async def interact(ctx, member, action, desc, find, self):
    t = TenGiphPy.Tenor(get_secret("tenor", "api_key"))
    if str(ctx.author.display_name) != str(member.display_name):
            embedVar = discord.Embed(title=(f"{str(ctx.author.display_name)} {action} {str(member.display_name)}"), description=desc, color=0xeb34cf)
            embedVar.set_image(url=str(t.random(str(find))))
            await ctx.send(embed=embedVar)
    
    elif str(ctx.author.display_name) == str(member.display_name):
        embedVar = discord.Embed(title=(f"{str(ctx.author.display_name)} is forever alone"), description="Sorry to see you so alone", color=0xeb34cf)
        embedVar.set_image(url=str(t.random("anime alone")))
        await ctx.send(embed=embedVar)


class MemberInteractions(commands.Cog, name="Interactions"):
    """
    Interactions between server members
    """
    def __init__(self, client):
        self.client = client
        

    @commands.command() 
    async def hug(self, ctx, member: discord.Member):
        """Hugs member"""
        action = "hugged"
        desc = "Only the warmest of cuddles"
        find = "Cute anime hug"
        await interact(ctx, member, action, desc, find, self)

    
    @commands.command() 
    async def kiss(self, ctx, member: discord.Member):
        """Kisses member"""
        action = "kissed"
        desc = "Just for you <3"
        find = "Cute anime kiss"
        await interact(ctx, member, action, desc, find, self)
    
    @commands.command() 
    async def thank(self, ctx, member: discord.Member):
        """Thanks member"""
        action = "thanked"
        desc = "You are very poggers"
        find = "anime thank"
        await interact(ctx, member, action, desc, find, self)

    @commands.command() 
    async def pop(self, ctx, member: discord.Member):
        """Pops? member"""
        action = "popped?"
        desc = "why does this exist?"
        find = "anime pop" #Wtf is this???
        await interact(ctx, member, action, desc, find, self)
    
    @commands.command() 
    async def stab(self, ctx, member: discord.Member):
        """Stabs member"""
        action = "stabbed"
        desc = "Get Rekt Skrub"
        find = "anime stab"
        await interact(ctx, member, action, desc, find, self)
    
    @commands.command() 
    async def punch(self, ctx, member: discord.Member):
        """Punches member"""
        action = "punched"
        desc = "Let me introduce my fist to your face"
        find = "anime punch"
        await interact(ctx, member, action, desc, find, self)
    
    @commands.command() 
    async def pat(self, ctx, member: discord.Member):
        """Pats member"""
        action = "pet"
        desc = "God dog"
        find = "Cute anime pat"
        await interact(ctx, member, action, desc, find, self)
    
    @commands.command() 
    async def sleep(self, ctx, member: discord.Member):
        """Sleeps with member"""
        action = "slept with"
        desc = "Special"
        find = "anime sleep"
        await interact(ctx, member, action, desc, find, self)

   
def setup(bot):
    bot.add_cog(MemberInteractions(bot))
