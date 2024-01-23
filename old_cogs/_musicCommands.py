from discord.ext import commands, tasks
import discord
from discord.ui import Button, View
from typing import Optional
from logging import info
from dotenv import load_dotenv
from os import getenv
from logging import info
from asyncio import sleep
from random import randrange
from time import time
from math import floor
# from asyncpg import create_pool
from ..cogs._python_commands import clear_csv, add_to_queue, clear_guild_queue

devMode = False

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

load_dotenv()

class _musicCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member:discord.Member, before, after):
    #     if member.bot == False:
    #         # dbData = await check(self, member.id)
    #         if after.channel == None and before.channel != None:
    #             print(f"{member.display_name} left vc in {member.guild.id} | {member.guild.name}")
    #         elif before.channel != after.channel and before.channel != None:
    #             print(f"{member.display_name} switched vc in {member.guild.id} | {member.guild.name}")
    #             if after.channel == member.guild.afk_channel:
    #                 # print('is afk vc')
    #                 await sleep(5)
    #                 await member.move_to(None)
    #         elif after.channel != None and before.channel == None:
    #             print(f"{member.display_name} joined vc in {member.guild.id} | {member.guild.name}")
    #             if after.channel == member.guild.afk_channel:
    #                 # print('is afk vc')
    #                 await sleep(5)
    #                 await member.move_to(None)
    #     else:
    #         # await guildCheck(self, member.guild.id)
    #         if member.id == self.bot.user.id:
    #             if after.channel == None and before.channel != None:
    #                 print(f"{member.display_name} left vc in {member.guild.id} | {member.guild.name}")
    #                 await clear_guild_queue(guildId=member.guild.id)
    #             elif before.channel != after.channel and before.channel != None:
    #                 print(f"{member.display_name} switched vc in {member.guild.id} | {member.guild.name}")
    #             elif after.channel != None and before.channel == None:
    #                 print(f"{member.display_name} joined vc in {member.guild.id} | {member.guild.name}")

    # @discord.app_commands.command(name='join', description='Have the bot join your vc')
    # async def join(self, interaction:discord.Interaction):
    #     print(interaction)
    #     print(self.bot.voice_clients)
    #     if interaction.user.voice.channel in self.bot.voice_clients:
    #         print('already in your vc')
    #     if not False:
    #         await interaction.user.voice.channel.connect(self_deaf=True)

    # @discord.app_commands.command(name='leave', description='Have the bot leave your vc')
    # async def leave(self, interaction:discord.Interaction):
    #     print(interaction)
    #     print(self.bot.voice_clients[0].channel)

    # @discord.app_commands.command(description="join vc/play a song")
    # async def play(self, interaction:discord.Interaction, song:Optional[str]):
    #     if devMode:
    #         await interaction.response.send_message("🍯Music features are in development at this time🍯", ephemeral=True)
    #     else:
    #         dbData = await check(self, interaction.user.id)
    #         guildData = await guildCheck(self, interaction.guild.id)
    #         if dbData[0]['in_voice'] == False:
    #             await interaction.response.send_message(content="please join a voice channel first", ephemeral=True)
    #         else:
    #             if guildData[0]['in_voice'] == False:
    #                 # join the voice channel
    #                 await interaction.user.voice.channel.connect()
    #                 await interaction.response.send_message(content="Joined your vc", ephemeral=True)
    #             elif guildData[0]['in_voice'] == True and guildData[0]['bot_vc'] != dbData[0]['voice_channel_id']:
    #                 await interaction.response.send_message(content="I am already in a voice channel", ephemeral=True)
    #             elif guildData[0]['bot_vc'] == dbData[0]['voice_channel_id'] and song != None:
    #                 if guildData[0]['queue'] == None:
    #                     search = f"ytsearch:{song}"
    #                     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #                         result = ydl.extract_info(search, download=False)
    #                         url = result['entries'][0]['url']
    #                     # Get the voice client and play the song
    #                     channel = self.bot.get_channel(guildData[0]['bot_vc'])
    #                     # voice_client = self.bot.voice_clients[0]
    #                     for voiceClient in self.bot.voice_clients:
    #                         print(f"{voiceClient.channel.guild.id}\n")
    #                         if voiceClient.channel.guild.id == guildData[0]['guild_id']:
    #                             voice_client = voiceClient
    #                     player = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url))
    #                     voice_client.play(player)
    #                     embed=discord.Embed()
    #                     await interaction.channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_musicCommands(bot))