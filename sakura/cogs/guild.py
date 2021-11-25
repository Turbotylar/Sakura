import discord
from discord.ext import commands
from sakura.utils.checks import is_guild_moderator
from sakura.utils.database import attach_database_guild, database_connect
from discord.ext.commands.core import guild_only


class Guild(commands.Cog, name="Guild"):
    """
    Guild Commands
    """
    def __init__(self, client):
        self.client = client

        
    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.Cog.listener()
    async def on_member_join(self, member):
        database_session = member.bot.DBSession()
        guild = database_session.query(Guild).filter_by(discord_id=member.guild.id).first()
        welcome_channel = self.guild.get_channel(guild.welcome_channel)
        database_session.close()
        embed=discord.Embed(title=f"Welcome to the server {member}!", color=0xeb34cf)
        embed.set_image(url=member.avatar_url)
        await welcome_channel.send(embed=embed)
    

    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        database_session = member.bot.DBSession()
        guild = database_session.query(Guild).filter_by(discord_id=member.guild.id).first()
        welcome_channel = self.guild.get_channel(guild.welcome_channel)
        database_session.close()
        embed=discord.Embed(title=f"{member} has left the server D:", color=0xeb34cf)
        embed.set_image(url=member.avatar_url)
        await welcome_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Guild(bot))