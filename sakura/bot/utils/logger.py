import logging

from discord.commands.context import ApplicationContext
logger = logging.getLogger(__name__)

#
#   Custom Hooks
#

def get_hooks(hook_dict):
    async def logger_before(cog, ctx: ApplicationContext):
        klass = ctx.command.cog.__class__

        scope = ".".join([
            klass.__module__,
            klass.__qualname__,
            str(ctx.command.name)
        ])

        ctx.logger = logging.getLogger(scope)

    
    if hook_dict["attach_logger"]:
        return ([logger_before], [])
    return ([],[])