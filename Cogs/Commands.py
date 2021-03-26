import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import praw
import random
from pathlib import Path

load_dotenv()
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

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # On ready event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands cog has been loaded.")

    # Command for posting a submission from reddit
    # Subreddit name as the argument
    @commands.command(aliases=['p', 'psot', 'pos', 'pot', 'ptos'])
    async def post(self, ctx, subredd):
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

def setup(bot):
    bot.add_cog(Commands(bot))