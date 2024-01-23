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


class _rolesReadOnly(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 
    
    @commands.command()
    async def inrole(self, ctx:commands.Context, roleid:int):
        if getenv('devMode') == "False":
            guild = ctx.guild
            if ctx.author.guild_permissions.manage_roles is True:
                await ctx.message.delete()
                role = guild.get_role(roleid)
                counter = 0
                for member in guild.members:
                    if role in member.roles:
                        counter += 1
                await ctx.send(f'{ctx.author.mention} There are `{counter} users` out of `{guild.member_count}` with the role `{role.name}`')
            else:
                try:
                    await ctx.author.send(content=f'You do not have the required permission to use `bzz inrole` in {guild.name}, must have `MANAGE_ROLES` permission')
                except:
                    await ctx.channel.send(content=f'{ctx.author.mention} You do not have the required permission to use `bzz inrole` in {guild.name}, must have `MANAGE_ROLES` permission')

    @commands.command()
    async def listuserswithrole(self, ctx:commands.Context, roleid:int):
        if getenv('devMode') == "False":
            guild = ctx.guild
            if ctx.author.guild_permissions.manage_roles is True:
                await ctx.message.delete()
                role = guild.get_role(roleid)
                counter = 0
                users = ' Users:'
                for member in guild.members:
                    if role in member.roles:
                        if counter == 0:
                            users += f'`{member.name}`'
                        else:
                            users += f', `{member.name}`'
                        counter += 1
                if counter <= 10:
                    outputText = str(counter) + users
                    await ctx.channel.send(outputText)
                else:
                    outputText = str(counter) + ' Users total, cannot print more then 10.'
                    await ctx.channel.send(outputText)   

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_rolesReadOnly(bot))