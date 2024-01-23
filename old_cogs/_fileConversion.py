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


class _fileConversion(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 
    
    @commands.command()
    async def convert(self, ctx: commands.Context, source: str, link: str):
        if getenv('devMode') == "False":
            await ctx.message.delete()
            if source.lower() == "youtube":
                try:
                    video = pytube.YouTube(link)
                    video_title = video.title
                    video_stream = video.streams.get_audio_only()

                    if video_stream:
                        mp3_file_path = f"{video_title}.mp3"
                        video_stream.download(filename=mp3_file_path)

                        channel = ctx.channel
                        await channel.send(file=File(mp3_file_path))
                        remove(mp3_file_path)
                    else:
                        await ctx.send("Failed to find an audio stream for the video.")
                except Exception as e:
                    await ctx.send(f"An error occurred: {str(e)}")
            else:
                await ctx.send("Invalid source. Only 'youtube' source is supported.")

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_fileConversion(bot))