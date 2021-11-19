import discord
from discord.ext import commands
from pyowm import OWM
import datetime
import pytz

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

        await ctx.send(f"Temperature in {location} is {temp}° celcius")

    @commands.command(
        name="weather",
        )
    async def weather(self, ctx, location=None):
        """Get's the current weather"""
        await ctx.trigger_typing()
        
        location = location or self.client.config["owm_default_location"]

        observation = self.weather_manager.weather_at_place(location)
        w = observation.weather
        temp = w.temperature("celsius")["temp"]
        high = w.temperature("celsius")["temp_max"]
        low = w.temperature("celsius")["temp_min"]


        embed=discord.Embed(title=f"Weather for today in {location.capitalize()}:", color=0xeb34cf)
        embed.set_author(name=f"{w.detailed_status.capitalize()}", icon_url=f"{w.weather_icon_url()}")
        embed.add_field(name="Clouds", value=f"There is currently a {w.clouds}% cloud coverage", inline=True)
        embed.add_field(name="Humidity", value=f"There is currently a {w.humidity}% humidity", inline=True)
        embed.add_field(name="Temperature", value=f"Today there is a high of {high}° and a low of {low}°\n\nThe current temperature is {temp}°", inline=False)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Weather(bot))
