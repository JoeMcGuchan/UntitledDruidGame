# bottica.py
import os
import random
import csv
import re

from discord.ext import commands
from dotenv import load_dotenv

blankEmoji = '<:blank_die:767499216678551582>'
pointEmoji = '<:point_die:767499240620163073>'
knotEmojiKey = '<knot>'
knotEmoji = '<:knot_die:767499232562118706>'

class ExplosiveRoll:
    exploded = False

    def __init__(self, diceNumber : int):
        results = [
            random.choice(range(1, 7))
            for _ in range(diceNumber)
        ]

        self.blanks = len([result for result in results if result <= 3])
        self.points = len([result for result in results if (result == 4 or result == 5)])
        self.knots = len([result for result in results if result == 6])

    def explode(self):
        self.exploded = True
        self.childRoll = ExplosiveRoll(self.knots)
        if (self.childRoll.knots > 0):
            self.childRoll.explode()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
priorRolls = {}

staminaDeck = []
convictionDeck = []
authorityDeck = []

with open('../cards/wounds.csv', newline='') as csvWounds:
    woundsReader = csv.DictReader(csvWounds, delimiter=',', quotechar='"')
    for row in woundsReader:
        for _ in range(int(row["Quantity"])):
            if row["Type"] == "STAMINA":
                staminaDeck.append(row)
            elif row["Type"] == "CONVICTION":
                convictionDeck.append(row)
            elif row["Type"] == "AUTHORITY":
                authorityDeck.append(row)
            else:
                print("Couldn't parse row")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

def getDiceString(roll):
    blankString = ' '.join([blankEmoji for _ in range(roll.blanks)])
    pointString = ' '.join([pointEmoji for _ in range(roll.points)])
    knotString = ' '.join([knotEmoji for _ in range(roll.knots)])
    strings = [knotString, pointString, blankString]
    return ' '.join([string for string in strings if string])

@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int):
    if (number_of_dice <= 0):
        await ctx.send(f'{ctx.author.display_name}\'s roll rejected. Too small.')
        return

    if (number_of_dice > 200):
        await ctx.send(f'{ctx.author.display_name}\'s roll rejected. Too large.')
        return

    dice = ExplosiveRoll(number_of_dice)

    diceString = getDiceString(dice)

    await ctx.send(f'{ctx.author.display_name} rolled {number_of_dice} dice\n{diceString}\nScore: {dice.points + dice.knots}\nKnots: {dice.knots}')
    if (dice.knots > 0):
        await ctx.send(f'Explode? Use "!explode"')

    priorRolls[ctx.author] = dice

@bot.command(name='explode', help='Explodes dice.')
async def explode(ctx):
    if not (ctx.author in priorRolls):
        await ctx.send(f'{ctx.author.display_name} has no prior roll to explode.')
        return

    prior = priorRolls[ctx.author]

    if (prior.knots == 0):
        await ctx.send(f'{ctx.author.display_name}\'s prior roll has no knots.')
        return

    if prior.exploded:
        await ctx.send(f'{ctx.author.display_name} has already exploded their roll.')
        return

    prior.explode()

    currentChild = prior.childRoll
    children = [currentChild]

    while currentChild.knots > 0:
        currentChild = currentChild.childRoll
        children.append(currentChild)

    rollsString = '\n'.join([getDiceString(child) for child in children])
    totalScore = sum([child.points + child.knots for child in children]) + prior.points + prior.knots

    await ctx.send(f'{ctx.author.display_name} exploded their roll!\n{rollsString}\nTotal score: {totalScore}')

def getWoundString(card):
    name = f'**{card["Name"].upper()}**'

    description = card["Description"]
    if description:
        description = f'*{description}*'

    whenDrawn = card["When Drawn"]
    if whenDrawn:
        whenDrawn = f'**When Drawn:** {whenDrawn}'

    toRemove = card["To Remove"]
    if toRemove:
        toRemove = f'**To Remove:** {toRemove}'

    onRemoval = card["On Removal"]
    if onRemoval:
        onRemoval = f'**On Removal:** {onRemoval}'

    footer = card["Footer"]
    if footer:
        footer = f'*({footer})*'

    strings = [name, description, whenDrawn, toRemove, onRemoval, footer]
    return '\n'.join([string for string in strings if string])

def drawStam(number_of_wounds):
    return random.sample(staminaDeck, number_of_wounds)

def drawConv(number_of_wounds):
    return random.sample(convictionDeck, number_of_wounds)

def drawAuth(number_of_wounds):
    return random.sample(authorityDeck, number_of_wounds)

woundTypeSwitch = {
    's': drawStam,
    'stam': drawStam,
    'stamina': drawStam,
    'phyiscal': drawStam,
    'p': drawStam,
    'c': drawConv,
    'conv': drawConv,
    'conviction': drawConv,
    'mental': drawConv,
    'm': drawConv,
    'a': drawAuth,
    'auth': drawAuth,
    'authority': drawAuth,
}

@bot.command(name='wound', help='Draw a wound card.')
async def wound(ctx, woundType : str, number_of_wounds: int):
    woundTypeLower = woundType.lower()

    if not woundTypeLower in woundTypeSwitch:
        await ctx.send(f'Invalid wound type, valid types: {" ".join(woundTypeSwitch.keys())}')
        return

    cards = woundTypeSwitch[woundType.lower()](number_of_wounds) 

    await ctx.send('\n\n'.join([getWoundString(card) for card in cards]))

def getItemString(card):
    lines = []

    name = f'**{card["Name"].upper()}**'
    value = f'{card["Value"]}'
    lines.append(' '.join([s for s in [name, value] if s]))

    flavour = card["Flavour"]
    if flavour:
        flavour = f'*{flavour}*'

    lines.append(flavour)


    conflictClass = card["Conflict Class"]
    if conflictClass:
        conflictClass = f'*{conflictClass}*'

    mainBonus = card["Bonus Main"]
    if mainBonus:
        mainBonus = f'**{mainBonus}**'

    secondaryBonus = card["Bonus Secondary"]
    if secondaryBonus:
        secondaryBonus = f'{secondaryBonus}'

    skills = card["Skills"]
    if skills:
        skills = f'*{skills}*'

    lines.append(' | '.join([s for s in [conflictClass, mainBonus, secondaryBonus, skills] if s]))


    conflictClass2 = card["Conflict Class 2"]
    if conflictClass2:
        conflictClass2 = f'*{conflictClass2}*'

    mainBonus2 = card["Bonus 2"]
    if mainBonus2:
        mainBonus2 = f'**{mainBonus2}**'

    mainBonus2Secondary = card["Bonus 2 Secondary"]
    if mainBonus2:
        mainBonus2 = f'**{mainBonus2}**'

    skills2 = card["Skills 2"]
    if skills2:
        skills2 = f'*{skills2}*'

    lines.append(' | '.join([s for s in [conflictClass2, mainBonus2, mainBonus2Secondary, skills2] if s]))


    rarity = f'{card["Rarity"].lower()}'

    uses = card["Uses"]
    if uses:
        uses = f'Uses: {uses}'

    lines.append(' '.join([s for s in [rarity, uses] if s]))

    return ('\n'.join([s for s in lines if s])).replace(knotEmojiKey,knotEmoji)

@bot.command(name='item', help='Get description of an item.')
async def item(ctx, name : str):
    matchingItems = []
    p = re.compile(name, re.IGNORECASE)

    with open('../cards/items.csv', newline='') as csvItems:
        itemsReader = csv.DictReader(csvItems, delimiter=',', quotechar='"')
        for card in itemsReader:
            if (p.search(card["Name"].lower())):
                matchingItems.append(card)

                if (len(matchingItems) >= 20):
                    await ctx.send(f"Too many matches for {name}!")
                    return

    if len(matchingItems) > 0:
        await ctx.send('\n\n'.join([getItemString(card) for card in matchingItems]))
    else:
        await ctx.send(f"Did not find {name}")

playerDeck = []
posInPlayerDeck = 0

@bot.command(name='initCombat', help='Initiate combat, feed list [name1, name2, ...].')
async def initCombat(ctx, names : str):
    global posInPlayerDeck, playerDeck
    playerDeck = names[1:-1].split(",")
    posInPlayerDeck = 0
    await ctx.send(f"Initiative deck built: {playerDeck}")
    random.shuffle(playerDeck)

@bot.command(name='next', help='Draw next card in combat deck')
async def next(ctx):
    global posInPlayerDeck, playerDeck
    await ctx.send(f"Next player {playerDeck[posInPlayerDeck]}")
    posInPlayerDeck += 1
    if (posInPlayerDeck == len(playerDeck) - 1):
        await ctx.send(f"Final player {playerDeck[posInPlayerDeck]}")
        await ctx.send(f"Last card! Shuffling...")
        posInPlayerDeck = 0
        random.shuffle(playerDeck)

bot.run(TOKEN)