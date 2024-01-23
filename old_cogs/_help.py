from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member, ui, ButtonStyle, TextStyle, Color, File, file, ChannelType, channel, DMChannel
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
import Paginator

class _help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot

    @commands.command()
    async def oauth(self, ctx:commands.Context):
        if getenv('devMode') == "False":
            if ctx.author.guild_permissions.manage_guild:
                oauthlink = getenv('oauth')
                await ctx.reply(f'Use the following link to re-add the bot to your server with the most up to date permissions.\n{oauthlink}')
            else:
                await ctx.reply('You need the `manage_guild` permission to use this')
        
    @commands.command()
    async def help(self, ctx:commands.Context, subject:Optional[str]):
        if getenv('devMode') == "False":
            mainPage = Embed(
                title='Help and Resources',
                description=f'Welcome {ctx.author.name}, Here you can find a long and detailed list of data related to each item the bot supports. If you want a feature implemented or updated, please dm the bot with your request and it will be forwarded to the developer.',
                color=int(getenv('embedColor'), 16)
            )
            funCommands = Embed(
                title='Fun Commands',
                description=f'These commands are just for fun, they offer no true function beyond that (not that they need to)',
                color=int(getenv('embedColor'), 16)
            ).add_field(
                name='Eject',
                value='Uncover if a user is an imposter :amongus: `bzz eject @person',
                inline=False
                ).add_field(
                name='Eightball / 8ball',
                value='Ask the ball, for it knows the real answers `bzz 8ball *question*`',
                inline=False
                ).add_field(
                name='Feed',
                value='Generate food for yourself or @ someone to make some for them. `bzz feed *@person*`',
                inline=False
                ).add_field(
                name='Ship',
                value='Want to see if you match with someone or if two others match? just @ them, or @ both the people you want to ship !! `bzz ship @person @someone`'
                ).set_footer(text='* - An optional field'
                ).add_field(
                name='Trivia',
                value='Play a round of trivia. `/trivia`'
                ).add_field(
                name='Hack',
                value='Hack another person! This command is a joke, no information is revealed or hacked. `bzz hack @user`'
                )
            rolesReadOnly = Embed(
                title='Read Only Role Commands',
                description='These commands only read the roles and return data from what you request.',
                color=int(getenv('embedColor'), 16)
            ).add_field(
                name='Inrole',
                value='Lets you check how many users in the server, have the specified role, you can use either the role mention or the id. `bzz inrole ^@role/role-id^`'
                ).set_footer(text='^ - Mutliple formats allowed')
            rolesAction = Embed(
                title='Action Based Role Commands',
                description='These commands make changes to the servers roles or (un)assigns roles to users. None of these currently exist.',
                color=int(getenv('embedColor'), 16)
            )
            channelsReadOnly = Embed(
                title='Read Only Channel Commands',
                description='These commands provide data for channels, and do not make any changes anywhere.',
                color=int(getenv('embedColor'), 16)
            ).add_field(
                name='channel_info',
                value='This command provides data relating to the channel it is ran in, useful for mobile users or quick checking a channels core settings. `bzz channel_info`',
                inline=False
                )
            channelsAction = Embed(
                title='Action Based Channel Commands',
                description='These commands make actual changes to a channels settings, name, or permissions.',
                color=int(getenv('embedColor'), 16)
            ).add_field(
                name='channel_name',
                value='Updates the channel name. `bzz channel_name \"newName\"`',
                inline=False
                ).add_field(
                name='channel_nsfw',
                value='This command will toggle the nsfw state of a channel useful for servers that are updating from one to the other. `bzz channel_nsfw true`',
                inline=False
                )
            categoryReadOnly = Embed(
                title='Read Only Category Commands',
                description='These commands provide data for categories, and do not make any changes anywhere. None of these currently exist.',
                color=int(getenv('embedColor'), 16)
            )
            categoryAction = Embed(
                title='Action Based Category Commands',
                description='These commands make changes to categories in your server, very very useful for adding new categories that are duplicates of other ones.',
                color=int(getenv('embedColor'), 16)
            ).add_field(
                name='category_name',
                value='This command will update the category name to whatever you specify, will be updated for multiword names soon. `bzz category_name \"newName\"`',
                inline=False
                ).add_field(
                name='category_clone',
                value='This command clones the first category over the second one. The first category is a template that replaces the second one. `bzz category_clone template_category_id target_category_id`',
                inline=False
                )
            inviteCommands = Embed(
                title='Invite Commands/Partner Commands',
                description='These commands are useful for partnering or just giving invite links without granting the permission.',
                color=int(getenv('embedColor'), 16)
            ).add_field(
                name='invite_create',
                value='While the member portion is just for mentioning their name, eventually we will support invite-per-user tracking, to make things easier overall. `bzz invite_create @person`',
                inline=False            
                ).add_field(
                name='invite_delete',
                value='Deletes an invite by code, cannot be undone. Useful if you accidentally make an invite, or are finished with it. `bzz invite_delete \"inviteCode\"`'
                ).add_field(
                name='invite_check',
                value='This command allows a user to check their invites via the invite code they have saved, we recommend pinning a message with just the invite code in the dms of the partner-manager, and the owner, again, support us and we can create the tracker system sooner. `bzz invite_check \"inviteCode\"`',
                inline=False
                )
            if subject is None:
                embeds = [
                            mainPage,
                            funCommands,
                            rolesReadOnly,
                            rolesAction,
                            channelsReadOnly,
                            channelsAction,
                            categoryReadOnly,
                            categoryAction,
                            inviteCommands
                        ]
                await Paginator.Simple().start(ctx=ctx, pages=embeds)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if getenv('devMode') == "False":
            if isinstance(message.channel, channel.DMChannel) and message.author.id is not self.bot.user.id and int(message.author.id) is not int(getenv('devId')):
                embed=Embed(color=int(getenv('embedColor'), 16), description=f'{message.content}').set_footer(text=f'Sent by: {message.author.display_name}')
                content = f'{message.author.mention}\n{message.author.id}'
                developer = await self.bot.fetch_user(int(getenv('devId')))
                await developer.send(embed=embed, content=content)
                await message.channel.send('I have forwarded your message to a developer.')
            elif self.bot.user.mention in message.content and message.author is not self.bot.user:
                await message.reply(f"{message.author.mention}, My prefix is `bzz `\nUse `bzz help` if you need support.")

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
    
# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)
async def setup(bot):
    await bot.add_cog(_help(bot))