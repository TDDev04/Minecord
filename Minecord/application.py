import os, sys, time, json, discord
import asyncio
import datetime
from pyngrok import ngrok
from discord import user
from discord import message
from discord import role
from discord.enums import ContentFilter
from discord.ext import commands
from discord.ext.commands import context, has_permissions, CheckFailure
from discord.guild import Guild

# client info
usrid = 1
token = "discord-usr-token"
ngrok.set_auth_token("auth-token")

# set the prefix
intents = discord.Intents().all()
client = commands.Bot(command_prefix="r", help_command=None, intents=intents)

#vars
now = datetime.datetime.now()
addr = 25565
protocol = "tcp"
state = "eu"

# events
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game('rstart to begin!'))
    print("user name is:", client.user.name)
    print("discord ID:", client.user.id)

# commands
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Member {member.mention} has been kicked.")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason, delete_message_days=0)
    await ctx.send(f'Member {member.mention} got vanished')

@client.command()
async def echo(ctx, *, content:str):
    print(f"Usage of echo!")
    await ctx.channel.purge(limit=1)
    await ctx.send(content)

@client.command()
async def eval(self, ctx, *, code):
    if ctx.author.id == usrid: pass
    else: await eval(code)
        
@eval.error
async def eval_error(self, ctx, error):
    Error = discord.Embed(
        description = f"**An exception has occured:**\n`​``py\n{error}\n`​``",
        colour = discord.Colour.red()
    )
    await ctx.send(embed=Error)
    raise(error)

@client.command()
async def ngrokrun(ctx):
    link = ngrok.connect(addr, protocol, state)
    # throw the ip to join the server (in this case, minecraft)
    await ctx.send(f"Connected: {link.public_url[link.public_url.rfind('://')+3:len(link.public_url)]}")

@client.command()
async def ngrokquit(ctx):
    tunnels = ngrok.get_tunnels()
    for tunnel in tunnels:
        ngrok.disconnect(tunnel.public_url)
        ngrok.kill()
        await ctx.send("Disconnected!")

client.run(token)