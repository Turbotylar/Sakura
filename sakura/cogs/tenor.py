from sakura.utils.secrets import get_secret
import discord
from discord.ext import commands
import TenGiphPy
import json

with open("config.json") as f:
        config = json.load(f)

t = TenGiphPy.Tenor(get_secret("tenor", "api_key"))

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
        """Get a gif from tenor."""
        embed = discord.Embed(title=(str(args)), color=0xeb34cf)
                embed.set_image(url=t.random(str(args)))
                embed.add_field(name=str(title), value=imgurl, inline=False)


def setup(bot):
    bot.add_cog(Tenor(bot))
