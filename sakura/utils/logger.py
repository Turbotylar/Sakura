from sakura.utils.hooks import before_invoke_hook

import logging
logger = logging.getLogger(__name__)

#
#   Custom Hooks
#

@before_invoke_hook(priority=1000000)
async def attach_logger(cog, ctx):
    ctx.logger = 