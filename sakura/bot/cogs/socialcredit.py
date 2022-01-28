from discord.ext import commands
import random
from nltk.sentiment.vader import SentimentIntensityAnalyzer




class SocialCredit(commands.Cog, name="Social Credit"):

    def __init__(self, bot):
        self.bot = bot
        self.sid = SentimentIntensityAnalyzer()

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return

        elif "china" in ctx.content.lower():
                #social_credit = random.randint(1,100)
                #var = ["+","-","÷","×"]
                
                #await ctx.channel.send(f"Social credit {random.choice(var)}{social_credit}")

                analysis = self.sid.polarity_scores(ctx.content)
                
                weight = analysis['compound']

                del analysis['compound']
                
                max_key = max(analysis, key=analysis.get)
                max_val = analysis[max_key]

                score_delta = int(weight * 10)
                
                if max_key is "neu":
                    score_delta = 0
                else:
                    await ctx.channel.send(f"{score_delta} social credit")

 
def setup(bot):
    bot.add_cog(SocialCredit(bot))
