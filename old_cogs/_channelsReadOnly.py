from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member, ui, ButtonStyle, TextStyle, Color, File, file
from discord.ui import Button, View
from typing import Optional
from logging import info
from dotenv import load_dotenv
from os import getenv, remove
from logging import info
from asyncio import sleep
from ..cogs._python_commands import check, sendMessage
from random import randrange
from time import time
from math import floor
from asyncpg import create_pool
import aiohttp
import pytube


class _channelsReadOnly(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 
    
    @commands.command()
    async def channel_info(self, ctx: commands.Context):
        if getenv('devMode') == "False":
            channel = ctx.message.channel
            title = f"Info for {channel.name}"
            description = (
                f"ID: `{channel.id}`\n"
                f"Type: `{channel.type}`\n"
                f"Cat ID: `{channel.category.id}`\n"
                f"NSFW: `{str(channel.nsfw)}`\n"
                f"Slow: `{channel.slowmode_delay}`\n"
                f"Topic: `{channel.topic}`"
            )
            embed = Embed(title=title, description=description, color=int(getenv('embedColor'), 16))
            await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_channelsReadOnly(bot))