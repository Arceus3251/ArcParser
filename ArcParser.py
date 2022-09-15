# ArcPy
import json
import random

import discord

import tatsu.exceptions
from tatsu import parse
from tatsu.util import asjson

GRAMMAR = """
@@grammar::CALC
start = expression $ ;

expression
    =
    | expression '+' term
    | expression '-' term
    | term
    ;
    
term
    =
    | term '*' dice
    | term '/' dice
    | dice
    ;

dice
    =
    | dice /[d]+/ factor
    | factor
    ;
    
factor
    =
    | '(' expression ')'
    | number
    ;
    
number = /\d+/;
"""

def operate(var2: str, operator: str, var1: str):
    if operator == "+":
        return float(var1)+float(var2)
    elif operator == "-":
        return float(var1)-float(var2)
    elif operator == "*":
        return float(var1)*float(var2)
    elif operator == "/":
        return float(var1)/float(var2)

def calculate(expression):
    expression = expression.replace('["(",', "")
    expression = expression.replace(',")"]', "")
    expression = expression.replace('"', "")
    expression = expression.replace(",", "")

    data = []
    for e in expression:
        data.append(e)
        if e == "]":
            data.pop()
            new_data = operate(data.pop(), data.pop(), data.pop())
            data.pop()
            data.append(str(new_data))
    return data[0]

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
    elif message.content.startswith("!"):
        expression = message.content.removeprefix("!")
        result = dice_parse(expression)
        total = 0
        for a in result:
            total += sum(a)
        message_out = f"{total}\n{expression}: {result}"
        await message.channel.send(message_out)
    ### dice parsing
    elif message.content.startswith("$"):
        expression = message.content.removeprefix("$")
        try:
            ast = parse(GRAMMAR, expression)
        except tatsu.exceptions.ParseException as e:
            await message.channel.send(f"```ParseException: {e}```")
            return
        j = json.dumps(asjson(ast), indent=2)
        j = j.replace("\n", "")
        j = j.replace(" ", "")
        await message.channel.send(f"```json\n{j}\n```")
        await message.channel.send(calculate(j))

client.run(TOKEN)
