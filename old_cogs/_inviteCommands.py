from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member, ui, ButtonStyle, TextStyle, Color, File, file
from discord.ui import Button, View
from typing import Optional
from logging import info
from dotenv import load_dotenv
from os import getenv, remove
from logging import info
from asyncio import sleep
from random import randrange
from time import time
from math import floor
from asyncpg import create_pool
import aiohttp
import pytube


class _inviteCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 
    
    @commands.command()
    async def invite_create(self, ctx:commands.Context, user:Member):
        if getenv('devMode') == "False":
            if ctx.author.guild_permissions.manage_channels:
                channel = ctx.channel
                invite = await channel.create_invite(temporary=False, max_uses=0, max_age=0, unique=True, reason=f"PM: {user.id}")
                await ctx.reply(f"I have created the following invite on behalf of {user.mention}:\n `{invite.url}`\n I will now attempt to dm and pin the invite in my dms with them for future referencing.")
                try:
                    msg = await user.send(content=f'Your assigned invite code for {ctx.guild.name} is: `{invite.url}`')
                    try:
                        await msg.pin(reason=None)
                        await ctx.send('I have sent and pinned the data to the user.')
                    except:
                        await ctx.send('I managed to send the data to the user, however I could not pin the message.')
                except:
                    await ctx.send('It appears I have failed to update/create the data in the dm channel with this user.')
            else:
                await ctx.reply(f"This command is for those with the `manage_channels` permission.")

    @commands.command()
    async def invite_delete(self, ctx:commands.Context, code:str):
        if getenv('devMode') == "False":
            invites = await ctx.guild.invites()
            for invite in invites:
                if invite.code == code:
                    await invite.delete()
                    embed=Embed(title=f"Invite Deleted", color=int(getenv('embedColor'), 16), description=f"You have succesfully deleted invite {invite.code}")
                    await ctx.send(embed=embed)
                    return
            await ctx.send(f"{ctx.author.mention}, I'm sorry but this invite was not found. Either it does not belong to this guild, or it does not exist.")

    @commands.command()
    async def invite_check(self, ctx:commands.Context, code:str):
        if getenv('devMode') == "False":
            invites = await ctx.guild.invites()
            for invite in invites:
                if invite.code == code:
                    embed=Embed(title=f"Invite Data", color=int(getenv('embedColor'), 16)).add_field(
                        name=f"Guild",
                        value=f"{invite.guild.name}",
                        inline=False
                    ).add_field(
                        name=f"Invite Code",
                        value=f"{invite.code}",
                        inline=False
                    ).add_field(
                        name=f"Uses",
                        value=f"{invite.uses}",
                        inline=False
                    )
                    await ctx.send(embed=embed)
                    return
            
            await ctx.send(f"{ctx.author.mention}, I'm sorry but this invite was not found. Either it does not belong to this guild, or it does not exist.")

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_inviteCommands(bot))