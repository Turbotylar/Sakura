import discord
from discord.ext import commands

class Guild(commands.Cog, name="Guild"):
    """
    Guild Commands
    """
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(ctx, member):
        welcome_channel = ctx.guild.get_channel(ctx.db_guild.welcome_channel)
        embed=discord.Embed(title=f"Welcome to the server {member}!", color=0xeb34cf)
        embed.set_image(url=member.avatar_url)
        await welcome_channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(ctx, member):
        welcome_channel = ctx.guild.get_channel(ctx.db_guild.welcome_channel)
        embed=discord.Embed(title=f"{member} has left the server D:", color=0xeb34cf)
        embed.set_image(url=member.avatar_url)
        await welcome_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Guild(bot))