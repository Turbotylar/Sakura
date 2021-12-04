import discord
from discord.ext import commands
from sakura.models.guild import Guild as DBGuild
from discord.ext.commands.core import guild_only

class Guild(commands.Cog, name="Guild"):
    """
    Guild Commands
    """
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_member_join(self, member):
        database_session = self.client.DBSession()
        
        guild = database_session.query(DBGuild).filter_by(discord_id=member.guild.id).first()
        welcome_channel = member.guild.get_channel(guild.welcome_channel)
        
        database_session.close()
        
        embed=discord.Embed(title=f"Welcome to the server {member}!", color=0xeb34cf)
        if member.avatar is not None:
            embed.set_image(url=member.avatar.url)
        await welcome_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        database_session = self.client.DBSession()

        guild = database_session.query(DBGuild).filter_by(discord_id=member.guild.id).first()
        welcome_channel = member.guild.get_channel(guild.welcome_channel)
        
        database_session.close()


        embed=discord.Embed(title=f"{member} has left the server D:", color=0xeb34cf)

        if member.avatar is not None:
            embed.set_image(url=member.avatar.url)

        await welcome_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Guild(bot))