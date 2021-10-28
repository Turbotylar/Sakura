import discord
from discord.ext import commands

class Moderation(commands.Cog, name="Moderation"):
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
        description="Banishes a member to the void"
    )
    async def banish(self, ctx, *, member: discord.Member):
        try:
            await ctx.send(f"You have banished {member.mention} to the void")
            await self.banish_member(member)
        except Exception as e:
            await ctx.send(e)


    @commands.command(
        name="unmute",
        breif="Umutes a member",
        description="unmutes a member that was sent to the void"
    )
    async def unmute(self, ctx, *, member: discord.Member):  
        try:
            await ctx.send(f"You have unmuted {member.mention}!")
            await self.unmute_member(member)
        except Exception as e:
            await ctx.send(e)

    async def banish_member(self, member):
        jail_role = member.guild.get_role(self.client.config["mute_role"])
        await member.add_roles(jail_role)

    async def unmute_member(self, member):
        jail_role = member.guild.get_role(self.client.config["mute_role"])
        await member.remove_roles(jail_role)

def setup(bot):
    bot.add_cog(Moderation(bot))
