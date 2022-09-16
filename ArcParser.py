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
    | left:expression op:'+' ~ right:term
    | left:expression op:'-' ~ right:term
    | term
    ;
    
term
    =
    | left:term op:'*' ~ right:dice
    | left:term op:'/' ~ right:dice
    | dice
    ;

dice
    =
    | left:dice op:/[d]+/ ~ right:factor
    | factor
    ;
    
factor
    =
    | '(' ~ @:expression ')'
    | number
    ;
    
number = /\d+/;
"""

class DiceSemantics:
    def number(self, ast):
        return int(ast)

def operate(var2: str, operator: str, var1: str, dList):
    outputVar = 0.0
    if operator == "+":
        outputVar = float(var1)+float(var2)
    elif operator == "-":
        outputVar = float(var1)-float(var2)
    elif operator == "*":
        outputVar = float(var1)*float(var2)
    elif operator == "/":
        outputVar = float(var1)/float(var2)
    elif operator == "d":
        return dice_parse(int(var1), int(var2), dList)
    if outputVar.is_integer(): return int(outputVar)
    return outputVar

def calculate(expression, dList):
    expression = expression.replace('["(",', "")
    expression = expression.replace(',")"]', "")
    expression = expression.replace('"', "")
    expression = expression.replace(",", "")

    data = []
    digitStack = []
    for e in expression:
        if e.isdigit():
            digitStack.append(e)
        elif e == "]":
            if len(digitStack)>0:
                num: str = ""
                for f in digitStack:
                    num = num + f
                data.append(num)
                digitStack = []
            
            new_data = operate(data.pop(), data.pop(), data.pop(), dList)
            data.pop()
            data.append(str(new_data))
        else:
            if len(digitStack)>0:
                num: str = ""
                for f in digitStack:
                    num = num + f
                data.append(num)
                digitStack = []
            data.append(e)
    return data[0]

with open('AUTHTOKEN.txt', 'r') as f:
    TOKEN = f.read().strip()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def dice_parse(x:int, y:int, dList: list[list[int]]) -> int:
    s = []
    sum = 0
    for _ in range(x):
        currVal = random.randint(1, y)
        s.append(currVal)
        sum += currVal
    dList.append(s)
    return sum
    

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
    ### dice parsing
    elif message.content.startswith("&"):
        expression = message.content.removeprefix("&")
        if expression.isdigit(): 
            await message.channel.send(f"```\n{int(expression)}\n```")
        else:
            try:
                ast = parse(GRAMMAR, expression, semantics = DiceSemantics())
            except tatsu.exceptions.ParseException as e:
                await message.channel.send(f"```ParseException: {e}```")
                return
            j = json.dumps(asjson(ast))
            await message.channel.send(ast)
            dList: list[list[int]] = []
            await message.channel.send(f"```json\n{j}\n```")
            await message.channel.send(f'```# {calculate(j, dList)}\nDetails:({expression}) {dList}```')

client.run(TOKEN)
