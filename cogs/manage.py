import discord
from discord.ext import commands
import subprocess
import typing


class ManageCog(commands.Cog, name="Manage"):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        ids = [role.id for role in ctx.author.roles]
        return any(
            role in self.client.config["bot_dev"]
            for role in ids
        )


    @commands.command()
    async def reload(self, ctx, *, cog: str):
        cog = f"cogs.{cog}"
        self.client.reload_extension(cog)
        await ctx.send(f"Reloaded {cog}")

    @commands.command()
    async def load(self, ctx, *, cog: str):
        cog = f"cogs.{cog}"
        self.client.load_extension(cog)
        await ctx.send(f"Loaded {cog}")
    
    @commands.command(
        name='pull',
    )
    async def pull(self, ctx, noreload: typing.Optional[str] = None):
        """Pull the latest changes from github"""
        #await ctx.trigger_typing()
        try:
            output = subprocess.check_output(
                ['git', 'pull']).decode()
            await ctx.send('```git\n' + output + '\n```')
        except Exception as e:
            return await ctx.send(str(e))

        if noreload is not None:
            return

        _cogs = [f'cogs.{i}' for i in self.cog_re.findall(output)]
        active_cogs = [i for i in _cogs if i in self.client.extensions]
        if active_cogs:
            for cog_name in active_cogs:
                await ctx.invoke(self.client.get_command('reload'), cog_name)

def setup(bot):
    bot.add_cog(ManageCog(bot))
