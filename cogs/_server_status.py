from discord.ext import commands, tasks
from discord import Embed, app_commands, Interaction, Member, message, Color
from logging import info
from dotenv import load_dotenv
from os import getenv
from logging import info
from asyncio import sleep
from aiohttp import ClientSession


class _server_status(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @tasks.loop()
    async def update_server_status(self):
        async with ClientSession() as session:
            # Replace 'http://example.com/api' with the actual API endpoint you want to call
            async with session.get(getenv('SERVER_API')) as response:
                if response.status == 200:
                    site_data = await response.json()
                    # Process the JSON data as needed
                    # print(site_data)
                else:
                    print(f"Failed to retrieve data: {response.status}")
        msg_id = 1202773805034905620
        channel_id = 1202765210859868221
        guild_id = 1200518682221236244

        guild = await self.bot.fetch_guild(guild_id)
        channel = await guild.fetch_channel(channel_id)
        message = await channel.fetch_message(msg_id)

        server = site_data['data']
        server_attributes = server['attributes']
        server_id = server_attributes['id']
        server_name = server_attributes['name']
        server_ip = server_attributes['ip']
        server_port = server_attributes['port']
        server_players = server_attributes['players']
        server_max_players = server_attributes['maxPlayers']
        server_status = server_attributes['status']
        details = server_attributes['details']
        server_version = details['version']

        if server_status == 'online':
            thumbnail_url = 'https://palworld.wiki.gg/images/3/34/Tanzee.png'
            color = Color.green()
        elif server_status == 'dead':
            thumbnail_url = 'https://palworld.wiki.gg/images/d/dd/Foxparks.png'
            color = Color.red()
        embed = Embed(
            title=f'{server_name} Status',
            description=f'Status: `{server_status}`\nPlayers: `{server_players}/{server_max_players}`\nAddress: `{server_ip}:{server_port}`\nServer ID: `{server_id}`',
            url='https://www.battlemetrics.com/servers/palworld/25797556',
            color=color
        ).set_footer(
            text=f'{server_version}'
        ).set_thumbnail(
            url=thumbnail_url
        )

        await message.edit(content='', embed=embed)

        await sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):
        info('\x1b[6;30;42m' + f'{__name__} Cog - Online' + '\x1b[0m')
        if not self.update_server_status.is_running():
            self.update_server_status.start()

# MAKE SURE YOU UPDATE YOUR CLASS NAME HERE IF YOU CHANGE IT AT TOP (THE CLASS NAME IN THIS FILE IS _commands < - YOU CAN TELL BY THE GREEN TEXT AFTER class)


async def setup(bot):
    await bot.add_cog(_server_status(bot))
