import discord
from discord.ext import commands
import pylunar
import datetime
import pytz

class Stats(commands.Cog, name="Stats"):
    MOON_EMOJIS = {
      "NEW_MOON": "🌑 New Moon",
      "WAXING_CRESCENT": "🌒 Waxing Crescent",
      "FIRST_QUARTER": "🌓 First Quarter",
      "WAXING_GIBBOUS": "🌔 Waxing Bingus",
      "FULL_MOON": "🌕 Full Moon",
      "WANING_GIBBOUS": "🌖 Waning gibbous",
      "LAST_QUARTER": "🌗 Last Quarter",
      "WANING_CRESCENT": "🌘 Waning Crescent"
    }
  
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="moon",
        breif="Stats",
        description="Get the current moon"
        )
    async def moon(self, ctx):
        """ Returns the current moon, as an emoji. """
        
        t = datetime.datetime.now(pytz.timezone("utc"))
        
        mi = pylunar.MoonInfo((41, 16, 36), (174, 46, 40))
        mi.update((t.year, t.month, t.day, t.hour, t.minute, t.second))

        phase = mi.phase_name()
        emoji = Stats.MOON_EMOJIS[phase]

        await ctx.send(f"Current Moon: {emoji}")
    
    @commands.command(
        name="today",
        breif="Stats",
        description="Gets current day and time"
        )
    async def today(self, ctx, arg=None):
        if arg is None:
            day = datetime.date.today() 
            await ctx.send(day.strftime("%A %B %d %Y"))
        else:
            day = datetime.datetime.now(pytz.timezone(str(arg)))
            await ctx.send(day.strftime("%A %B %d %Y \nTime: %H:%M:%S"))

def setup(bot):
    bot.add_cog(Stats(bot))
