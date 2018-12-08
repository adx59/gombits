#!/usr/bin/env python
import sys
import os
import subprocess
import asyncio
import logging
import importlib as il

from discord.ext import commands
import discord

from util.checks import is_dev

class Dev:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['evaluate'])
    @is_dev()
    async def debug(self, ctx, *, code: str):
        """Executes some code."""
        try:
            env = {}
            to_exec = 'async def func(ctx):\n'
            for line in code.splitlines():
                to_exec += f'  {line}\n'

            exec(to_exec, env)

            func = env['func']
            res = await func(ctx)
        except Exception as e:
            await ctx.send(f':warning: Error: ```{str(e)}```')
            return
        else:
            if res is None:
                await ctx.message.add_reaction('✅')
            else:
                await ctx.send(f':white_check_mark: Executed successfully. ```{res}```')

    @commands.command(aliases=["re"])
    async def reload(self, ctx, *, cog):
        try:
            ctx.bot.unload_extension(cog)
            ctx.bot.load_extension(cog)
        except Exception as e:
            logging.exception(e)
            await ctx.send(f":warning: `{e}`")
        else:
            await ctx.send(f":white_check_mark: Reloaded `{cog}`!")
                

    @commands.command(aliases=['reboot'])
    @is_dev()
    async def restart(self, ctx):
        """Restarts the bot.

        Developer only command."""
        await ctx.send(':arrows_counterclockwise: Rebooting!')
        os.execl(sys.executable, sys.executable, * sys.argv)


def setup(bot):
    bot.add_cog(Dev(bot))