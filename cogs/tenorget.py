import discord
from discord.ext import commands
import TenGiphPy
import json

with open("config.json") as f:
        config = json.load(f)

t = TenGiphPy.Tenor(config["tenor_api_key"])

class TenorGet(commands.Cog, name="Tenor Get"):
    def __init__(self, client):
        self.client = client


    @commands.command(
        name="get",
        breif="get a image from tenor",
        description="get a image from tenor"
    )    
    
    async def get(self, ctx, arg):
        print(t.random(arg))
        await ctx.send(t.random(str(arg)))





    

def setup(bot):
    bot.add_cog(TenorGet(bot))