import discord
import random
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands, tasks
from itertools import cycle


import logging


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


client = commands.Bot(command_prefix='.')
status = cycle(['Android Studio', 'Visual Studio code'])


@client.event
async def on_ready():
    change_status.start()
    print("Bot is ready!")


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['Q', 'q'])
async def _q(ctx, *, question):
    responses = ['It is certain',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes definitely.',
                 'No man you rock',
                 'Not a clue',
                 'You are worhless',
                 'No you!',
                 'You may rely on it.']
    await ctx.send(f'{random.choice(responses)}')


@client.command()
async def text(ctx, *, message):
    await ctx.send(message)


@client.command()
@commands.has_permissions(manage_messages=True)
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await user.send(message)


@client.command()
async def say(ctx, *, text=''):
    if text == '':
        await ctx.send("You need to say something")
    else:
        await ctx.send(text)
        await ctx.message.delete()


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=2):
    await ctx.channel.purge(limit=amount+1)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = " no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(f'User {member.mention} has been kicked for {reason}')


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = "No need of reason"
    await ctx.guild.ban(member)
    await ctx.send(f'User {member.mention} has been banned for {reason}')


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"{user} have been unbanned sucessfully")

client.run('token')
