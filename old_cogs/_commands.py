from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, AppCommandPermissionType, Guild, TextChannel, Member, message, errors, Color
from typing import Optional
from logging import info
from dotenv import load_dotenv
from os import getenv
from logging import info
from asyncio import sleep
import random
from ..cogs._python_commands import sendMessage
import re
import aiohttp

load_dotenv()
# MAKE SURE YOU LOAD_DOTENV() ON EVERY FILE THAT USES ENV

# CLASS NAME NEEDS TO BE UNIQUE FOR EACH COG, I LIKE TO KEEP MY COG NAME AND CLASS NAME THE SAME
class _commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.guild.id == 1104375448839925821 or message.guild.id == 1044055313973772379:
    #         msg = message.content
    #         if msg.startswith('# ') or msg.startswith('## ') or msg.startswith('### ') or msg.startswith('#### ') or msg.startswith('##### ') or msg.startswith('###### '):
    #             await message.delete()
    #         pattern = r'\[.*?\]\(https?://.*?\)'
    #         if bool(re.search(pattern, msg)) == True:
    #             await message.delete()
    #             print(f'Deleted: {msg}')
    #         if message.channel.category.id in [1105106236313190430, 1104688491297767435]:
    #             siteArray = ['.com', '.net', '.org', '.info', '.biz', '.io', '.co', "https://", "http://"]
    #             hasLink = False
    #             for item in siteArray:
    #                 if item in message.content:
    #                     hasLink = True
    #             if message.attachments:
    #                 for attachment in message.attachments:
    #                     if attachment.endswith('.exe'):
    #                         await message.delete()
    #             elif message.channel.id in [1105469733035311176, 1105121215636578325]:
    #                 return
    #             elif hasLink:
    #                 return
    #             else:
    #                 await message.delete()
    #         if int(message.flags.value) == 8192:
    #             await message.delete()

    @commands.Cog.listener() 
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')

        # # STARTS THE TESTLOOP TASK.LOOP
        # if not self.testloop.is_running():
        #     self.testloop.start()

# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_commands(bot))