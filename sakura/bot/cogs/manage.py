import sakura
from discord.commands.commands import SlashCommandGroup
from discord.commands.context import ApplicationContext
from sakura.bot.utils.command import sakura_command_group
import discord
from discord.ext import commands
from os.path import dirname, basename, isfile, join
import glob
from sakura.utils.database import get_user

CHECKMARK=":white_check_mark:"
CROSSMARK=":x:"

class ManageCog(commands.Cog, name="Manage"):
    """
    Bot Management commands only accessible to bot devs
    """
    def __init__(self, client):
        self.client = client

    manage = sakura_command_group("manage", "Bot management tools", dev_command=True)
    manage_cog = manage.create_group("cog", "Manage cogs")


    @manage_cog.command(
        name='reload'
    )
    async def manage_cog_reload(self, ctx, cog: str):
        """Reloads cog"""
        cog = f"sakura.bot.cogs.{cog}"
        self.client.reload_extension(cog)
        await sakura.sync_commands()
        await ctx.respond(f"Reloaded {cog}")

    @manage_cog.command(
        name='load'
    )
    async def manage_cog_load(self, ctx, cog: str):
        """Loads cog"""
        cog = f"sakura.bot.cogs.{cog}"
        self.client.load_extension(cog)
        await sakura.sync_commands()
        await ctx.respond(f"Loaded {cog}")

    @manage_cog.command(
        name='unload'
    )
    async def manage_cog_unload(self, ctx, cog: str):
        """Unloads cog"""
        cog = f"sakura.bot.cogs.{cog}"
        self.client.unload_extension(cog)
        await sakura.sync_commands()
        await ctx.respond(f"Loaded {cog}")

    @manage_cog.command(
        name='list',
        dev_command = True
    )
    async def manage_cog_list(self, ctx):
        """Lists all cogs"""
        module_files = glob.glob(join(dirname(__file__), "*.py"))
        modules = [f"sakura.bot.cogs.{basename(f)[:-3]}" for f in module_files if isfile(f) and not f.endswith('__init__.py')]
        
        module_list = []
        loaded_modules = list(self.client.extensions.keys())

        for module in modules:
            loaded = module in loaded_modules
            loaded_mark = CHECKMARK if loaded else CROSSMARK
            module_list.append(f"{loaded_mark} {module}")
        
        await ctx.respond(f"Loaded Modules:\n" + "\n".join(module_list))

    @manage.command(
        
    )
    async def sync_commands(self, ctx: ApplicationContext):
        await ctx.defer()

        await sakura.sync_commands()

        await ctx.respond("Synced")
        

    @manage.command(
        connect_database=True
    )
    async def set_bot_dev(self, ctx, member: discord.Member, new_value: bool):
        db_user = await get_user(ctx.db_session, member.id)
        db_user.is_bot_dev = new_value

        await ctx.respond(f"Updated {member.mention}'s bot_dev status to {new_value}")


def setup(bot):
    bot.add_cog(ManageCog(bot))
