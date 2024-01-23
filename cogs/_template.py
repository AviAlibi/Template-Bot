from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member
from logging import info
from dotenv import load_dotenv
from os import getenv
from logging import info
from asyncio import sleep


class _template(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')

# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)


async def setup(bot):
    await bot.add_cog(_template(bot))
