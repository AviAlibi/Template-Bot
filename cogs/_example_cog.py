from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member
from logging import info
from dotenv import load_dotenv
from os import getenv, remove
from logging import info
from asyncio import sleep
from ._python_commands import is_this_user_the_developer


class _example_cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='command')
    async def command_function_name(self, ctx: commands.Context):
        await ctx.channel.send(
            content=f'Hey {ctx.author.mention}, you ran !command')

    @commands.command(name='me')
    async def self_info_display(self, ctx: commands.Context):
        embed = Embed(
            title=ctx.author.name,
            description=f'Global Name: {ctx.author.global_name}\n' +
            f'Display Name: {ctx.author.display_name}\n' +
            f'Created At: {ctx.author.created_at}\n' +
            f'Joined At: {ctx.author.joined_at}\n' +
            f'Is a Bot: {ctx.author.bot}'
        ).set_image(
            url=ctx.author.display_avatar
        ).set_footer(
            text='Subtext is here in the footer'
        )
        await ctx.channel.send(embed=embed)

    @app_commands.command(
        name='oauth2',
        description='A dev only command to retrieve the Oauth link for your bot',
        nsfw=False
    )
    # this makes it so this command will not work when dm'ing the bot
    @app_commands.guild_only()
    async def oath_retrieve_command(self, interaction: Interaction):
        is_dev = await is_this_user_the_developer(
            self=self,
            user_id=interaction.user.id
        )
        if is_dev:  # basically we are checking if the user should be able to retrieve data from the .env file
            await interaction.response.send_message(  # this sends a message to the person who ran the command, note, the ephemeral means only the person who runs the command can see the response
                content=str(getenv('OAUTH')),
                ephemeral=True
            )

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')

# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)


async def setup(bot):
    await bot.add_cog(_example_cog(bot))
