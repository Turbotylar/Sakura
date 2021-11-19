async def invoke_many(functions, *args):
    """Useful in before/after hooks for running multiple"""
    for f in functions:
        f(*args)