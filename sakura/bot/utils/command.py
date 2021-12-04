"""Custom decorator for defining commands, with special options."""

from discord.commands.commands import ApplicationCommand, SlashCommandGroup, slash_command
from sakura.bot.utils.database import get_hooks as get_db_hooks
from sakura.bot.utils.logger import get_hooks as get_log_hooks
import logging
logger = logging.getLogger(__name__)

dev_commands = []

def sakura_command_group(
    *args,
    dev_command = False,
    **kwargs,
):
    group = SlashCommandGroup(*args, **kwargs)

    if dev_command:
        dev_commands.append(group.name)

    return group

def sakura_command(
        *args,
        connect_database=False,
        attach_user=False,
        attach_guild=False,
        attach_logger=True,

        dev_command = False, # Command should be limited to devs & dev_guilds?
        **kwargs):
    """
    Only execute these in cogs
    """
    hook_dict = {
        "attach_user": attach_user,
        "attach_guild": attach_guild,
        "attach_logger": attach_logger,
        "connect_database": connect_database
    }

    hook_sources = [
        get_db_hooks(hook_dict),
        get_log_hooks(hook_dict)
    ]

    def decorator(callback):
        
        logger.info(f"Registering command {callback=} with options {hook_dict}")

        before_hooks = []
        after_hooks = []

        for (before, after) in hook_sources:
            before_hooks.extend(before)
            after_hooks.extend(after)

        async def before_invoke(cog, ctx):
            for hook in before_hooks:
                if hook is not None:
                    await hook(cog, ctx)

        async def after_invoke(cog, ctx):
            for hook in after_hooks:
                if hook is not None:
                    await hook(cog, ctx)
        
        func = slash_command(*args, **kwargs)(callback)
        func.before_invoke(before_invoke)
        func.after_invoke(after_invoke)

        if dev_command:
            dev_commands.append(func.name)
        
        return func

    return decorator

def _update_permissions(command: ApplicationCommand, dev_permissions=None):
    if dev_permissions is not None and command.name in dev_commands:
        logger.debug(f"Setting {command} permissions to dev permissions")
        command.permissions = dev_permissions
        command.default_permission = False


    