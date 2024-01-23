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


class _channelsAction(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
    
    @commands.command()
    async def channel_nsfw(self, ctx:commands.Context, state:bool):
        if getenv('devMode') == "False":
            if ctx.author.guild_permissions.manage_channels:
                if bool:
                    await ctx.message.channel.edit(nsfw=True)
                    await ctx.send(f"{ctx.channel.mention} is now a NSFW channel")
                else:
                    await ctx.message.channel.edit(nsfw=False)
                    await ctx.send(f"{ctx.channel.mention} is no longer a NSFW channel")
    
    @commands.command(aliases=["cn"])
    async def channel_name(self, ctx:commands.Context, newName:Optional[str]):
        if getenv('devMode') == "False":
            if ctx.author.guild_permissions.manage_channels:
                await ctx.channel.edit(name=newName)
                msg = await ctx.reply("Success")
                await ctx.message.delete()
                await sleep(5)
                await msg.delete()
            else:
                await ctx.reply("You need the `manage_channels` permission to use this command")


    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_channelsAction(bot))