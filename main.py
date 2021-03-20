import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import praw
import random
from discord.ext.commands import Bot
import asyncio

# Load sensitive data from .env file
# Create .env file in the same folder and insert your data
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
c_id = os.getenv('CLIENT_ID')
c_secret = os.getenv('CLIENT_SECRET')
uname = os.getenv('REDDIT_USERNAME')
pswd = os.getenv('REDDIT_PASSWORD')
agent = os.getenv('USER_AGENT')

reddit = praw.Reddit(client_id = c_id,
                    client_secret = c_secret,
                    username = uname,
                    password = pswd,
                    user_agent = agent,
                    check_for_async=False)

bot = commands.Bot(command_prefix='>')
bot.remove_command('help') # Removing default help command

# Event for checking if the bot is online
@bot.event
async def on_ready():
    print(f'{bot.user} is now live on:')
    for guild in bot.guilds:
        print(f"-{guild.name} ({guild.id})")

# Command for posting a submission from reddit
# Subreddit name as the argument
@bot.command(aliases=['p', 'psot', 'pos', 'pot', 'ptos'])
async def post(ctx, subredd):
    subreddit = reddit.subreddit(subredd)
    all_subs = []

    hot = subreddit.hot()

    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    title = random_sub.title
    url = random_sub.url
    op = random_sub.author
    sub_id = random_sub.id
    name = random_sub.subreddit

    # NSFW channel filter conditioning
    # Check if the channel is NSWF then post
    if ctx.channel.is_nsfw():
        await ctx.reply(f"{title}\nr/{name}\nby u/{op} (http://redd.it/{sub_id})\n{url}")
    # Check if the channel is not a NSFW channel then check if the subreddit is NSFW
    # The post will not show up if the subreddit is NSFW
    else:
        if subreddit.over18:
            await ctx.reply("BONK! Go to horny jail")
        else:
            await ctx.reply(f"{title}\nr/{name}\nby u/{op} (http://redd.it/{sub_id})\n{url}")

# Command for sending bee movie script
# Sending text from bee.txt
@bot.command()
async def bee(ctx):
    with open('bee.txt', 'r') as f:
        for line in f:
            await ctx.send(line)

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
    em.set_footer(text='Made by Hann#6130')

    await ctx.send(embed=em)

# Error Handling Event
@bot.event
async def on_command_error(ctx, error):
    # Check if the argument is missing
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Please type the subreddit after >post command.")
    
    # Check if command is not found
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Command not found.")

    # Check if there is no subreddit with that name/invalid argument
    if isinstance(error, commands.CommandInvokeError):
        await ctx.reply("Subreddit is unavailable/invalid argument.")

# Function for changing presence
async def changePresence():
    await bot.wait_until_ready()

    statuses = ["your mom | >help", f"on {len(bot.guilds)} servers | >help", "Made by Hann#6130 | >help"]

    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=discord.Game(name=status))

        await asyncio.sleep(10)

bot.loop.create_task(changePresence())
bot.run(TOKEN)