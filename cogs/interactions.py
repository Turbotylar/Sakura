import discord
from discord.ext import commands
from discord import *
from __main__ import bot
from discord_components import *
import TenGiphPy
import json

with open("config.json") as f:
        config = json.load(f)

t = TenGiphPy.Tenor(config["tenor_api_key"])

async def interact(ctx, member, action, desc, find):
    if str(ctx.author.display_name) != str(member.display_name):
            embedVar = discord.Embed(title=(f"{str(ctx.author.display_name)} {action} {str(member.display_name)}"), description=desc, color=0xeb34cf)
            embedVar.set_image(url=str(t.random(str(find))))
            await ctx.send(embed=embedVar)
    elif str(ctx.author.display_name) == str(member.display_name):
        embedVar = discord.Embed(title=(f"{str(ctx.author.display_name)} is forever alone"), description="Sorry to see you so alone", color=0xeb34cf)
        embedVar.set_image(url=str(t.random(str("anime alone"))))
        await ctx.send(embed=embedVar)

class MemberInteractions(commands.Cog, name="Member Interactions"):
    def __init__(self, client):
        self.client = client

    @commands.command() 
    async def hug(self, ctx, member: discord.Member):
        action = "hugged"
        desc = "Only the warmest of cuddles"
        find = "Cute anime hug"
        await interact(ctx, member, action, desc, find)

    
    @commands.command() 
    async def kiss(self, ctx, member: discord.Member):
        action = "kissed"
        desc = "Just for you <3"
        find = "Cute anime kiss"
        await interact(ctx, member, action, desc, find)

    @commands.command() 
    async def pop(self, ctx, member: discord.Member):
        action = "popped?"
        desc = "why does this exist?"
        find = "anime pop" #Wtf is this???
        await interact(ctx, member, action, desc, find)
    
    @commands.command() 
    async def stab(self, ctx, member: discord.Member):
        action = "stabbed"
        desc = "Get Rekt Skrub"
        find = "anime stab"
        await interact(ctx, member, action, desc, find)
    
    @commands.command() 
    async def punch(self, ctx, member: discord.Member):
        action = "punched"
        desc = "Let me introduce my fist to your face"
        find = "anime punch"
        await interact(ctx, member, action, desc, find)
    
    @commands.command() 
    async def pat(self, ctx, member: discord.Member):
        action = "pet"
        desc = "God dog"
        find = "Cute anime pat"
        await interact(ctx, member, action, desc, find)
    
    @commands.command() 
    async def sleep(self, ctx, member: discord.Member):
        action = "slept with"
        desc = "Special"
        find = "anime sleep"
        await interact(ctx, member, action, desc, find)
    
def setup(bot):
    bot.add_cog(MemberInteractions(bot))