import discord
from discord.ext import commands

class Moderation(commands.Cog, name="Moderation"):
    """
    Moderation Commands
    """
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        ids = [role.id for role in ctx.author.roles]
        return any(
            role in self.client.config["mod_roles"]
            for role in ids
        )


    @commands.command(
        name="banish",
        breif="Banish member",
        description="Banishes a member to the void",
        aliases=['bonk', 'mute']
    )
    async def banish(self, ctx, *, member: discord.Member):
        """Banishes a member to the void"""
        try:
            await ctx.send(f"You have banished {member.mention} to the void")
            await self.banish_member(member)
        except Exception as e:
            await ctx.send(e)

    @commands.command(
        name="jail",
        breif="Jails a member",
        description="Send a user to jail"
    )
    async def jail(self, ctx, *, member: discord.Member):  
        """Send a user to jail"""
        await ctx.send(f"Attempting to jail {member.mention}!")
        try:
            await ctx.send(f"Jailed {member.mention}!")
            await self.jail_member(member)
        except Exception as e:
            await ctx.send(e)

    @commands.command(
        name="unmute",
        breif="Umutes a member",
        description="unmutes a member that was sent to the void",
        aliases=['unbonk']
    )
    async def unmute(self, ctx, *, member: discord.Member):  
        """unmutes a member that was sent to the void"""
        try:
            await ctx.send(f"You have unmuted {member.mention}!")
            await self.unmute_member(member)
        except Exception as e:
            await ctx.send(e)

    async def jail_member(self, member):
        jail_role = member.guild.get_role(self.client.config["jail_role"])
        verified_role = member.guild.get_role(self.client.config["verified_role"])
        await member.add_roles(jail_role)
        await member.remove_roles(verified_role)
    
    async def banish_member(self, member):
        mute_role = member.guild.get_role(self.client.config["mute_role"])
        await member.add_roles(mute_role)

    async def unmute_member(self, member):
        mute_role = member.guild.get_role(self.client.config["mute_role"])
        await member.remove_roles(mute_role)
    
    
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
