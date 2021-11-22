from sakura.utils.secrets import get_secret
from sakura.utils.command import sakura_command
import discord
from discord.ext import commands
from pyowm import OWM
import datetime
import pytz
import pylunar

from sakura.utils.database import attach_database_user, database_connect

class Glance(commands.Cog, name="Glance"):
    """Information at a glance"""

    MOON_EMOJIS = {
      "NEW_MOON": "🌑 New Moon",
      "WAXING_CRESCENT": "🌒 Waxing Crescent",
      "FIRST_QUARTER": "🌓 First Quarter",
      "WAXING_GIBBOUS": "🌔 Waxing Bingus",
      "FULL_MOON": "🌕 Full Moon",
      "WANING_GIBBOUS": "🌖 Waning Bingus",
      "LAST_QUARTER": "🌗 Last Quarter",
      "WANING_CRESCENT": "🌘 Waning Crescent"
    }


    def __init__(self, client):
        self.client = client
        self.owm = OWM(get_secret("openweathermap", "api_key"))
        self.weather_manager = self.owm.weather_manager()
        self.default_location = get_secret("openweathermap", "default_location")

    @sakura_command(
        name="temperature",
        attach_user=True
    )
    async def temperature(self, ctx, location=None):
        """Gets the current temperature"""
        await ctx.trigger_typing()

        location = location or ctx.db_user.location or self.default_location

        observation = self.weather_manager.weather_at_place(location)
        weather = observation.weather

        temp = weather.temperature("celsius")["temp"]
        high = weather.temperature("celsius")["temp_max"]
        low = weather.temperature("celsius")["temp_min"]

        await ctx.send(f"Temperature in {location} is {temp}° Celsius, today there is a high of {high}° Celsius and a low of {low}° Celsius")

    @sakura_command(
        name="weather",
        attach_user=True
    )
    async def weather(self, ctx, location=None):
        """Get's the current weather"""
        await ctx.trigger_typing()
        
        location = location or ctx.db_user.location or self.default_location

        observation = self.weather_manager.weather_at_place(location)
        w = observation.weather
        temp = w.temperature("celsius")["temp"]
        high = w.temperature("celsius")["temp_max"]
        low = w.temperature("celsius")["temp_min"]
        rain = w.rain


        embed=discord.Embed(title=f"Weather for today in {location.capitalize()}:", color=0xeb34cf)
        embed.set_author(name=f"{w.detailed_status.capitalize()}", icon_url=f"{w.weather_icon_url()}")
        embed.add_field(name="Clouds", value=f"There is currently a {w.clouds}% cloud coverage", inline=True)
        embed.add_field(name="Humidity", value=f"There is currently a {w.humidity}% humidity", inline=True)
        embed.add_field(name="Temperature", value=f"Today there is a high of {high}° and a low of {low}°\n\nThe current temperature is {temp}°", inline=True)
        if(rain):
            embed.add_field(name="Rain", value=f"Preticipation volume in the last hour: {rain['1h']}", inline=True)
        await ctx.send(embed=embed)

    @commands.command(
        name="moon",
        breif="Stats",
        description="Get the current moon"
        )
    async def moon(self, ctx):
        """ Returns the current moon, as an emoji. """
        
        t = datetime.datetime.utcnow()
        
        mi = pylunar.MoonInfo((41, 16, 36), (174, 46, 40))
        mi.update((t.year, t.month, t.day, t.hour, t.minute, t.second))

        phase = mi.phase_name()
        emoji = Glance.MOON_EMOJIS[phase]

        await ctx.send(f"Current Moon: {emoji}")
    
    @commands.command(
        name="today",
        breif="Stats",
        description="Gets current day and time"
        )
    async def today(self, ctx, arg=None):
        """Gets current day and time"""
        if arg is None:
            day = datetime.date.today()
        else:
            day = datetime.datetime.now(pytz.timezone(str(arg)))
            
        await ctx.send(day.strftime("%A %B %d %Y \nTime: %H:%M:%S"))
    
    @database_connect
    @attach_database_user
    @commands.command(
        name="setlocation"
    )
    async def set_location(self, ctx, location: str):
        """Set your default location"""
        ctx.db_user.location = location
        await ctx.send(f"{ctx.author.mention}, set your location to '{location}'")


def setup(bot):
    bot.add_cog(Glance(bot))
