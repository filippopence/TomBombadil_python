import discord
from discord.ext import commands, tasks
import random 
import json
from unidecode import unidecode
import os
from dotenv import load_dotenv, find_dotenv
import datetime
import time

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())
with open("Cards.json", "r", encoding="utf8") as f:
    data = json.load(f)
    data_official = []
    CardList = []
    CardListName = []
    PlayerCards = []
    for n in range(len(data)):
        if data[n]['is_official'] == True:
            data_official.append(data[n])
            CardListName.append(unidecode(data[n]['name']).upper())
            CardList.append(data[n])
            if data[n]['type_name'] in ['Ally', 'Hero', 'Attachment', 'Event']:
                PlayerCards.append(data[n])

# @client.command()
# async def ge(ctx):
#     print(ctx.guild.emojis)
#     await ctx.send(f"<:spirit:1081702484784992289>")

# GUESS UNOFFICIAL
@client.command(aliases=['guess+'])
async def guessall(ctx, max:int=len(data)):
    i = random.randint(1,max)
    while data[i]['type_name'] != 'Hero' and data[i]['type_name'] != 'Ally':
            i = random.randint(1,max)
    traits = data[i]['traits'].split(".")
    traits = list(map(lambda x : unidecode(x.strip()).upper(), traits))
    name = data[i]['name']
    print(i, name)
    embed = discord.Embed(title = "What's the card?", description = "Guess the card name typing `is <query>`", color= discord.Color.yellow(), timestamp = ctx.message.created_at)
    if data[i]['type_name'] == 'Hero':
        embed.add_field(name = "Threat", value = data[i]['threat'])
    else:
        embed.add_field(name = "Cost", value = data[i]['cost'])
    embed.add_field(name= "Type", value = data[i]['type_name'])
    embed.add_field(name = "Unique", value = data[i]['is_unique'])
    embed.add_field(name = "<:willpower:1079780338122899537>", value = data[i]['willpower'])
    embed.add_field(name = "<:attack:1079780316337672343>", value = data[i]['attack'])
    embed.add_field(name = "<:defense:1079780291138289725>", value = data[i]['defense'])
    embed.add_field(name = "<:hitpoints:1082806330508722266>", value = data[i]['health'])
    embed.add_field(name = "Traits", value = data[i]['traits'])
    if data[i]['sphere_code'] == 'spirit':
        card_sphere = '<:spirit:1079729428638208032>'
    elif data[i]['sphere_code'] == 'lore':
        card_sphere = '<:lore:1079729387458547752>'
    elif data[i]['sphere_code'] == 'leadership':
        card_sphere = '<:leadership:1079729503334572032>'
    elif data[i]['sphere_code'] == 'tactics':
        card_sphere = '<:tactics:1079729464398856252>'
    elif data[i]['sphere_code'] == 'baggins':
        card_sphere = '<:baggins:1079729273004363786>'
    elif data[i]['sphere_code'] == 'fellowship':
        card_sphere = '<:fellowship:1079729539342675988>'
    elif data[i]['sphere_code'] == 'neutral':
        card_sphere = 'Neutral'
    embed.add_field(name = "Sphere", value = card_sphere)
    dict = {"<b>": "**",  # define desired replacements here
            "</b>": "**", 
            "<i>": "_", 
            "</i>": "_", 
            data[i]['name']: "This Card", 
            "[": "<:", 
            "attack]": "attack:1079780316337672343>",
            "defense]": "defense:1079780291138289725>",
            "willpower]": "willpower:1079780338122899537>",
            "threat]": "threat:1079780360403034112>",
            "lore]": "lore:1079729387458547752>",
            "leadership]": "leadership:1079729503334572032>",
            "spirit]": "spirit:1079729428638208032>",
            "tactics]": "tactics:1079729464398856252>",
            "fellowship]": "fellowship:1079729539342675988>",
            "baggins]": "baggins:1079729273004363786>"
            } 
    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text
    embed.add_field(name = "Text", value = replace_all(data[i]['text'], dict))
    embed.add_field(name = "Flavor", value = data[i]['flavor'])
    embed.add_field(name = "Set", value = data[i]['pack_name'])
    await ctx.send(embed=embed)
    await ctx.send(f"I'm thinking of a card...\nTry to guess which one!")
    tries = 0
    def check(m):
        return m.channel == ctx.message.channel #m.author == ctx.author and 
    for j in range(10000):
        guess = await client.wait_for('message', check=check)
        if guess.content.startswith('is'):
            message_text = guess.content.split(" ")
            message_text.pop(0)
            card_name = []
            for i in message_text:
                card_name.append(i)
            mySeparator = " "
            card = mySeparator.join(card_name)
            if unidecode(card).upper() == unidecode(name).upper():
                await ctx.send("You guessed correctly!")
                break
            else:
                await ctx.send(f"Nope.\n{4-tries} attempts left.")
                if tries == 4:
                    await ctx.send("Game lost, try again tomorrow!")
                    break
                tries += 1
        else:
            await ctx.send("You have to type `is` followed by the name of the card!")

# GUESS OFFICIAL
@client.command(aliases=['guess1'])
async def guess(ctx, max:int=len(data_official)):
    i = random.randint(1,max)
    while data_official[i]['type_name'] != 'Hero' and data_official[i]['type_name'] != 'Ally':
            i = random.randint(1,max)
    traits = data_official[i]['traits'].split(".")
    traits = list(map(lambda x : unidecode(x.strip()).upper(), traits))
    name = data_official[i]['name']
    print(i, name)
    embed = discord.Embed(title = "What's the card?", description = "Guess the card name typing `is <query>`", color= discord.Color.yellow(), timestamp = ctx.message.created_at)
    if data_official[i]['type_name'] == 'Hero':
        embed.add_field(name = "Threat", value = data_official[i]['threat'])
    else:
        embed.add_field(name = "Cost", value = data_official[i]['cost'])
    embed.add_field(name= "Type", value = data_official[i]['type_name'])
    embed.add_field(name = "Unique", value = data_official[i]['is_unique'])
    embed.add_field(name = "<:willpower:1079780338122899537>", value = data_official[i]['willpower'])
    embed.add_field(name = "<:attack:1079780316337672343>", value = data_official[i]['attack'])
    embed.add_field(name = "<:defense:1079780291138289725>", value = data_official[i]['defense'])
    embed.add_field(name = "<:hitpoints:1082806330508722266>", value = data_official[i]['health'])
    embed.add_field(name = "Traits", value = data_official[i]['traits'])
    if data_official[i]['sphere_code'] == 'spirit':
        card_sphere = '<:spirit:1079729428638208032>'
    elif data_official[i]['sphere_code'] == 'lore':
        card_sphere = '<:lore:1079729387458547752>'
    elif data_official[i]['sphere_code'] == 'leadership':
        card_sphere = '<:leadership:1079729503334572032>'
    elif data_official[i]['sphere_code'] == 'tactics':
        card_sphere = '<:tactics:1079729464398856252>'
    elif data_official[i]['sphere_code'] == 'baggins':
        card_sphere = '<:baggins:1079729273004363786>'
    elif data_official[i]['sphere_code'] == 'fellowship':
        card_sphere = '<:fellowship:1079729539342675988>'
    elif data_official[i]['sphere_code'] == 'neutral':
        card_sphere = 'Neutral'
    embed.add_field(name = "Sphere", value = card_sphere)
    dict = {"<b>": "**",  # define desired replacements here
            "</b>": "**", 
            "<i>": "_", 
            "</i>": "_", 
            data_official[i]['name']: "This Card", 
            "[": "<:", 
            "attack]": "attack:1079780316337672343>",
            "defense]": "defense:1079780291138289725>",
            "willpower]": "willpower:1079780338122899537>",
            "threat]": "threat:1079780360403034112>",
            "lore]": "lore:1079729387458547752>",
            "leadership]": "leadership:1079729503334572032>",
            "spirit]": "spirit:1079729428638208032>",
            "tactics]": "tactics:1079729464398856252>",
            "fellowship]": "fellowship:1079729539342675988>",
            "baggins]": "baggins:1079729273004363786>"
            } 
    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text
    embed.add_field(name = "Text", value = replace_all(data_official[i]['text'], dict))
    embed.add_field(name = "Flavor", value = data_official[i]['flavor'])
    embed.add_field(name = "Set", value = data_official[i]['pack_name'])
    await ctx.send(embed=embed)
    await ctx.send(f"I'm thinking of a card...\nTry to guess which one!")
    tries = 0
    def check(m):
        return m.channel == ctx.message.channel #m.author == ctx.author and 
    for j in range(10000):
        guess = await client.wait_for('message', check=check)
        if guess.content.startswith('is'):
            message_text = guess.content.split(" ")
            message_text.pop(0)
            card_name = []
            for i in message_text:
                card_name.append(i)
            mySeparator = " "
            card = mySeparator.join(card_name)
            if unidecode(card).upper() == unidecode(name).upper():
                await ctx.send("You guessed correctly!")
                break
            else:
                await ctx.send(f"Nope.\n{4-tries} attempts left.")
                if tries == 4:
                    await ctx.send("Game lost, try again tomorrow!")
                    break
                tries += 1
        else:
            await ctx.send("You have to type `is` followed by the name of the card!")
    

# SEARCH CARD
@client.command()
async def hobimg(ctx, card=None):
    message = ctx.message.content.split(' ')
    message.pop(0)
    cc = message
    message = " ".join(message)
    card = unidecode(message).upper()
    print(f"Looking for: {card}")
    def search(card_list, string):
        index_list = []
        for n in range(len(card_list)):
            if card_list[n].find(string) != -1:
                index_list.append(n)
        return index_list
    CardIndexes = search(CardListName, card)
    if len(CardIndexes) == len(CardList):
        await ctx.send('I am sorry, but I need at least a name to find a card')
    elif len(CardIndexes) == 1:
        await ctx.send(CardList[CardIndexes[0]]['imagesrc'])
    elif len(CardIndexes) == 0:
        await ctx.send(f"No cards found matching '{cc}'.")
    else:
        dict = {"<b>": "**",  # define desired replacements here
            "</b>": "**", 
            "<i>": "_", 
            "</i>": "_", 
            "lore": "<:lore:1079729387458547752>",
            "leadership": "<:leadership:1079729503334572032>",
            "spirit": "<:spirit:1079729428638208032>",
            "tactics": "<:tactics:1079729464398856252>",
            "fellowship": "<:fellowship:1079729539342675988>",
            "baggins": "<:baggins:1079729273004363786>",
            "none": " ",
            "neutral": " "
            } 
        def replace_all(text, dic):
            for i, j in dic.items():
                text = text.replace(i, j)
            return text
        cards_found = []
        if len(CardIndexes) > 20:
            max = 20
            await ctx.send(f"I've found {len(CardIndexes)} cards (Sending 20). Reply with the number of the one you want")
        else:
            max = len(CardIndexes)
            await ctx.send(f"I've found {len(CardIndexes)} cards. Reply with the number of the one you want")
        for ids in range(max):
            sphere = replace_all(CardList[CardIndexes[int(ids)]]['sphere_code'], dict)
            cards_found.append((f"{ids+1}. {sphere} **{CardList[CardIndexes[int(ids)]]['name']}**\n_{CardList[CardIndexes[int(ids)]]['type_name']}_ ({CardList[CardIndexes[int(ids)]]['pack_name']})"))
        await ctx.send('\n'.join(cards_found))
        def check(m):
            return m.channel == ctx.message.channel #m.author == ctx.author and 
        for j in range(1):
            id = await client.wait_for('message', check=check)
            id = id.content
            try:
                await ctx.send(CardList[CardIndexes[int(id)-1]]['imagesrc'])
            except:
                await ctx.send("You have to type the number of the card you want!")


# CARD OF THE DAY
WHEN = datetime.time(10, 0, 0)  # set time here in UTC - 10:00 AM
CHANNEL_ID = 1080119360422682746 # Put your channel id here

@tasks.loop(time=WHEN) 
async def send_message():
    channel = client.get_channel(CHANNEL_ID)
    i = random.randint(1,len(PlayerCards))
    await channel.send("**Card of the day!**")
    card = await channel.send(PlayerCards[i]['imagesrc'])
    emojis = ["\u0031\ufe0f\u20e3", '\u0032\ufe0f\u20e3', '\u0033\ufe0f\u20e3', '\u0034\ufe0f\u20e3', '\u0035\ufe0f\u20e3']
    time.sleep(0.5)
    for emoji in emojis:
        await card.add_reaction(emoji)

@client.event
async def on_ready():
    send_message.start()

# .day command
@client.command()
async def day(ctx):
    channel = client.get_channel(CHANNEL_ID)
    i = random.randint(1,len(PlayerCards))
    await channel.send("**Card of the day!**")
    card = await channel.send(PlayerCards[i]['imagesrc'])
    emojis = ["\u0031\ufe0f\u20e3", '\u0032\ufe0f\u20e3', '\u0033\ufe0f\u20e3', '\u0034\ufe0f\u20e3', '\u0035\ufe0f\u20e3']
    time.sleep(0.5)
    for emoji in emojis:
        await card.add_reaction(emoji)



load_dotenv(find_dotenv())
client.run(os.getenv('TOKEN'))










