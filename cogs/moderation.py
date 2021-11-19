from utils.database import attach_database_guild, database_connect
import discord
from discord.ext import commands
from discord.ext.commands.core import guild_only

class Moderation(commands.Cog, name="Moderation"):
    """
    Moderation Commands
    """
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        ids = [role.id for role in ctx.author.roles]
        return any(
            role in self.client.config["mod_roles"] #TODO: Move to check, and move roles onto guild db not config
            for role in ids
        )


    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.command(
        name="banish",
        breif="Banish member",
        description="Banishes a member to the void",
        aliases=['bonk', 'mute']
    )
    async def mute(self, ctx, *, member: discord.Member):
        """Banishes a member to the void"""
        try:
            if ctx.db_guild.mute_role is None:
                return await ctx.send("Your server doesn't have mute setup")

            mute_role = ctx.guild.get_role(ctx.db_guild.mute_role)
            await member.add_roles(mute_role)

            await ctx.send(f"You have banished {member.mention} to the void")

        except Exception as e:
            await ctx.send(e)


    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.command(
        name="unmute",
        breif="Umutes a member",
        description="unmutes a member that was sent to the void",
        aliases=['unbonk']
    )
    async def unmute(self, ctx, *, member: discord.Member):  
        """unmutes a member that was sent to the void"""
        try:
            if ctx.db_guild.mute_role is None:
                return await ctx.send("Your server doesn't have mute setup")
                
            
            mute_role = ctx.guild.get_role(ctx.db_guild.mute_role)
            await member.remove_roles(mute_role)

            await ctx.send(f"You have unmuted {member.mention}!")

        except Exception as e:
            await ctx.send(e)

    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.command(
        name="jail",
        breif="Jails a member",
        description="Send a user to jail"
    )
    async def jail(self, ctx, *, member: discord.Member):  
        """Send a user to jail"""
        try:
            if ctx.db_guild.jail_role is None:
                return await ctx.send("Your server doesn't have jail setup")

            jail_role = ctx.guild.get_role(ctx.db_guild.jail_role)
            await member.add_roles(jail_role)
            await ctx.send(f"Jailed {member.mention}!")
        except Exception as e:
            await ctx.send(e)

    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.command(
        name="setjailrole"
    )
    async def set_jail_role(self, ctx, role: discord.Role):
        """Sets the jail role"""
        ctx.db_guild.jail_role = role.id
        await ctx.send(f"Set jail role to {role.mention}")

    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.command(
        name="setmuterole"
    )
    async def set_mute_role(self, ctx, role: discord.Role):
        """Sets the mute role"""
        ctx.db_guild.mute_role = role.id
        await ctx.send(f"Set mute role to {role.mention}")
    

    @commands.command(
        name="giverole",
        breif="Give Role",
        description="Gives a user a role"
    )
    async def giverole(self, ctx, member: discord.Member, role: discord.Role):
        """Gives a user a role"""
        await member.add_roles(role)
        await ctx.send(f"Added {role} to {member}")

    
    @commands.command(
        name="removerole",
        breif="Remove Role",
        description="Removes a users role",
        aliases=['rmrole']
    )
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        """Removes a users role"""
        await member.remove_roles(role)
        await ctx.send(f"Removed {role} from {member}")

def setup(bot):
    bot.add_cog(Moderation(bot))
