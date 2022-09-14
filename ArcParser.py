# ArcPy

import random
from re import S

import discord

with open('AUTHTOKEN.txt', 'r') as f:
    TOKEN = f.read().strip()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def dice_parse(expression: str) -> list[list[int]]:
    express_list = expression.split()
    export_list: list[list[int]] = []
    for e in express_list:
        s = []
        x, y = e.split("d", 1)
        x = int(x)
        y = int(y)
        for _ in range(x):
            s.append(random.randint(1, y))
        export_list.append(s)
    return export_list
    

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    ### ping
    if message.content.startswith("ArcPing"):
        await message.channel.send("Hello world!")
    ### dice roll
    elif message.content.startswith("$"):
        expression = message.content.removeprefix("$")
        result = dice_parse(expression)
        total = 0
        for a in result:
            total += sum(a)
        message_out = f"{total}\n{expression}: {result}"
        await message.channel.send(message_out)

client.run(TOKEN)
