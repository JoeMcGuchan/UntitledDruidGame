# bottica.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

class ExplosiveRoll:
    def __init__(self, diceNumber : int):
        results = [
            random.choice(range(1, 7))
            for _ in range(diceNumber)
        ]

        self.blanks = len([result for result in results if result <= 3])
        self.points = len([result for result in results if (result == 4 or result == 5)])
        self.knots = len([result for result in results if result == 6])

    def explode(self):
        self.childRoll = ExplosiveRoll(self.knots)
        if (self.childRoll.knots > 0):
            self.childRoll.explode()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
priorRolls = {}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int):
    dice = ExplosiveRoll(number_of_dice)

    blankString = ' '.join(['◻️' for _ in range(dice.blanks)])
    pointString = ' '.join(['🔵' for _ in range(dice.points)])
    knotString = ' '.join(['💥' for _ in range(dice.knots)])
    diceString = f'{knotString} {pointString} {blankString}'

    await ctx.send(f'{ctx.author} rolled {number_of_dice} dice\n{diceString}\nScore: {dice.points + dice.knots}\nKnots: {dice.knots}')
    if (dice.knots > 0):
        await ctx.send(f'Explode? Use "!explode"')

    priorRolls[ctx.author] = dice

@bot.command(name='explode', help='Explodes dice.')
async def explode(ctx):
    if not (ctx.author in priorRolls):
        await ctx.send(f'{ctx.author} has no prior roll to explode.')
        return

    prior = priorRolls[ctx.author]
    prior.explode()
    await ctx.send(f'{ctx.author} exploded their roll!')

    currentChild = prior.childRoll
    children = [currentChild]

    while currentChild.knots > 0:
        currentChild = currentChild.childRoll
        children.append(currentChild)

    await ctx.send(f'number of children {len(children)}')

bot.run(TOKEN)