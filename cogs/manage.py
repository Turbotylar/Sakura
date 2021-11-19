import discord
from discord.ext import commands
import subprocess
import typing
import sys
import os

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
        output = subprocess.check_output(
            ['git', 'pull']).decode()
        await ctx.send('```git\n' + output + '\n```')

    
    @commands.command(
        name='revert',
    )
    async def revert(self, ctx, number_of_commits=1):
        """Revert to n commits ago"""
        output = subprocess.check_output(
            ['git', 'checkout', 'HEAD~' + str(number_of_commits)]).decode()
        await ctx.send('```git\n' + output + '\n```')


    @commands.command(
        name='dependencies',
    )
    async def dependencies(self, ctx):
        """Pull the latest dependencies from pypi"""
        output = subprocess.check_output(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']).decode()
        await ctx.send('```pip\n' + output + '\n```')

def setup(bot):
    bot.add_cog(ManageCog(bot))
