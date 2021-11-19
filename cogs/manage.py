import discord
from discord.ext import commands
import subprocess
import typing
import sys
import importlib


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

    @commands.group()
    async def cog(self, ctx):
        pass

    @cog.command(
        name='reload'
    )
    async def cog_reload(self, ctx, *, cog: str):
        """Reloads cog"""
        cog = f"cogs.{cog}"
        self.client.reload_extension(cog)
        await ctx.send(f"Reloaded {cog}")

    @cog.command(
        name='load'
    )
    async def cog_load(self, ctx, *, cog: str):
        """Loads cog"""
        cog = f"cogs.{cog}"
        self.client.load_extension(cog)
        await ctx.send(f"Loaded {cog}")

    @cog.command(
        name='unload'
    )
    async def cog_unload(self, ctx, *, cog: str):
        """Unloads cog"""
        cog = f"cogs.{cog}"
        self.client.unload_extension(cog)
        await ctx.send(f"Loaded {cog}")

    @commands.command()
    async def reload_config(self, ctx):
        """Reloads config"""
        with open("config.json") as f:
            self.client.config = json.load(f)
    
    @commands.command(
        name='update',
    )
    async def update(self, ctx):
        """Pull the latest changes from github and reload all modules"""
        output = subprocess.check_output(
            ['git', 'pull']).decode()
        await ctx.send('```git\n' + output + '\n```')

        reloads = []
        for key, module in sys.modules.items():
            try:
                importlib.reload(module)
                reloads.push(f"✔ {key}")
            except Exception as e:
                reloads.push(f"✘ {key}: {type(e)}")





def setup(bot):
    bot.add_cog(ManageCog(bot))
