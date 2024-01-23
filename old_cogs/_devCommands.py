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


class _devCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 

    @app_commands.command(description="A command to list all guilds the bot is in")
    async def user_dm(self, interaction:Interaction, target:Member, message:str):
        if interaction.user.id == int(getenv('devId')):
            print(target)
            print(message)
            embed=Embed(title='BZZZZZ BZZZ BZZZZ (You\'ve got mail)', description=f'{message}\nSent by: {interaction.user.name}', color=int(getenv('embedColor'), 16))
            await target.send(embed=embed)
            await interaction.response.send_message(content=f'Message sent to {target.name}', ephemeral=True)
            
    @app_commands.command(description="A command for pushing announcements to all active guilds the bot is in")
    async def guild_notify(self, interaction:Interaction, message:str):
        if interaction.user.id == int(getenv('devId')):
            fails = 0
            for guild in self.bot.guilds:
                try:
                    await guild.system_channel.send(f"{message}")
                except:
                    try:
                        await guild.owner.send(f"You have received this message in dms due to no system channel being found within {guild.name}\n*{message}*")
                    except:
                        print(guild.id, guild.name, "failed to be notified")
                        fails += 1
            print(f'You have notified `{len(self.bot.guilds) - fails}` guilds out of `{len(self.bot.guilds)}` guilds')
        else:
            await interaction.response.send_message("This command is not for you.")
    
    @commands.command()
    async def guild_leave(self, ctx:commands.Context, guild:int):
        if ctx.author.id == int(getenv('devId')):
            guild = self.bot.get_guild(guild)
            await guild.leave()
            await ctx.reply(f"I have left `{guild.name}`")
        else:
            await ctx.reply(f"Thats not for you.")
            
    # @app_commands.command(description="A command to list all guilds the bot is in")
    # async def guilds(self, interaction:Interaction):
    #     description = "Guild ID | Guild Name"
    #     i = 0
    #     for guild in self.bot.guilds:
    #         i += 1
    #         description = description + f"\n{i}: {guild.id} - {guild.name}"
    #     embed = Embed(description=description, color=int(getenv('embedColor'), 16))
    #     await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # @commands.command()
    # async def emoji_name_fix(self, ctx:commands.Context, virus:str, cure:str):
    #     if ctx.author.id == int(getenv('devId')):
    #         for emoji in ctx.guild.emojis:
    #             if virus in emoji.name:
    #                 print(emoji.name)
    #                 await emoji.edit(name=emoji.name.replace(virus, cure))
    #         await ctx.reply('Emoji names have been')

    # @commands.command()
    # async def test_pin(self, ctx:commands.Context):
    #     await ctx.message.pin(reason=None)

    @commands.command()
    async def guild_list(self, ctx:commands.Context):
        if getenv('devMode') == "False":
            description = ''
            for guild in self.bot.guilds:
                description += f'\n{guild.name} | {guild.id}'
            embed = Embed(description=description)
            await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_devCommands(bot))