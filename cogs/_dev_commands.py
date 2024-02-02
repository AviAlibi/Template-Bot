from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member
from logging import info
from dotenv import load_dotenv
from os import getenv
from logging import info
from asyncio import sleep
import datetime


class _dev_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='ping')
    async def dev_ping(self, ctx: commands.Context):
        start_time = ctx.message.created_at
        end_time = datetime.datetime.now(datetime.timezone.utc)
        latency = (end_time - start_time).total_seconds()
        await ctx.send(content=f'Pong: `{latency}`')

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')

# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)


async def setup(bot):
    await bot.add_cog(_dev_commands(bot))
