import discord
from discord.ext import commands
import pylunar
import datetime

class Stats(commands.Cog, name="Stats"):
    MOON_EMOJIS = {
      "NEW_MOON": "🌑",
      "WAXING_CRESCENT": "🌒",
      "FIRST_QUARTER": "🌓",
      "WAXING_GIBBOUS": "🌔",
      "FULL_MOON": "🌕",
      "WANING_GIBBOUS": "🌖",
      "LAST_QUARTER": "🌗",
      "WANING_CRESCENT": "🌘"
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
        
        t = datetime.utcnow()
        
        mi = pylunar.MoonInfo((41, 16, 36), (174, 46, 40))
        mi.update((t.year, t.month, t.day, t.hour, t.minute, t.second))

        phase = mi.phase_name()
        emoji = Stats.MOON_EMOJIS[phase]

        day = datetime.date.today()
        await ctx.send(f"Current Moon: {emoji} {phase}")

def setup(bot):
    bot.add_cog(Misc(bot))
