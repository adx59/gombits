#!/usr/bin/env python
import logging

from discord.ext import commands
import discord

class Gambit:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        await ctx.send(
            ("Hello! Welcome to registration. Please input your platform type.\n"
            "`1` :: `XBOX`\n"
            "`2` :: `PSN`\n"
            "`4` :: `Battle.Net (PC)`\n"
            "And yes, that's a `4` for Battle.Net.")
        )

        def platform_check(m):
            try:
                if not (int(m.content) in [1, 2, 4]):
                    return False
            except Exception as e:
                logging.warn(str(e))
                return False
            else:
                return m.author.id == ctx.author.id

        platform = await self.bot.wait_for("message", check = platform_check)

        await ctx.send(":white_check_mark: Good job, you managed to input a number lmao. What's your username?")
        username = await self.bot.wait_for("message")

        p_info = await self.bot.api.e_player_info(username.content, platform.content)
        
        if not p_info:
            await ctx.send((
                "**Here's the good news:** you managed to input your username and platform! (yay!)\n"
                "**Here's the bad news:** I couldn't find that player. You're probably retarded."
            ))
            return
        
        db_res = ctx.bot.db.new_user(
            ctx.author,
            username.content,
            p_info["userInfo"]["membershipId"],
            platform.content,
            p_info["characterIds"]
        )

        await ctx.send(f":white_check_mark: **Registered!**\n```{p_info}```\n```{db_res}```")


def setup(bot):
    bot.add_cog(Gambit(bot))