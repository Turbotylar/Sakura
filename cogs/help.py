import discord
from discord.ext import commands

prefix = '>'

class Help(commands.Cog):
    """
    Sends help message
    """

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, *input):
        """Displays help command"""
        if not input:
            emb = discord.Embed(title='Help has arrived!', color=0xeb34cf,
                                description=f'Use `{prefix}help <category>` for more information')

            cogs_desc = ''
            for cog in self.client.cogs:
                cogs_desc += f'`{cog}` {self.client.cogs[cog].__doc__}\n'
            emb.add_field(name='Categories:', value=cogs_desc, inline=False)

            commands_desc = ''
            for command in self.client.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            if commands_desc:
                emb.add_field(name='Not belonging to a category', value=commands_desc, inline=False)

            emb.add_field(name="About", value=f"Lolibot is deveoped and maintained by Turbotylar#7714 and HexF#0015")
            emb.set_footer(text=f"Running since April 2021")

        elif len(input) == 1:

            for cog in self.client.cogs:
                if cog.lower() == input[0].lower():
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.client.cogs[cog].__doc__,
                                        color=0xeb34cf)

                    for command in self.client.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(name=f'`{prefix}{command.name}`', value=command.help, inline=False)
                    break
            else:
                emb = discord.Embed(title="You've confused me!",
                                    description=f"I've never heard from a module called `{input[0]}` before.",
                                    color=0xeb34cf)
        elif len(input) > 1:
            emb = discord.Embed(title="That's overwhelming.",
                                description="Please request only one module at once.",
                                color=0xeb34cf())

        else:
            emb = discord.Embed(title="You are build different.",
                                description="I don't know how you got here. But I didn't see this coming at all.\n"
                                            "Would you please be so kind to report that issue to me on github?\n"
                                            "https://github.com/turbotylar/lolibot/issues\n"
                                            "Thank you! ~Turbotylar#7714",
                                color=discord.Color.red())
        await ctx.send(embed = emb)


def setup(bot):
    bot.add_cog(Help(bot))