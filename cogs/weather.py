import discord
from discord.ext import commands
from pyowm import OWM

class Weather(commands.Cog, name="Weather"):
    """Weather based commands"""
  
    def __init__(self, client):
        self.client = client
        self.owm = OWM(self.client.config["owm_api_key"])
        self.weather_manager = self.owm.weather_manager()


    @commands.command(
        name="temperature",
        )
    async def temperature(self, ctx, location=None):
        """Gets the current temperature"""
        await ctx.trigger_typing()

        location = location or self.client.config["owm_default_location"]

        observation = self.weather_manager.weather_at_place(location)
        weather = observation.weather

        temp = weather.temperature("celsius")["temp"]

        await ctx.send(f"Temperature in {location} is {temp}")

def setup(bot):
    bot.add_cog(Weather(bot))
