from sakura.bot.utils.checks import is_guild_moderator
from sakura.utils.database import attach_database_guild, database_connect
import discord
from discord.ext import commands
from discord.ext.commands.core import guild_only

class Moderation(commands.Cog, name="Moderation"):
    """
    Moderation Commands
    """
    def __init__(self, client):
        self.client = client


    @guild_only()
    @database_connect
    @attach_database_guild
    @is_guild_moderator()
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
    @is_guild_moderator()
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
    @is_guild_moderator()
    @commands.command(
        name="jail",
        breif="Jails a member",
        description="Send a user to jail"
    )
    async def jail(self, ctx, *, member: discord.Member):  
        """Send a user to jail"""
        try:
            if ctx.db_guild.jail_role is None or ctx.db_guild.verified_role is None:
                return await ctx.send("Your server doesn't have jail setup")

            jail_role = ctx.guild.get_role(ctx.db_guild.jail_role)
            verified_role = ctx.guild.get_role(ctx.db_guild.verified_role)
            await member.add_roles(jail_role)
            await member.remove_roles(verified_role)
            await ctx.send(f"Jailed {member.mention}!")
        except Exception as e:
            await ctx.send(e)

    @guild_only()
    @database_connect
    @attach_database_guild
    @is_guild_moderator()
    @commands.command(
        name="unjail",
        breif="UnJails a member",
        description="Retrieves a user from jail"
    )
    async def unjail(self, ctx, *, member: discord.Member):  
        """Brings back a user from jail"""
        try:
            if ctx.db_guild.jail_role is None or ctx.db_guild.verified_role is None:
                return await ctx.send("Your server doesn't have jail setup")

            jail_role = ctx.guild.get_role(ctx.db_guild.jail_role)
            verified_role = ctx.guild.get_role(ctx.db_guild.verified_role)
            await member.remove_roles(jail_role)
            await member.add_roles(verified_role)
            await ctx.send(f"UnJailed {member.mention}!")
        except Exception as e:
            await ctx.send(e)

    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.has_permissions(administrator=True)
    #@is_guild_moderator()
    @commands.command(
        name="purge",
        breif="purges a channel",
        description="Purges messages from a channel"
    )
    async def purge(self, ctx, limit: int):  
        """Purges messages from a channel"""
        try:
            deleted = await ctx.channel.purge(limit=limit)
            await ctx.send(f'Deleted {len(deleted)} message(s)')
        except Exception as e:
            await ctx.send(e)


    @guild_only()
    @database_connect
    @attach_database_guild
    @is_guild_moderator()
    @commands.command(
        name="slowmode",
        breif="enables/disables slowmode in a channel",
        description="enables/disables slowmode in a channel"
    )
    async def slowmode(self, ctx, secs: int):  
        """Purges messages from a channel"""
        try:
            slowmode = await ctx.channel.slowmode_delay(secs)
            await ctx.send(f'Enabled slowmode of {len(slowmode)} second(s)')
        except Exception as e:
            await ctx.send(e)



    @guild_only()
    @database_connect
    @attach_database_guild
    @is_guild_moderator()
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
    @is_guild_moderator()
    @commands.command(
        name="setmuterole"
    )
    async def set_mute_role(self, ctx, role: discord.Role):
        """Sets the mute role"""
        ctx.db_guild.mute_role = role.id
        await ctx.send(f"Set mute role to {role.mention}")


    @guild_only()
    @database_connect
    @attach_database_guild
    @is_guild_moderator()
    @commands.command(
        name="setwelcomechannel"
    )
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        """Sets the welcome channel"""
        ctx.db_guild.welcome_channel = channel.id
        await ctx.send(f"Set welcome channel to {channel.mention}")


    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.has_guild_permissions(manage_roles=True)
    @commands.command(
        name="setmodrole"
    )
    async def set_mod_role(self, ctx, role: discord.Role):
        """Sets the mod role"""
        ctx.db_guild.mod_role = role.id
        await ctx.send(f"Set mod role to {role.mention}")
    

    @guild_only()
    @database_connect
    @attach_database_guild
    @commands.has_guild_permissions(manage_roles=True)
    @commands.command(
        name="setverifiedrole"
    )
    async def set_verified_role(self, ctx, role: discord.Role):
        """Sets the verified role"""
        ctx.db_guild.verified_role = role.id
        await ctx.send(f"Set verified role to {role.mention}")
    


    @commands.command(
        name="giverole",
        breif="Give Role",
        description="Gives a user a role"
    )
    @is_guild_moderator()
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
    @is_guild_moderator()
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        """Removes a users role"""
        await member.remove_roles(role)
        await ctx.send(f"Removed {role} from {member}")


def setup(bot):
    bot.add_cog(Moderation(bot))
