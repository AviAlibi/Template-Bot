import string
import random
import csv
import asyncio
from discord import Embed
from os import getenv


async def is_this_user_the_developer(self, user_id):
    return True if user_id is getenv('DEVELOPER_ID') else False
