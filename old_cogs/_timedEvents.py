from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member, ui, ButtonStyle, TextStyle, Color, File, file, Message
from discord.ui import Button, View
from typing import Optional
from logging import info
from dotenv import load_dotenv
from os import environ, getenv
from logging import info
from asyncio import sleep
from ..cogs._python_commands import encode_question, get_row, add_row, update_row, remove_row, get_top_10_nitro_point_holders, clear_csv, createNitroPuzzle
from random import randrange
from time import time
from math import floor
from asyncpg import create_pool
import aiohttp
import pytube
import random
nitroPointsCsv = 'longTermData/nitroPoints.csv'

class _timedEvents(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
    
    @tasks.loop()
    async def nitroChance(self):
        if getenv('devMode') == "False":
            difficulty = getenv('triviaDifficulty')
            luno = await self.bot.fetch_guild(1044055313973772379)
            lunoChat = await luno.fetch_channel(1044079515586007090)
            link = f'https://the-trivia-api.com/v2/questions?limit=1&difficulty={difficulty}'
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    data = await resp.json()
                    # print(data)
            
            if len(data[0]['correctAnswer']) > 80 or len(data[0]['incorrectAnswers'][0]) > 80 or len(data[0]['incorrectAnswers'][1]) > 80 or len(data[0]['incorrectAnswers'][2]) > 80:
                await lunoChat.send(content="Uh oh, an error with trivia-api has occurred please run the command again, as this is most likely a bug")
            else:
                question = await encode_question(data[0]['question']['text'])
                embed = Embed(title=f"{data[0]['category']}", description=f"{question}", color=int(getenv('embedColor'), 16))
                embed.set_footer(text=f"id: {data[0]['id']}")
                view = View()
                correct = Button(style=ButtonStyle.grey, label=f"{data[0]['correctAnswer']}")
                async def correctAnswerClicked(interaction:Interaction):
                    await interaction.message.delete()
                    row = await get_row(nitroPointsCsv, str(interaction.user.id))
                    if row:
                        # update the line with a + 1
                        points = await update_row(nitroPointsCsv, str(interaction.user.id))
                    else:
                        # add a line with a count of 1
                        await add_row(nitroPointsCsv, str(interaction.user.id))
                        points = 1
                    pointText = 'points' if points > 1 else 'point'
                    view.clear_items()
                    embed = Embed(title="🎉CORRECT🎉", description=f"{data[0]['question']['text']}\n**Answer:** *{data[0]['correctAnswer']}*\n\n{interaction.user.mention}, You now have `{points} {pointText}` towards a free 10$ nitro", color=Color.green())
                    msg = await lunoChat.send(embed=embed, view=view)
                    nitroEventLogChannel = await luno.fetch_channel(1133282441377886279)
                    embed=Embed(title=f'Nitro Point Won', description=f'{interaction.user.mention} has successfully entered the nitro events code', color=Color.green()).set_thumbnail(url=interaction.user.display_avatar)
                    await nitroEventLogChannel.send(embed=embed)
                    if points >= 100:
                        STAFFCHAT = luno.get_channel(1044096940037656646)
                        embed=Embed(title=f'NITRO EVENT WON', description=f'{interaction.user.mention} has won a 10$ nitro gift code', color=Color.red()).set_thumbnail(url=interaction.user.display_avatar)
                        await STAFFCHAT.send(embed=embed)
                    await sleep(15)
                    try:await msg.delete()
                    except:None
                async def incorrectAnswerClicked(interaction:Interaction):
                    view.clear_items()
                    embed = Embed(title="🚫INCORRECT🚫", description=f"{data[0]['question']['text']}\n\n**Answer:** *{data[0]['correctAnswer']}*", color=Color.red())
                    await interaction.message.delete()
                    msg = await lunoChat.send(embed=embed, view=view)
                    await sleep(15)
                    try:await msg.delete()
                    except:None
                incorrect1 = Button(style=ButtonStyle.grey, label=f"{data[0]['incorrectAnswers'][0]}")
                incorrect2 = Button(style=ButtonStyle.grey, label=f"{data[0]['incorrectAnswers'][1]}")
                incorrect3 = Button(style=ButtonStyle.grey, label=f"{data[0]['incorrectAnswers'][2]}")
                correct.callback = correctAnswerClicked
                incorrect1.callback = incorrectAnswerClicked
                incorrect2.callback = incorrectAnswerClicked
                incorrect3.callback = incorrectAnswerClicked
                num = randrange(1,4)
                if num == 1:
                    view.add_item(correct)
                    view.add_item(incorrect1)
                    view.add_item(incorrect2)
                    view.add_item(incorrect3)
                elif num == 2:
                    view.add_item(incorrect1)
                    view.add_item(correct)
                    view.add_item(incorrect2)
                    view.add_item(incorrect3)
                elif num == 3:
                    view.add_item(incorrect1)
                    view.add_item(incorrect2)
                    view.add_item(correct)
                    view.add_item(incorrect3)
                elif num == 4:
                    view.add_item(incorrect1)
                    view.add_item(incorrect2)
                    view.add_item(incorrect3)
                    view.add_item(correct)
                msg = await lunoChat.send(embed=embed, view=view)
                await sleep(30)
                try:await msg.delete()
                except:None
            num = random.randint(780, 1020)
            await sleep(num)

    @tasks.loop()
    async def nitroPointLeaderBoard(self):
        if getenv('devMode') == "False":
            top_10 = await get_top_10_nitro_point_holders(nitroPointsCsv)
            embed=Embed(color=int(getenv('embedColor'), 16),title='Nitro Points Leaderboard',
                        description=f'{top_10[0]}\n{top_10[1]}\n{top_10[2]}\n{top_10[3]}\n{top_10[4]}\n{top_10[5]}\n{top_10[6]}\n{top_10[7]}\n{top_10[8]}\n{top_10[9]}\n')
            leaderboardMessageChannel = self.bot.get_channel(1134322319070859274)
            try:
                leaderboardMessage = await leaderboardMessageChannel.fetch_message(1134323638020096101)
                await leaderboardMessage.edit(content=None, embed=embed)
            except:
                await leaderboardMessageChannel.send(embed=embed)
            await sleep(1800) # runs every 30 minutes

    @commands.command()
    async def nitropoints_clear(self, ctx:commands.Context):
        if ctx.author.guild_permissions.administrator:
            if ctx.guild.id == 1044055313973772379:
                await clear_csv(nitroPointsCsv)
                await ctx.reply('Csv file was cleared for nitro points data')

    @commands.command()
    async def nitropoints(self, ctx:commands.Context, member:Optional[Member]):
        if getenv('devMode') == "False":
            user = member if member else ctx.author
            row = await get_row(nitroPointsCsv, str(user.id))
            print(row)
            if row:
                await ctx.reply(f'{user.mention} currently has `{row[1]}` nitro points')
            else:
                await ctx.reply(f'{user.mention} currently has `0` nitro points')
    
    # @commands.Cog.listener()
    # async def on_message(self, message:Message):
    #     if getenv('devMode') == "False":
    #         if message.author.bot is True:
    #             return
    #         luno = self.bot.get_guild(1044055313973772379)
    #         lunoChat = luno.get_channel(1044079515586007090)
    #         if message.channel is lunoChat:
    #             randomText = getenv('NITROCHANCEANSWER', None)
    #             nitroChanceMessage = getenv('NITROCHANCEMESSAGE', None)
    #             if randomText is None:
    #                 return
    #             if nitroChanceMessage is None:
    #                 return
    #             if randomText == message.content:
    #                 # csv process
    #                 row = await get_row(nitroPointsCsv, str(message.author.id))
    #                 if row:
    #                     # update the line with a + 1
    #                     points = await update_row(nitroPointsCsv, str(message.author.id))
    #                 else:
    #                     # add a line with a count of 1
    #                     await add_row(nitroPointsCsv, str(message.author.id))
    #                     points = 1
    #                 pointText = 'points' if points > 1 else 'point'
    #                 nitroEventLogChannel = luno.get_channel(1133282441377886279)
    #                 embed=Embed(title=f'Nitro Point Won', description=f'{message.author.mention} has successfully entered the nitro events code', color=Color.green()).set_thumbnail(url=message.author.display_avatar)
    #                 await nitroEventLogChannel.send(embed=embed)
    #                 nitroChanceMessage = await lunoChat.fetch_message(int(nitroChanceMessage))
    #                 embed=Embed(description=f'{message.author.mention}, You now have `{points} {pointText}` towards a free 10$ nitro', color=int(getenv('embedColor'), 16))
    #                 await nitroChanceMessage.edit(embed=embed, content=None)
    #                 if 'RANDOMTEXT' in environ:
    #                     del environ['NITROCHANCEANSWER']
    #                 if 'NITROCHANCEMESSAGE' in environ:
    #                     del environ['NITROCHANCEMESSAGE']
    #                 if points >= 100:
    #                     STAFFCHAT = luno.get_channel(1044096940037656646)
    #                     embed=Embed(title=f'NITRO EVENT WON', description=f'{message.author.mention} has won a 10$ nitro gift code', color=Color.red()).set_thumbnail(url=message.author.display_avatar)
    #                     await STAFFCHAT.send(embed=embed)
    #         else:return
    
    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
        if not self.nitroChance.is_running():
            self.nitroChance.start()
        if not self.nitroPointLeaderBoard.is_running():
            self.nitroPointLeaderBoard.start()
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_timedEvents(bot))