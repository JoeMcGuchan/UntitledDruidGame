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

def getDiceString(roll):
    blankString = ' '.join(['◻️' for _ in range(roll.blanks)])
    pointString = ' '.join(['🔵' for _ in range(roll.points)])
    knotString = ' '.join(['💥' for _ in range(roll.knots)])
    strings = [knotString, pointString, blankString]
    return ' '.join([string for string in strings if string])

@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int):
    dice = ExplosiveRoll(number_of_dice)

    diceString = getDiceString(dice)

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

    if (prior.knots == 0):
        await ctx.send(f'{ctx.author}`s prior roll has no knots.')
        return

    prior.explode()

    currentChild = prior.childRoll
    children = [currentChild]

    while currentChild.knots > 0:
        currentChild = currentChild.childRoll
        children.append(currentChild)

    rollsString = '\n'.join([getDiceString(child) for child in children])
    totalScore = sum([child.points + child.knots for child in children]) + prior.points + prior.knots

    await ctx.send(f'{ctx.author} exploded their roll!\n{rollsString}\nTotal score: {totalScore}')

bot.run(TOKEN)