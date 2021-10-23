import discord
from discord.ext import commands

class ManageCog(commands.Cog, name="Manage"):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        ids = [role.id for role in ctx.author.roles]
        return any(
            role in self.client.config["mod_roles"]
            for role in ids
        )


    @commands.command()
    async def reload(self, ctx, *, cog: str):
        cog = f"cogs.{cog}"
        self.client.reload_extension(cog)
        await ctx.send(f"Reloaded {cog}")

    @commands.command()
    async def load(self, ctx, *, cog: str):
        cog = f"cogs.{cog}"
        self.client.load_extension(cog)
        await ctx.send(f"Loaded {cog}")

def setup(bot):
    bot.add_cog(ManageCog(bot))
