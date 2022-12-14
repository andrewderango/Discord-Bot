import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
import random
import time

client = commands.Bot(command_prefix = '-')

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game("I am currently active"))
  await client.get_channel('xxxxxxxxxxxxxx').send("I am now active.")

blackjackPlaying = True
if blackjackPlaying == True:
  @client.event
  async def on_message(message):
    embeds = message.embeds # return list of embeds
    for embed in embeds:
      #print(embed.to_dict()) # it's content of embed in dict
      blackjackEmbed = embed.to_dict()
      if 'blackjack game' in blackjackEmbed['author']['name'] and blackjackEmbed.get('description') == None:
        cpuCard = blackjackEmbed['fields'][1]['value'][14:16]
        if cpuCard[1] == '`':
          cpuCard = cpuCard[0]
        if cpuCard == 'K' or cpuCard == 'Q' or cpuCard == 'J':
          cpuCard = 10
        if cpuCard == 'A':
          cpuCard = 1
        cpuCard = int(cpuCard)
        # await message.channel.send('CPU card value is ' + str(cpuCard))
        userSum = blackjackEmbed['fields'][0]['value'][-3:-1:]
        if userSum[0] == '`':
          userSum = int(userSum[1])
        # await message.channel.send('User total value is ' + str(userSum))



        cards = [1,1,2,3,4,5,6,7,8,9,10,10,10,10]
        cpuPossibilities = []
        userSumPerm = userSum
        winningPossibilities = 0
        tyingPossibilities = 0
        losingPossibilities = 0

        for a in range(len(cards)):
          hypotheticalCPUsum = 0
          hypotheticalCPUsum = cpuCard + cards[a]
          if hypotheticalCPUsum >= 17:
            for h in range(len(cards)**3):
              cpuPossibilities.append(hypotheticalCPUsum)
          else:
            for c in range(len(cards)):
              hypotheticalCPUsum = int(cpuCard) + cards[a]
              hypotheticalCPUsum += cards[c]
              if hypotheticalCPUsum >= 17:
                for g in range(len(cards)**2):
                  cpuPossibilities.append(hypotheticalCPUsum)
              else:
                for d in range(len(cards)):
                  hypotheticalCPUsum = int(cpuCard) + cards[a] + cards[c]
                  hypotheticalCPUsum += cards[d]
                  if hypotheticalCPUsum >= 17:
                    for f in range(len(cards)):
                      cpuPossibilities.append(hypotheticalCPUsum)
                  else:
                    for e in range(len(cards)):
                      hypotheticalCPUsum = int(cpuCard) + cards[a] + cards[c] + cards[d]
                      hypotheticalCPUsum += cards[e]
                      if hypotheticalCPUsum <= 21:
                        cpuPossibilities.append(21)
                      else:
                        cpuPossibilities.append(22)
                  
        for b in range(len(cpuPossibilities)):
          if cpuPossibilities[b] < int(userSum) or cpuPossibilities[b] > 21:
            winningPossibilities += 1
          elif cpuPossibilities[b] == userSum:
            tyingPossibilities += 1
          else:
            losingPossibilities += 1

        #print('\nOdds of winning if fold: ' + str(round(winningPossibilities/len(cpuPossibilities)*100,2)) + '%')
        #print('Odds of tying if fold: ' + str(round(tyingPossibilities/len(cpuPossibilities)*100,2)) + '%')
        #print('Odds of losing if fold: ' + str(round(losingPossibilities/len(cpuPossibilities)*100,2)) + '%')

        userWins = 0
        cpuWins = 0
        gamesPlayed = 0

        for simulationNumber in range(100000):
          userSum = int(userSumPerm) + int(random.choice(cards))
          #for a in range(3):
          #  if userSum < 17:
          #    userSum += random.choice(cards)
          #  if a == 4 and userSum < 21:
          #    userSum = 21
          cpuSum = cpuCard + random.choice(cards)
          for a in range(3):
            if cpuSum < 17:
              cpuSum += random.choice(cards)
            if a == 4 and cpuSum < 21:
              cpuSum = 21
          if userSum == 21:
            userWins += 1
          elif userSum > 21:
            cpuWins += 1
          elif userSum > cpuSum:
            userWins += 1
          elif cpuSum > 21:
            userWins += 1
          gamesPlayed += 1

        #print('\nOdds of winning if hit: ' + str(round(userWins/gamesPlayed*100,2)) + '%')
        #print('Odds of losing if hit: ' + str(round(cpuWins/gamesPlayed*100,2)) + '%')

        if cpuWins/gamesPlayed*100 < losingPossibilities/len(cpuPossibilities)*100:
          bjoFooter = 'You should probably __**HIT (H)**__'
          bjoColor = 0x00FF00
        else:
          bjoFooter = 'You should probably __**STAND (S)**__'
          bjoColor = 0xFF0000


        embed=discord.Embed(title="Probabilities of Losing", url="https://www.seekpng.com/png/full/819-8194226_blackjack-instant-game-logo-graphic-design.png", description='**Stand**: ' + str(round(losingPossibilities/len(cpuPossibilities)*100,2)) + '%\n**Hit**: ' + str(round(cpuWins/gamesPlayed*100,2)) + '%\n\n' + bjoFooter, color=bjoColor)
        embed.set_author(name=blackjackEmbed['author']['name'], url="https://www.seekpng.com/png/full/819-8194226_blackjack-instant-game-logo-graphic-design.png", icon_url=blackjackEmbed['author']['icon_url'])
        embed.set_thumbnail(url='https://www.seekpng.com/png/full/819-8194226_blackjack-instant-game-logo-graphic-design.png')
        await message.channel.send(embed=embed)



@client.command(aliases=['Ping'])
async def ping(ctx):
  await ctx.send(f'Client ping is {round(client.latency * 1000, 1)} ms')

@client.command(aliases=['Clear','Clean','clean','del','Del','delete','Delete'])
async def clear(ctx, quantity = 1):
  await ctx.channel.purge(limit = int(quantity) + 1)
  await ctx.send('Deleted ' + str(quantity) + ' messages.')
  time.sleep(2)
  await ctx.channel.purge(limit = 1)

@client.command(aliases=['RNG','Rng','randomnumber','Randomnumber','Randomnumbergenerator','randomnumbergenerator','randint','Randint'])
async def rng(ctx, lowerBound, upperBound):
  rngNum = random.randint(int(lowerBound),int(upperBound))
  embed=discord.Embed(title="Random number is " + str(rngNum), description="Random number generated between " + str(lowerBound) + " and " + str(upperBound) + " for " + str(ctx.author.mention), color=0xFFFF00)
  embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
  await ctx.send(embed = embed)

@rng.error
async def rng_error(ctx, error):
  await ctx.send('Please provide a lower limit and an upper limit separated by spaces.\n\n**Ex:** -rng 1 10')

@client.command(aliases=['Chooseone','Pickone','pickone','choose','pick'])
async def chooseone(ctx, opt1, opt2):
  chooseone_options = []
  chooseone_options.append(str(opt1))
  chooseone_options.append(str(opt2))
  chooseone_chosenOption = random.choice(chooseone_options)
  embed=discord.Embed(title=str(chooseone_chosenOption), description="Random selection between " + str(opt1) + " and " + str(opt2) + ", requested by " + str(ctx.author.mention), color=0x00FF00)
  await ctx.send(embed = embed)

@chooseone.error
async def chooseone_error(ctx, error):
  await ctx.send('Please provide 2 options separated by a space. Each option must not contain a space.\n\n**Ex:** -chooseone Team1 Team2')

@client.command(aliases = ['Coinflip','HeadsOrTails','Headsortails','headsortails','flipcoin','CoinFlip','FlipCoin','Flipcoin'])
async def coinflip(ctx):
  coinflip_chosenSide = random.choice(['Heads','Tails'])
  embed=discord.Embed(title=str(coinflip_chosenSide), description="Result of a heads or tails coin flip requested by " + str(ctx.author.mention), color=0x00FF00)
  await ctx.send(embed = embed)

@client.command(aliases=['Kick'])
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  member = str(member)
  embed=discord.Embed(title=str(member[:-5]) + " has been kicked from the server", description=str(ctx.author.mention) + " has kicked " + str(member[:-5]) + " from the server.", color=0xFF0000)
  embed.add_field(name="Reason", value=str(reason), inline=False)
  await ctx.send(embed=embed)

@client.command(aliases=['Ban'])
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)
  member = str(member)
  embed=discord.Embed(title=str(member[:-5]) + " has been banned from the server", description=str(ctx.author.mention) + " has banned " + str(member[:-5]) + " from the server.", color=0xFF0000)
  embed.add_field(name="Reason", value=str(reason), inline=False)
  await ctx.send(embed=embed)
  
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run('xxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxx)
