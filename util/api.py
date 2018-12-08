#!/usr/bin/env python
import asyncio
import aiohttp
import requests
from discord.ext import commands

class BungieAPI(object):
    """A class reprsenting the Bungie/Destiny 2 API"""
    GAMBIT_PROGRESS_HASH = "2772425241"
    def __init__(self, bot):
        self.bot = bot
        
        self.apibase = "https://www.bungie.net/Platform"
        self.apikey = self.bot.config["apikey"]

    async def _dispatch(self, endpoint, method, headers, params):
        """Dispatches a request asynchronously.

        Internal method."""
        res = None
        async with aiohttp.ClientSession() as session:
            res = await session.request(
                url = f"{self.apibase}{endpoint}",
                method = method,
                headers = headers,
                params = params
            )
            
            await session.close()

        if res.status < 200 or res.status >= 400:
            raise commands.errors.CommandError(f"Web Request Failed: {res.status}")

        response_json = await res.json()
        if not response_json:
            return await res.text()

        return response_json

    async def _dispatch_sync(self, endpoint, method, headers, params):
        """Dispatches a request synchronously.
        
        Internal method."""
        res = requests.request(
            method,
            f"{self.apibase}{endpoint}",
            headers = headers,
            params = params
        )

        res_json = res.json()
        if not res_json:
            return res.text()

        return res_json

    async def search_user(self, username, member_type):
        """kk"""
        formatted_username = username.replace("#", "%23")
        res = await self._dispatch(
            f"/Destiny2/SearchDestinyPlayer/{member_type}/{formatted_username}",
            "GET",
            {
                "X-API-Key": self.apikey
            },
            {}
        )

        if not res["Response"]:
            return False

        return res["Response"][0]

    async def player_info(self, member_id, member_type):
        res = await self._dispatch(
            f"/Destiny2/{member_type}/Profile/{member_id}/",
            "GET",
            {
                "X-API-Key": self.apikey
            },
            {
                "components": "100"
            }
        )

        if not res["Response"]:
            return False

        return res["Response"]["profile"]["data"]

    async def e_player_info(self, username, member_type):
        user_info = await self.search_user(username, member_type)
        
        player_id = user_info["membershipId"]
        player_info = await self.player_info(player_id, member_type)

        return player_info


    async def gambit_infamy(self, member_id, member_type, character_id):
        res = await self._dispatch_sync(
            f"/Destiny2/{member_type}/Profile/{member_id}/",
            "GET",
            {
                "X-API-Key": self.apikey
            },
            {
                "components": "202"
            }
        )

        if not res["Response"]:
            return False

        infamy = res["Response"]["characterProgressions"]["data"][f"{character_id}"]\
                    ["progressions"][self.GAMBIT_PROGRESS_HASH]

        return {
            "infamy": infamy["currentProgress"],
            "weekly": infamy["weeklyProgress"],
            "daily": infamy["dailyProgress"]
        }
