import string
import random
import csv
import asyncio
from discord import Embed
from os import getenv

async def check(self, user_id):
    e = await self.bot.pg_con.fetch('SELECT * FROM core WHERE user_id = $1', user_id)
    if e == []:
        await self.bot.pg_con.execute('INSERT INTO core (user_id) VALUES ($1)', user_id)
        e=await self.bot.pg_con.fetch('SELECT * FROM core WHERE user_id = $1', user_id)
    
    return e

async def sendMessage(self, ctx, content, embed):
    if content == "":
        content = f"{ctx.author.mention}"
    try:
        await ctx.reply(embed=embed)
    except:
        await ctx.send(embed=embed, content=content)

async def generate_random_string(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

async def get_row(file_path, value):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == value:
                return row
    return None

async def add_row(file_path, userId):
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        new_row = [userId, 1]
        writer.writerow(new_row)
    return new_row

async def update_row(file_path, userId):
    data = []
    updated_value = None
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == userId:
                row[1] = str(int(row[1]) + 1)  # Increment the value in the second column
                updated_value = int(row[1])  # store the updated value
            data.append(row)

    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    return updated_value

async def remove_row(file_path, userId):
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Only append to data if the userId does not match
            if row[0] != userId:
                data.append(row)
    
    # Write back the data without the row of the cheating user
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

async def get_top_10_nitro_point_holders(file_path):
    data = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append((row[0], int(row[1])))
    data.sort(key=lambda x: (-x[1], x[0]))
    
    top_10 = data[:10]
    
    while len(top_10) < 10:
        top_10.append(('pending', 0))
        
    top_10_str = [f'<@{user[0]}> **-** `{user[1]}`' if user[0] != 'pending' else f'{user[0]} **-** `{user[1]}`' for user in top_10]
    
    return top_10_str

async def clear_csv(file_path):
    headers = None
    # read the headers first
    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
    
    # write back only the headers
    if headers is not None:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    else:
        print(f"No headers found in the csv file at {file_path}")

async def createNitroPuzzle():
    puzzleNum = random.randint(1,2)
    if puzzleNum is 1:
        # TEXT TYPING
        answer = await generate_random_string(6)
        embed=Embed(title='Nitro Event', color=int(getenv('embedColor'), 16), description=f'Type in: `{answer}` for a nitro point')
        return True, answer, embed
    elif puzzleNum is 2:
        # MATH PROBLEM
        a, b = random.randint(1,100), random.randint(1,100)
        equationType = random.randint(1,2)
        answer = str(a+b) if equationType == 1 else str(a-b)
        description = f'What is `{a} + {b}`? Answer for a nitro point' if equationType == 1 else f'What is `{a} - {b}`? Answer for a nitro point'
        embed=Embed(title='Nitro Event', color=int(getenv('embedColor'), 16), description=description)
        return True, answer, embed
    else:
        print('encountered an error')
        return False, 'Fail', 'Fail'
    
async def encode_question(question):
    substitution_dict = {
        'a': 'α',
        'c': 'ϲ',
        'e': 'е',
        'f': 'ƒ',
        'g': 'ɡ',
        'h': 'һ',
        'i': 'і',
        'j': 'ϳ',
        'k': 'κ',
        'l': 'Ɩ',
        'o': 'ο',
        'r': 'г',
        's': 'ѕ',
        'v': 'ν',
        'x': 'х',
        'y': 'у',

        'A': 'Α',
        'B': 'Β',
        'C': 'Ϲ',
        'G': 'Ԍ',
        'I': 'Ι',
        'J': 'Ј',
        'K': 'Κ',
        'M': 'Ḿ',
        'N': 'Ν',
        'O': 'Ο',
        'P': 'Ρ',
        'R': 'Ṙ',
        'S': 'Ѕ',
        'T': 'Τ',
        'V': 'Ѵ',
        'W': 'Ԝ',
        'X': 'Χ',
        'Y': 'Υ',
        'Z': 'Ζ',
        }
    
    encoded_question = ''
    for char in question:
        if char in substitution_dict:
            encoded_question += substitution_dict[char]
        else:
            encoded_question += char
    return encoded_question

async def clear_guild_queue(guildId):
    data = []
    with open('../longTermData/musicQueue.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Only append to data if the userId does not match
            if row[0] != guildId:
                data.append(row)
    
    # Write back the data without the row of the cheating user
    with open('../longTermData/musicQueue.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

async def add_to_queue(guildId, query):
    exists = False
    with open('../longTermData/musicQueue.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == guildId:
                exists = True
    if exists:
        with open('../longTermData/musicQueue.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            new_row = [guildId, str(list(query))]
            writer.writerow(new_row)
            return new_row[1]
    else:
        data = []
        updated_value = None
        with open('../longTermData/musicQueue.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == guildId:
                    row[1] = str(list(row[1]).append(query))  # Increment the value in the second column
                    updated_value = row[1]
                data.append(row)

        with open('../longTermData/musicQueue.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        return updated_value