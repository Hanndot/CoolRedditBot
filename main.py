import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
import praw
import random
from discord.ext.commands import Bot
import asyncio

cwd = Path(__file__).parents[0]
cwd = str(cwd)

# Load sensitive data from .env file
# Create .env file in the same folder and insert your data
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='>')
bot.remove_command('help') # Removing default help command

# Event for checking if the bot is online
@bot.event
async def on_ready():
    print(f'{bot.user} is now live on:')
    for guild in bot.guilds:
        print(f"-{guild.name} ({guild.id})")

# Command for sending bee movie script
# Sending text from bee.txt
@bot.command()
async def bee(ctx):
    with open('bee.txt', 'r') as f:
        for line in f:
            await ctx.send(line)

# Command for generating bot invite link
@bot.command(aliases=['i', 'link'])
async def invite(ctx):
    link = 'https://discord.com/api/oauth2/authorize?client_id=816638346193010700&permissions=8&scope=bot'
    em = discord.Embed(
        title = "CoolRedditBot Invite Link",
        type = "rich",
        color = 0xFF5700
    )
    em.add_field(name='Here you go :)', value=link)

    await ctx.send(embed=em)

# Command for sending all available commands
@bot.command(aliases=['h', 'hlep', 'tolong'])
async def help(ctx):
    em = discord.Embed(
        title = "How to use CoolRedditBot",
        type = "rich",
        description = "List of available commands",
        color = 0xFF5700
    )
    em.add_field(name='>post <subreddit>', value='Get a submission from reddit', inline='false')
    em.add_field(name='>bee', value='Annoy everyone', inline='false')
    em.add_field(name='>help', value='Get list of available commands', inline='false')
    em.add_field(name='>invite', value='Generate invite link', inline='false')
    em.set_footer(text='Made by Hann#6130')

    await ctx.send(embed=em)

# Function for changing presence
async def changePresence():
    await bot.wait_until_ready()

    statuses = ["with your mom | >help", f"on {len(bot.guilds)} servers | >help", "Made by Hann#6130 | >help"]

    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=discord.Game(name=status))

        await asyncio.sleep(10)

if __name__ == '__main__':
    # Loading all cogs
    for file in os.listdir(cwd+"/Cogs"):
        if file.endswith(".py"):
            bot.load_extension(f"Cogs.{file[:-3]}")
    # Running the bot
    bot.loop.create_task(changePresence())
    bot.run(TOKEN)
