import os
import json
import datetime
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

BOT_NAME = os.getenv("bot_name")

async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    "How could you the-forget?!"

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *input):
        # Shows all modules

        with open("assets/prefixes.json", 'r') as f:
            prefix = json.load(f)[str(ctx.guild.id)]
        version =  os.getenv("bot_version")

        # owner      = 	# ENTER YOU DISCORD-ID
        # owner_name = 	# ENTER YOUR USERNAME#1234

        if not input:

            # starting to build embed
            emb = discord.Embed (
                                title = "Commands and Modules", 
                                # color=discord.Color.magenta(),
                                # color = discord.Color.from_rgb( random.randrange(255), random.randrange(255), random.randrange(255)),
                                color = discord.Color.random(),
                                description = f'Use `{prefix}help <module>` to gain more information about that module '
                                )

            # iterating through cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            # adding 'list' of cogs to embed
            emb.add_field(name = "Modules", value = cogs_desc, inline = False)

            # integrating trough uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # adding those commands to embed
            if commands_desc:
                emb.add_field(name = "For Everyone Usage", value = commands_desc, inline = False)

            # setting information about author
            emb.add_field(name = "About", value = f"{BOT_NAME} can't explain how the-great it is to see you.")
            emb.set_footer(text = f"It is so {BOT_NAME} still {version}")

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emb = discord.Embed (
                                        title = f'{cog} - Commands', description= self.bot.cogs[cog].__doc__,
                                        # color = discord.Color.from_rgb( random.randrange(255), random.randrange(255), random.randrange(255))
                                        color = discord.Color.random()
                                        )

                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(name = f"`{prefix}{command.name}`", value = command.help, inline=False)
                    # found cog - breaking loop
                    break

            # if input not found
            else:
                emb = discord.Embed (
                                    title = "What's that?!",
                                    description = f"{BOT_NAME} never knew that module called `{input[0]}` exist! :scream:",
                                    color = discord.Color.orange()
                                    )

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed (
                                title = "That's too much.",
                                description = "{BOT_NAME} didnt Get It! What do you want? :thinking:",
                                color = discord.Color.red()
                                )

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)

def setup(bot):
    bot.add_cog(Help(bot))