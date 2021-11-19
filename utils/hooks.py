from functools import partial
from discord.ext import commands

#
# Public methods
# 

async def invoke_many(functions, *args):
    """Useful in before/after hooks for running multiple"""
    for f in functions:
        await f(*args)


def multi_hook(func):
    """Invokes all previously registered hooks by other utilities
    
    Automatically applied by any other hook
    """

    if func.__before_invokes is not None:
        invokes = [y[1] for y in sorted(func.__before_invokes, key=lambda x: x[0])]
        coro = partial(invoke_many, invokes)
        if isinstance(func, commands.Command):
            func.before_invoke(coro)
        else:
            func.__before_invoke__ = coro

    if func.__after_invokes is not None:
        invokes = [y[1] for y in sorted(func.__after_invokes, key=lambda x: x[0])]
        coro = partial(invoke_many, invokes)
        if isinstance(func, commands.Command):
            func.after_invoke(coro)
        else:
            func.__after_invoke__ = coro

    return func


#
# Internal Methods
#

def before_invoke_hook(priority=0):
    """Makes this coroutine a before_invoke hook
    A higher priority will mean it will run first.
    
    NOTE: This method then can no-longer be called independently, and needs to be annotated
    """

    def decorator(coro):
        def hook(func):
            if func.__before_invokes is None:
                func.__before_invokes = []

            func.__before_invokes.append((priority, coro))
            return multi_hook(func)

        return hook
    return decorator

def after_invoke_hook(priority=0):
    """Makes this coroutine an after_invoke hook
    A higher priority will mean it will run first.
    
    NOTE: This method then can no-longer be called independently, and needs to be annotated
    """

    def decorator(coro):
        def hook(func):
            if func.__after_invokes is None:
                func.__after_invokes = []

            func.__after_invokes.append((priority, coro))
            return multi_hook(func)

        return hook
    return decorator
