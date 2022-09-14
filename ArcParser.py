# ArcPy

import discord
import parser
import random

from typing import List

with open('AUTHTOKEN.txt', 'r')as f:
    TOKEN = f.read().strip()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def dice_parse(expression):
    expressList = expression.split("d")
    exportList = List[int]
    for i in range(len(expressList)):
        expressList[i] = eval(parser.expr(expressList[i]).compile())
    for e in range(expressList[0]):
        exportList.append(random.randrange(expressList[1]))
    return exportList

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("ArcPing"):
        await message.channel.send("Hello world!")
    if message.content.startswith("$"):
        expression = message.content.replace("$", "")
        result = dice_parse(expression)
        sum = 0
        for a in result:
            sum += a
        messageOut = """{}
        {}:{}"""
        await message.channel.send(messageOut.format(sum, expression, result))
    if message.content.startswith("ArcRand"):
        expression = message.content.replace("ArcRand", "")
        await message.channel.send(random.randrange(int(expression)))

client.run(TOKEN)
