import discord
from discord.ext import commands
import subprocess
import typing
import sys
import importlib
from os.path import dirname, basename, isfile, join
import glob

from utils.database import database_connect, get_user

CHECKMARK=":white_check_mark:"
CROSSMARK=":x:"

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

    @manage_cog.command(
        name='list'
    )
    async def manage_cog_list(self, ctx):
        """Lists all cogs"""
        module_files = glob.glob(join(dirname(__file__), "*.py"))
        modules = [f"cogs.{basename(f)[:-3]}" for f in module_files if isfile(f) and not f.endswith('__init__.py')]
        
        module_list = []
        loaded_modules = list(self.client.extensions.keys())

        for module in modules:
            loaded = module in loaded_modules
            loaded_mark = CHECKMARK if loaded else CROSSMARK
            module_list.append(f"{loaded_mark} {module}")
        
        await ctx.send(f"Loaded Modules:\n" + "\n".join(module_list))

    @manage.command(
        name='config'
    )
    async def manage_reload_config(self, ctx):
        """Reloads config"""
        with open("config.json") as f:
            self.client.config = json.load(f)

    @database_connect
    @manage.command()
    async def set_bot_dev(self, ctx, member: discord.Member, new_value: bool):
        db_user = await get_user(ctx.db_session, member.id)
        db_user.is_bot_dev = new_value

        await ctx.send(f"Updated {member.mention}'s bot_dev status to {new_value}")
    
    @manage.command(
        name='update',
    )
    async def manage_update(self, ctx):
        """Pull the latest changes from github and reload all modules"""
        output = subprocess.check_output(
            ['git', 'pull']).decode()
        await ctx.send('Git Log:\n```git\n' + output + '\n```')

        cogs = []

        reloads = []
        for key, module in sys.modules.copy().items():
            if key.startswith("cogs."):
                cogs.append(key)
                continue

            if key.split(".")[0] not in ["models", "utils"]:
                # Skip non-lolibot modules
                continue

            try:
                importlib.reload(module)
                reloads.append(f"{CHECKMARK} {key}")
            except Exception as e:
                reloads.append(f"{CROSSMARK} {key}: {type(e)}")
        
        await ctx.send("Reloading Lolibot modules: \n" + "\n".join(reloads))

        cog_reloads = []
        for cog in cogs:
            
            try:
                self.client.reload_extension(cog)
                cog_reloads.append(f"{CHECKMARK} {cog}")
            except Exception as e:
                cog_reloads.append(f"{CROSSMARK} {cog}: {type(e)}")
            
        await ctx.send("Reloading cogs: \n" + "\n".join(cog_reloads) + "\n Done")







def setup(bot):
    bot.add_cog(ManageCog(bot))
