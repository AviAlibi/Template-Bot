from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, AppCommandPermissionType, Guild, TextChannel, Member, message, errors, Color
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


class _categoryAction(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 
    
    @commands.command(name="catname", aliases=["ct"])
    async def category_name(self, ctx:commands.Context, newName:Optional[str]):
        if getenv('devMode') == "False":
            if ctx.author.guild_permissions.manage_channels:
                await ctx.channel.category.edit(name=newName)
                msg = await ctx.reply("Success")
                await ctx.message.delete()
                await sleep(5)
                await msg.delete()
    
    @commands.command()
    async def category_clone(self, ctx:commands.Context, cure:int, virus:int):
        if getenv('devMode') == "False":
            if ctx.author.guild_permissions.manage_channels:
                cureCategory = ctx.guild.get_channel(cure)
                virusCategory = ctx.guild.get_channel(virus)
                
                # Copy permission overwrites from cure to virus
                overwrites = cureCategory.overwrites
                for key, value in overwrites.items():
                    try:
                        await virusCategory.set_permissions(key, overwrite=value)
                    except errors.HTTPException as e:
                        if e.status == 429:
                            retry_after = e.headers.get('Retry-After')
                            await ctx.send(f"Rate limited. Waiting {retry_after} seconds...")
                            await sleep(int(retry_after))
                            await virusCategory.set_permissions(key, overwrite=value)
                        else:
                            raise
                await ctx.send("Permissions copied successfully!")

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_categoryAction(bot))