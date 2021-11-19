import discord
from discord.ext import commands
import subprocess
import typing


class ManageCog(commands.Cog, name="Manage"):
    """
    Bot Management commands only accessible to bot devs
    """
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        ids = [role.id for role in ctx.author.roles]
        return any(
            role in self.client.config["bot_dev"]
            for role in ids
        )


    @commands.command()
    async def reload(self, ctx, *, cog: str):
        """Reloads cog"""
        cog = f"cogs.{cog}"
        self.client.reload_extension(cog)
        await ctx.send(f"Reloaded {cog}")

    @commands.command()
    async def load(self, ctx, *, cog: str):
        """Loads cog"""
        cog = f"cogs.{cog}"
        self.client.load_extension(cog)
        await ctx.send(f"Loaded {cog}")
    
    @commands.command(
        name='pull',
    )
    async def pull(self, ctx):
        """Pull the latest changes from github"""
        try:
            output = subprocess.check_output(
                ['git', 'pull']).decode()
            await ctx.send('```git\n' + output + '\n```')
        except Exception as e:
            return await ctx.send(str(e))

    @commands.command(
        name='dependencies',
    )
    async def dependencies(self, ctx):
        """Pull the latest dependencies from pypi"""
        try:
            output = subprocess.check_output(
                ['pip', 'install', '-r', 'requirements.txt']).decode()
            await ctx.send('```pip\n' + output + '\n```')
        except Exception as e:
            return await ctx.send(str(e))

def setup(bot):
    bot.add_cog(ManageCog(bot))
