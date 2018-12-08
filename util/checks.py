#!/usr/bin/env python
from discord.ext import commands

def is_dev():
    def predicate(ctx: commands.Context):
        if ctx.author.id in ctx.bot.config["dev"]:
            return True
        return False
    return commands.check(predicate)

def manage_guild():
    def predicate(ctx: commands.Context):
        if ctx.author.permissions.guild_permissions.manage_guild:
            return True
        return False
    return commands.check(predicate)