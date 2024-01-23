from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member, ui, member,  ButtonStyle, TextStyle, Color, File, channel
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


class _onJoin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 
        
        
    # @commands.Command()
    # async def test(self, ctx:commands.Context):
    #     print(ctx)
        
    @commands.Cog.listener()
    async def on_member_join(self, member:Member):
        if getenv('devMode') == "False":
            if member.guild.id == 1044055313973772379:
                # nitro ping
                nitroChannel = await member.guild.fetch_channel(1064113905883947008)
                msg = await nitroChannel.send(content=f"Hey there {member.mention}, Check out our current Nitro Giveaways")
                await sleep(10)
                await msg.delete()
    
    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_onJoin(bot))