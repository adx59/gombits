#!/usr/bin/env python
import asyncio
import logging
import json
import importlib

import util.api
import util.db

import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

class Gombits(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = "g!",
            description="Binds your gambit stats to roles."
        )


        self.config = json.load(open("config.json"))
        self.api = util.api.BungieAPI(self)
        self.db = util.db.DB(self)

    async def on_ready(self):
        logging.info("Ready!")

    def reload_api(self):
        importlib.reload(util.api)
        del self.api
        
        newapi = importlib.import_module("util.api")
        self.api = newapi.BungieAPI(self)

    def run(self):
        cogs = self.config["cogs"]
    
        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                logging.info(f'Failed to load cog {cog}:\n\t{e}')
            else:
                logging.info(f'Loaded cog {cog}')


        super().run(self.config['token'])
        
gombits = Gombits()
gombits.run()

