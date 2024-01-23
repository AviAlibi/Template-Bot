from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member, ui, ButtonStyle, TextStyle, Color, File, file
from discord.ui import Button, View
from typing import Optional
from logging import info
from dotenv import load_dotenv
from os import getenv, remove
from logging import info
from asyncio import sleep
from ._python_commands import check, sendMessage
from random import randrange
from time import time
from math import floor
from asyncpg import create_pool
import aiohttp
import pytube


class _joinToCreate(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 
    
    @app_commands.command(
        name='jtc_create',
        description='An admin only command for adding more join to create VC\'s',
        nsfw=False
    )
    async def jtc_create(self, interaction:Interaction):
        if interaction.user.guild_permissions.administrator:
            name_prefix = 'new_jtc_'
            category = await interaction.guild.create_category(name_prefix + 'cat')
            channel = await category.create_voice_channel(name_prefix + 'chan')
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member:Member, before, after):
        if member.bot == False:
            # dbData = await check(self, member.id)
            if after.channel == None and before.channel != None:
                print(f"{member.display_name} left vc in {member.guild.id} | {member.guild.name}")
            elif before.channel != after.channel and before.channel != None:
                print(f"{member.display_name} switched vc in {member.guild.id} | {member.guild.name}")
                if after.channel == member.guild.afk_channel:
                    # print('is afk vc')
                    await sleep(5)
                    await member.move_to(None)
            elif after.channel != None and before.channel == None:
                print(f"{member.display_name} joined vc in {member.guild.id} | {member.guild.name}")
                if after.channel == member.guild.afk_channel:
                    # print('is afk vc')
                    await sleep(5)
                    await member.move_to(None)
        else:
            # await guildCheck(self, member.guild.id)
            if member.id == self.bot.user.id:
                if after.channel == None and before.channel != None:
                    print(f"{member.display_name} left vc in {member.guild.id} | {member.guild.name}")
                elif before.channel != after.channel and before.channel != None:
                    print(f"{member.display_name} switched vc in {member.guild.id} | {member.guild.name}")
                elif after.channel != None and before.channel == None:
                    print(f"{member.display_name} joined vc in {member.guild.id} | {member.guild.name}")


    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_joinToCreate(bot))