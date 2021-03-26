import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # On ready event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Events cog has been loaded.")
    
    # Error Handling Event
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Check if the argument is missing
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please type the subreddit after >post command.")
        
        # Check if command is not found
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply("Command not found.")

        # Check if there is no subreddit with that name/invalid argument
        if isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Subreddit is unavailable/invalid argument.")

def setup(bot):
    bot.add_cog(Events(bot))