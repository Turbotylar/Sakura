"""Custom decorator for defining commands, with special options."""

import discord
from discord.commands.commands import SlashCommand, SlashCommandGroup, slash_command
from sakura.utils.database import get_hooks as get_db_hooks
from sakura.utils.logger import get_hooks as get_log_hooks
import logging
logger = logging.getLogger(__name__)

def sakura_command_group(
    *args,
    **kwargs,
):
    group = SlashCommandGroup(*args, **kwargs)
    # hacky af patching to make SlashCommandGroup work with Cogs
    def wrap_command(*wargs, **wkwargs):
        def decorator(callback)  -> SlashCommand:
            command = sakura_command(*wargs, **wkwargs, parent=group)(callback)
            def stub_copy():
                return command
            command.copy = stub_copy
            group.subcommands.append(command)
            logger.debug(f"Registered Subcommand: {group.subcommands}")
            return command
        return decorator

    def wrap_command_group(*wargs, **wkwargs):
        cmd_group = sakura_command_group(*wargs, **wkwargs, parent=group)
        group.subcommands.append(cmd_group)
        return cmd_group

    def _update_copy(kwargs):
        return group
        if kwargs:
            kw = kwargs.copy()
            kw.update(group.__original_kwargs__)
            copy = group.__class__(group.callback, **kw)
            return copy
        else:
            return group.copy()

    def _copy():
        return group
        ret = group.__class__(group.name, group.description, **group.__original_kwargs__)
        ret.subcommands.extend(group.subcommands)
        ret.cog = group.cog
        return ret


    group.command = wrap_command

    group.command_group = wrap_command_group

    group._update_copy = _update_copy
    group.copy = _copy
    

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
            logger.debug(f"{args}")
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
        func.default_permission = not dev_command

        callback.dev_command = dev_command
        
        return func

    return decorator