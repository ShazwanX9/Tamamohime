import os
import json
import datetime
from itertools import cycle
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks

##################################################################################################################################

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

##################################################################################################################################

def get_prefix(bot, message):
    with open("assets/prefixes.json", 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

##################################################################################################################################

description = "The-weird... I feel like I've missed you but that doesn't the-make sense."
personality = """You.. You... You... How dare you call me the-stinky again!
               That is the last the-straw! I am the-fragrant!
               Roses line up just to get the-one whiff of me!
               What really the-stinks is your whole stupid existence!"""
status = cycle(["but I'm Sleepy...", " for you", " takes forever"])

bot = commands.Bot  (
                    command_prefix = get_prefix, 
                    description = description, 
                    help_command = None
                    )

##################################################################################################################################

@bot.event
async def on_ready():
    status_update.start()
    print (f"{os.getenv("bot_name")} is online")

@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send(f"Ayy, Something wrong here... Please refer \"{get_prefix(bot, ctx)}help\" for more info!")

@bot.event
async def on_guild_join(guild):
    with open("assets/prefixes.json", 'r') as f:
        prefixes = json.load(f)

    #default Prefix
    prefixes[str(guild.id)] = "hey " 

    with open("assets/prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent = 4)
    
@bot.event
async def on_guild_left(guild):
    with open("assets/prefixes.json", 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("assets/prefixes.json", 'w') as f:
        json.dump(prefixes, f, indent = 4)

# @clear.errors
# async def command_error(ctx, err):
    # if isinstance(err, commands.MissingPermission):
        # await ctx.send("Sorry, You don't seem to have enough power to do that")

##################################################################################################################################

# change status loop
@tasks.loop(seconds = 15)
async def status_update():
    await bot.change_presence ( 
        status = discord.Status.idle, 
        activity = discord.Activity ( 
            type = discord.ActivityType.watching, 
            name = next(status)
        ) 
     )

##################################################################################################################################


# @bot.command(aliases = ["play", "yt"])
@bot.command()
async def test(ctx):
    await ctx.send("Testing")


##################################################################################################################################

# Install all cog at startup
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

##################################################################################################################################

if __name__ == "__main__" :
    # Get the API token from the .env file.
    load_dotenv()
    bot.run(os.getenv("discord_token"))