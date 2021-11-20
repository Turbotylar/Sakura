import discord
from discord.ext import commands
import TenGiphPy
import json

with open("config.json") as f:
        config = json.load(f)

t = TenGiphPy.Tenor(config["tenor_api_key"])

class Tenor(commands.Cog, name="Tenor"):
    """
    Get gifs from tenor
    """
    def __init__(self, client):
        self.client = client


    @commands.command(
        name="tenor",
        breif="Get a gif from tenor",
        aliases=["get"]
    )    
    
    async def tenor(self, ctx, *args):
        """Get a gif from tenor"""
        await ctx.send(t.random(str(args)))





    

def setup(bot):
    bot.add_cog(Tenor(bot))