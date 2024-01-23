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
from random import randrange, randint
from time import time
from math import floor
from asyncpg import create_pool
import random
import aiohttp
import html
# bg = 'cogs/img/amongusEjectionBackground.gif'
ejectionGif = 'cogs/img/amongusEjection.gif'

class _funCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot 
    
    @commands.command()
    async def eject(self, ctx:commands.Context, ejectedPerson:Member):
        if getenv('devMode') == "False":
            random = randrange(0,2)
            possibility = "" if random == 1 else "not "
            await ctx.send(content=f'{ejectedPerson.mention} was {possibility}The Imposter')
    
    @commands.command(name='8ball', aliases=['eightball', '8b'])
    async def eightball(self, ctx:commands.Context):
        if getenv('devMode') == "False":
            answerPool = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, Definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My Reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
            num = randint(1, 20)
            if num in range(16,21):
                color = Color.red()
            elif num in range(11,16):
                color = Color.yellow()
            elif num in range(1,11):
                color = Color.green()
            embed=Embed(title=f'{answerPool[num-1]}', color=color)
            await ctx.reply(embed=embed)
        
    @commands.command()
    async def feed(self, ctx:commands.Context, member:Optional[Member]):
        if getenv('devMode') == "False":
            fridge = ["🍕", "🍔", "🍟", "🌭", "🍿", "🥓", "🥚", "🍳", "🧇", "🥞", "🧈", "🍞", "🥐", "🥨", "🥯", "🥖", "🫓", "🧀", "🥗", "🥙", "🥪", "🌮", "🌯", "🫔", "🥫", "🍖", "🍗", "🥩", "🍠", "🥟", "🥠", "🥡", "🍱", "🍙", "🍘", "🍚", "🍛", "🍜", "🦪", "🍣", "🍤", "🍥", "🥮", "🍢", "🧆", "🥘", "🍲", "🫕", "🍝", "🥣", "🥧", "🍦", "🍧", "🍨", "🍩", "🍪", "🎂", "🍰", "🧁", "🍫", "🍬", "🍭", "🍡", "🍮", "🍯", "🍼", "🥛", "🧃", "☕", "🫖", "🍵", "🧉", "🍾", "🍷", "🍸", "🍹", "🍺", "🍻", "🥂", "🥃", "🫗", "🧊", "🥤", "🧋", "🥝", "🥥", "🍇", "🍈", "🍉", "🍊", "🍋", "🍌", "🍍", "🥭", "🍎", "🍏", "🍐", "🍑", "🍒", "🍓", "🫐", "🍅", "🫒", "🍆", "🌽", "🌶️", "🫑", "🥑", "🥒", "🥬", "🥦", "🥔", "🧄", "🧅", "🥕", "🌰", "🥜", "🫘"]
            num = random.randint(1,len(fridge))
            embed = Embed(description=f'{fridge[num]}', color=int(getenv('embedColor'), 16))
            content = member.mention if member else ''
            await ctx.reply(content=content,embed=embed)
        
    @commands.command()
    async def ship(self, ctx:commands.Context, user1:Member, user2:Optional[Member]):
        if getenv('devMode') == "False":
            if user2 is None:
                user2 = ctx.author
            if user1.id == 851195035826257922 and user2.id == 839619257091227649 or user1.id == 839619257091227649 and user2.id == 851195035826257922:
                number = 100
            elif user1.id == 851195035826257922 and user2.id != 839619257091227649 or user1.id != 839619257091227649 and user2.id == 851195035826257922:
                number = 0
            else:
                number = round(random.triangular(1, 100, 80)) # generate a number using triangular distribution
            if user1.id == ctx.author.id:
                await ctx.reply("The first mention must be someone else for this command")
            elif user1.id == user2.id:
                await ctx.reply("It's important to love yourself, however, I can't help here")
            elif user1.bot or user2.bot:
                await ctx.reply("That robot can't love you, sorry...")
            else:
                if number >= 91:
                    title="💘 A perfect match 💘"
                elif number >= 75:
                    title="🥰 A great couple for sure 🥰"
                elif number >= 50:
                    title="❤️‍🩹 It won't be easy ❤️‍🩹"
                else:
                    title="💔 It's not you, its me 💔"
                embed = Embed(title=title,description=f"<@{user1.id}> ❤️ {number}% ❤️ <@{user2.id}>",color=int(getenv('embedColor'), 16))
                try:
                    await ctx.reply(embed=embed)
                except:
                    await ctx.send(embed=embed)
        
    @commands.command()
    async def hack(self, ctx:commands.Context, user:commands.MemberConverter):
        if getenv('devMode') == "False":
            messages = [
                "> Bypassing Discord firewall...",
                "> Successfully bypassed Discord's firewall. Accessing user's data...",
                "> Hacking into user's email account...",
                "> Success! Found user's email account...",
                f"> Storing all of {user.name}@gmail.com's emails",
                "> Attempting to download credit card information...",
                "> Success! Storing data in the Hive...",
                "> Welcome to the Hive"
            ]
            msg = await ctx.send(content=f"> Starting hack on {user.name}...")
            for message in messages:
                sleepTimer = random.randint(1,4)
                await sleep(sleepTimer)  # add delay for realism
                await msg.edit(content=message)
                    
    @app_commands.command(name="trivia", description="🐝A command for playing trivia🐝")
    async def triviaSlash(self, interaction:Interaction):
        if getenv('devMode') == "False":
            link = 'https://the-trivia-api.com/api/questions?limit=1'
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    data = await resp.json()
                    # print(data)
            
            if len(data[0]['correctAnswer']) > 80 or len(data[0]['incorrectAnswers'][0]) > 80 or len(data[0]['incorrectAnswers'][1]) > 80 or len(data[0]['incorrectAnswers'][2]) > 80:
                await interaction.response.send_message(content="Uh oh, an error with trivia-api has occurred please run the command again, as this is most likely a bug")
            else:
                embed = Embed(title=f"{data[0]['category']}", description=f"{data[0]['question']}", color=int(getenv('embedColor'), 16))
                embed.set_footer(text=f"id: {data[0]['id']}")
                user = interaction.user
                view = View()
                correct = Button(style=ButtonStyle.grey, label=f"{data[0]['correctAnswer']}")
                async def playAgain(interaction:Interaction):
                    if user.id == interaction.user.id:
                        view.clear_items()
                        await interaction.response.edit_message(view=view)
                        await interaction.channel.send(content="The \"`Play Again?`\" button is still in development at this time.")
                    else:
                        embed=Embed(description="🍯This button is not for you🍯", color=int(getenv('embedColor'), 16))
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                async def correctAnswerClicked(interaction:Interaction):
                    if user.id == interaction.user.id:
                        view.clear_items()
                        playagain = Button(style=ButtonStyle.secondary, label=f"Play Again?")
                        playagain.callback = playAgain
                        view.add_item(playagain)
                        embed = Embed(title="🎉CORRECT🎉", description=f"{data[0]['question']}\n\n**Answer:** *{data[0]['correctAnswer']}*", color=Color.green())
                        await interaction.response.edit_message(embed=embed, view=view)
                    else:
                        embed=Embed(description="🍯This button is not for you🍯", color=int(getenv('embedColor'), 16))
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                async def incorrectAnswerClicked(interaction:Interaction):
                    if user.id == interaction.user.id:
                        view.clear_items()
                        playagain = Button(style=ButtonStyle.secondary, label=f"Play Again?")
                        playagain.callback = playAgain
                        view.add_item(playagain)
                        embed = Embed(title="😞INCORRECT😞", description=f"{data[0]['question']}\n\n**Answer:** *{data[0]['correctAnswer']}*", color=Color.red())
                        await interaction.response.edit_message(embed=embed, view=view)
                    else:
                        embed=Embed(description="🍯This button is not for you🍯", color=int(getenv('embedColor'), 16))
                        await interaction.response.send_message(embed=embed, ephemeral=True)
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
                await interaction.response.send_message(embed=embed, view=view)

    @commands.command(name='trivia')
    async def triviaText(self, ctx:commands.Context):
        if getenv('devMode') == "False":
            link = 'https://the-trivia-api.com/api/questions?limit=1'
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    data = await resp.json()
                    # print(data)
            
            if len(data[0]['correctAnswer']) > 80 or len(data[0]['incorrectAnswers'][0]) > 80 or len(data[0]['incorrectAnswers'][1]) > 80 or len(data[0]['incorrectAnswers'][2]) > 80:
                await ctx.send(content="Uh oh, an error with trivia-api has occurred please run the command again, as this is most likely a bug")
            else:
                embed = Embed(title=f"{data[0]['category']}", description=f"{data[0]['question']}", color=int(getenv('embedColor'), 16))
                embed.set_footer(text=f"id: {data[0]['id']}")
                user = ctx.author
                view = View()
                correct = Button(style=ButtonStyle.grey, label=f"{data[0]['correctAnswer']}")
                async def playAgain(interaction:Interaction):
                    if user.id == interaction.user.id:
                        view.clear_items()
                        await interaction.message.delete()
                        await interaction.channel.send(content="The \"`Play Again?`\" button is still in development at this time.")
                    else:
                        embed=Embed(description="🍯This button is not for you🍯", color=int(getenv('embedColor'), 16))
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                async def correctAnswerClicked(interaction:Interaction):
                    if user.id == interaction.user.id:
                        view.clear_items()
                        playagain = Button(style=ButtonStyle.secondary, label=f"Play Again?")
                        playagain.callback = playAgain
                        view.add_item(playagain)
                        embed = Embed(title="🎉CORRECT🎉", description=f"{data[0]['question']}\n\n**Answer:** *{data[0]['correctAnswer']}*", color=Color.green())
                        await interaction.response.edit_message(embed=embed, view=view)
                    else:
                        embed=Embed(description="🍯This button is not for you🍯", color=int(getenv('embedColor'), 16))
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                async def incorrectAnswerClicked(interaction:Interaction):
                    if user.id == interaction.user.id:
                        view.clear_items()
                        playagain = Button(style=ButtonStyle.secondary, label=f"Play Again?")
                        playagain.callback = playAgain
                        view.add_item(playagain)
                        embed = Embed(title="😞INCORRECT😞", description=f"{data[0]['question']}\n\n**Answer:** *{data[0]['correctAnswer']}*", color=Color.red())
                        await interaction.response.edit_message(embed=embed, view=view)
                    else:
                        embed=Embed(description="🍯This button is not for you🍯", color=int(getenv('embedColor'), 16))
                        await interaction.response.send_message(embed=embed, ephemeral=True)
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
                await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_funCommands(bot))