from sakura.utils.hooks import before_invoke_hook

import logging
logger = logging.getLogger(__name__)

#
#   Custom Hooks
#

@before_invoke_hook(priority=1000000)
async def attach_logger(cog, ctx):
    klass = ctx.command.cog.__class__

    scope = ".".join([
        klass.__module__,
        klass.__qualname__,
        str(ctx.command.name)
    ])

    ctx.logger = logging.getLogger(scope)