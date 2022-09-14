# ArcPy

import discord
import random

with open('AUTHTOKEN.txt', 'r') as f:
    TOKEN = f.read().strip()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def dice_parse(expression):
    express_list = expression.split("d")
    export_list: list[int] = []
    return export_list
    

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("ArcPing"):
        await message.channel.send("Hello world!")
    elif message.content.startswith("$"):
        expression = message.content.replace("$", "")
        result = dice_parse(expression)
        sum = 0
        for a in result:
            sum += a
        message_out = f"{sum}\n{expression}:{result}"
        await message.channel.send(message_out)
    elif message.content.startswith("ArcRand"):
        expression = message.content.replace("ArcRand", "")
        await message.channel.send(random.randrange(int(expression)))

client.run(TOKEN)
