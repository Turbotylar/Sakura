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
    async def manage(self, ctx):
        pass

    @manage.group(
        name='cog'
    )
    async def manage_cog(self, ctx):
        pass

    @manage_cog.command(
        name='reload'
    )
    async def manage_cog_reload(self, ctx, *, cog: str):
        """Reloads cog"""
        cog = f"cogs.{cog}"
        self.client.reload_extension(cog)
        await ctx.send(f"Reloaded {cog}")

    @manage_cog.command(
        name='load'
    )
    async def manage_cog_load(self, ctx, *, cog: str):
        """Loads cog"""
        cog = f"cogs.{cog}"
        self.client.load_extension(cog)
        await ctx.send(f"Loaded {cog}")

    @manage_cog.command(
        name='unload'
    )
    async def manage_cog_unload(self, ctx, *, cog: str):
        """Unloads cog"""
        cog = f"cogs.{cog}"
        self.client.unload_extension(cog)
        await ctx.send(f"Loaded {cog}")

    @manage.command(
        name='config'
    )
    async def manage_reload_config(self, ctx):
        """Reloads config"""
        with open("config.json") as f:
            self.client.config = json.load(f)
    
    @manage.command(
        name='update',
    )
    async def manage_update(self, ctx):
        """Pull the latest changes from github and reload all modules"""
        output = subprocess.check_output(
            ['git', 'pull']).decode()
        await ctx.send('```git\n' + output + '\n```')

        reloads = []
        for key, module in sys.modules.copy().items():
            try:
                importlib.reload(module)
                reloads.append(f"✔ {key}")
            except Exception as e:
                reloads.append(f"✘ {key}: {type(e)}")
        
        await ctx.send("\n".join(reloads)[:1500])





def setup(bot):
    bot.add_cog(ManageCog(bot))
