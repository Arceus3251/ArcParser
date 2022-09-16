# ArcPy
import json

import discord

import tatsu.exceptions
from tatsu import parse
from tatsu.util import asjson

import dice

class Settings:
    def __init__(self) -> None:
        with open("settings.json") as f:
            j = json.load(f)
        self.prefix = j["prefix"]
    
def main():
    with open('AUTHTOKEN.txt', 'r') as f:
        TOKEN = f.read().strip()

    settings = Settings()

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

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
        ### COMMANDS
        ### dice parsing
        elif message.content.startswith(settings.prefix):
            expression = message.content.removeprefix(settings.prefix)
            if expression.isdigit(): 
                await message.channel.send(f"```\n{int(expression)}\n```")
            else:
                try:
                    ast = parse(dice.GRAMMAR, expression, semantics = dice.DiceSemantics())
                except tatsu.exceptions.ParseException as e:
                    await message.channel.send(f"```ParseException: {e}```")
                    return
                j = json.dumps(asjson(ast))
                expression_input = json.loads(j)
                dList: list[list[int]] = []
                await message.channel.send(f"```json\n{j}\n```")
                await message.channel.send(f'```# {dice.calculate(expression_input, dList)}\nDetails:({expression}) {dList}```')

    client.run(TOKEN)

if __name__ == "__main__":
    main()