#!/usr/bin/env python
import pymongo
import discord

class DB(object):
    """Class to interface with mongo DB."""
    HOST = "adam-likes-it.xyz"
    PORT = 27017

    def __init__(self, bot):
        self.bot = bot

        self.mongo = pymongo.MongoClient(
            host = self.HOST,
            port = self.PORT, 
            username = bot.config["mongo"]["username"],
            password = bot.config["mongo"]["password"]
        )
        self.db = self.mongo.gombits

    def new_user(self, user: discord.User, username: str, player_id: str, platform: int, characters: list):
        users = self.db.users

        user_data = {
            "_id": user.id,
            "username": username,
            "player_id": player_id,
            "platform": platform,
            "characters": characters
        }
        
        return users.insert_one(user_data).inserted_id


    