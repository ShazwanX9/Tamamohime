import os
import json
import datetime
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

def is_owner():
    async def predicate(ctx):
        return str(ctx.author.id) == str(os.getenv("discord_id"))
    return commands.check(predicate)

class Admin(commands.Cog):
    " You...don't think you could the-maybe elaborate?"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ping", help = "Check current latency")
    async def ping(self, ctx):
        await ctx.send(f"{self.bot.latency * 1000:.2f}ms")

    @is_owner()
    @commands.command(name = "clear", help = "clear a bunch of code")
    async def clear(self, ctx, amount : int):
        if amount:
            await ctx.channel.purge(limit = amount+1)

    @is_owner()
    @commands.command(name = "changePrefix", help = "Change current prefix to new one")
    async def changePrefix(self, ctx, prefix):
        with open("assets/prefixes.json", 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("assets/prefixes.json", 'w') as f:
            json.dump(prefixes, f, indent = 4)

        await ctx.send(f"Aight! I'll remember [ {prefix} ] now!")     

    @commands.command(name = "info", help = "Details of the server")
    async def info(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", description="Owner is so cool!", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
        embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
        embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
        embed.set_thumbnail(url="https://i.redd.it/qdz0y217z3x31.png")

        await ctx.send(embed=embed)

    @is_owner()
    @commands.command(name = "load", help = "Install a module")
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Aight! Extension [ {extension} ] added!")

    @is_owner()
    @commands.command(name = "unload", help = f"Uninstall a module")
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Aight! Extension [ {extension} ] removed!")

def setup(bot):
    bot.add_cog(Admin(bot))