import discord
from discord.ext import commands

class Bonk(commands.Cog):
    def __init__(self, bot, mod_channel, stan_channel):
        self.bot = bot
        self.mod_channel = mod_channel
        self.stan_channel = stan_channel

    def 