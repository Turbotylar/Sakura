import discord
from discord.ext import commands
from pyowm import OWM

class Weather(commands.Cog, name="Weather"):
    """Weather based commands"""
  
    def __init__(self, client):
        self.client = client
        self.owm = OWM(self.client.config["owm_api_key"])
        self.weather_manager = self.omw.weather_manager()


    @commands.command(
        name="temperature",
        )
    async def temperature(self, ctx, location=None):
        """Gets the current temperature"""
        await ctx.trigger_typing()

        location = location or self.client.config["owm_default_location"]

        observation = mgr.weather_at_place(location)

        temp = observation.temperature("celsius")["temp"]

        await ctx.send(f"Temperature in {location} is {temp}")

def setup(bot):
    bot.add_cog(Weather(bot))
