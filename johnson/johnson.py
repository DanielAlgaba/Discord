import os
import random
import glob
import json
from datetime import date

import discord
import requests

from johnson_quotes import quotes


client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


# All the possible command for the bot
@client.event
async def on_message(message):

    # The bot will ignore his own messages
    if message.author == client.user:
        return

    # List of available commands for the user
    if message.content.startswith(".help"):
        await message.channel.send(
            (
                "**These are the avialable commands**:\n"
                "- **.image**:\t\t    Johnson sends"
                " a ramdom Halo Infinite art image.\n"
                "- **.sir**:\t\t\t\t   Johnson sends a random quote.\n"
                "- **.born**:\t\t\t   days left for Johnson to be born.\n"
                "- **.infinite**:\t\t   days left for Halo Infinite release.\n"
                "- **.camaign**:\t\t followed by a Gamertag"
                " to see its campaign stats.\n"
                "- **.multiplayer**:\tfollowed by a Gamertag "
                "to see its multiplayer stats\n"
                "- **.avatar**:\t\t\t followed by a Gamertag to see "
                "its emblem, avatar, clan and service tag\n"
            )
        )

    # The bot sends a random image from a local folder
    if message.content.startswith(".image"):
        images = glob.glob(
            ("/workspaces/discord_bots/johnson" "/ArtOfHaloInfiniteHD/*.jpg")
        )
        random_image = random.choice(images)
        await message.channel.send(
            "**There you go, Marine!**",
            file=discord.File(random_image),
        )

    # The bot sends a message with a random quote
    if message.content.startswith(".sir"):
        await message.channel.send(f"**{random.choice(quotes)}**")

    # The bot sends a message with the days left for
    # the character Avery J. Johnson to be born in Halo lore
    if message.content.startswith(".born"):
        d = date(2552, 12, 11)
        delta = d - date.today()
        await message.channel.send(
            f"There are **{delta.days}** days left for me to be born!"
        )

    # The bot send a message with the days left
    # for the release of Halo Infinite
    if message.content.startswith(".infinite"):
        d = date(2021, 12, 8)
        today = date.today()
        if today < d:
            delta = d - today
            await message.channel.send(
                (
                    f"There are **{delta.days}** days"
                    f" left for"
                    f" Halo Infinite launch!"
                )
            )
        else:
            await message.channel.send(
                (
                    "Halo Infinite is out! What are you waiting for Marine?!"
                    " **Go play right now!**"
                )
            )

    # The bot sends a message with the Master Chief Collection Campaign
    # stats of the gamertag selected
    if message.content.startswith(".campaign"):
        try:
            player = message.content.split("campaign")[1].lstrip()
            access_token = os.environ["HALOAPI_TOKEN"]
            url = (
                f"https://cryptum.halodotapi.com/games/hmcc/"
                f"stats/players/{player}/service-record"
            )
            headers = {
                "Content-Type": "application/json",
                "Cryptum-API-Version": "2.3-alpha",
                "Authorization": f"Cryptum-Token {access_token}",
            }
            response = requests.request("GET", url, headers=headers)
            stats = json.loads(response.text)
            player = stats["additional"]["gamertag"]
            missions = stats["data"]["campaign"]["missions"]["completed"]
            missions_kills = stats["data"]["campaign"]["missions"]["kills"]
            missions_deaths = stats["data"]["campaign"]["missions"]["deaths"]
            playlists = stats["data"]["campaign"]["playlists"]["completed"]
            playlists_kills = stats["data"]["campaign"]["playlists"]["kills"]
            playlists_deaths = stats["data"]["campaign"]["playlists"]["deaths"]

            await message.channel.send(
                (
                    f"**{player}** has completed"
                    f" **{missions}** missions, has killed "
                    f"**{missions_kills}** enemies and has died "
                    f"**{missions_deaths}** times in campaign."
                )
            )
            await message.channel.send(
                (
                    f"**{player}** has completed **{playlists}** playlists, "
                    f"has killed **{playlists_kills}** enemies and "
                    f"has died **{playlists_deaths}** times in playlists."
                )
            )
        except KeyError:
            await message.channel.send(
                (
                    "`An error has occurred! You have not written any Gamertag"
                    " or the one you have entered does not exit!`"
                )
            )

    # The bot sends a message with the Master Chief Collection multiplayer
    # stats of the gamertag selected
    if message.content.startswith(".multiplayer"):
        try:
            player = message.content.split("multiplayer")[1].lstrip()
            access_token = os.environ["HALOAPI_TOKEN"]
            url = (
                f"https://cryptum.halodotapi.com/games/hmcc/"
                f"stats/players/{player}/service-record"
            )
            headers = {
                "Content-Type": "application/json",
                "Cryptum-API-Version": "2.3-alpha",
                "Authorization": f"Cryptum-Token {access_token}",
            }
            response = requests.request("GET", url, headers=headers)
            stats = json.loads(response.text)
            player = stats["additional"]["gamertag"]
            matches = stats["data"]["multiplayer"]["total_matches"]
            kd_ratio = stats["data"]["multiplayer"]["kdr"]
            kills = stats["data"]["multiplayer"]["summary"]["kills"]
            deaths = stats["data"]["multiplayer"]["summary"]["deaths"]
            assists = stats["data"]["multiplayer"]["summary"]["assists"]
            wins = stats["data"]["multiplayer"]["summary"]["wins"]
            loses = stats["data"]["multiplayer"]["summary"]["losses"]
            if loses > 0:
                wl_ratio = wins / loses
            else:
                wl_ratio = wins
            rank_pl = stats["data"]["multiplayer"]["ranked"]["highest_rank"]["playlist"]
            rank_level = stats["data"]["multiplayer"]["ranked"]["highest_rank"]["rank"]

            await message.channel.send(
                (
                    f"**{player}** has a k/d of"
                    f" **{str(round(kd_ratio, 2))}** "
                    f"with **{kills}** kills, **{deaths}** deaths and "
                    f"**{assists}** assists."
                )
            )
            await message.channel.send(
                (
                    f"**{player}** has a win/lose ratio "
                    f"of **{str(round(wl_ratio, 2))}** "
                    f"in **{matches}** matches. "
                    f"**{player}** has won **{wins}** matches and"
                    f" has lost **{loses}** matches."
                )
            )
            await message.channel.send(
                (f"**{player}** max rank " f"was **{rank_level}** in **{rank_pl}**.")
            )
        except KeyError:
            await message.channel.send(
                (
                    "`An error has occurred! You have not written any Gamertag"
                    " or the one you have entered does not exit!`"
                )
            )

    # The bot sends a message with the Master Chief Collection emblem,
    # clan tag and avatar of the gamertag selected
    if message.content.startswith(".avatar"):
        try:
            player = message.content.split("avatar")[1].lstrip()
            access_token = os.environ["HALOAPI_TOKEN"]
            url = (
                f"https://cryptum.halodotapi.com/games/hmcc/"
                f"appearance/players/{player}"
            )
            headers = {
                "Content-Type": "application/json",
                "Cryptum-API-Version": "2.3-alpha",
                "Authorization": f"Cryptum-Token {access_token}",
            }
            response = requests.request("GET", url, headers=headers)
            stats = json.loads(response.text)
            player = stats["additional"]["gamertag"]
            clan = stats["data"]["clan_tag"]
            emblem = stats["data"]["emblem_url"]
            avatar = stats["data"]["avatar_url"]
            tag = stats["data"]["service_tag"]

            await message.channel.send(emblem)
            await message.channel.send((f"[**{clan}**] " f"{player}" f" *" f"*{tag}**"))
            await message.channel.send(avatar)
        except KeyError:
            await message.channel.send(
                (
                    "`An error has occurred! You have not written any Gamertag"
                    " or the one you have entered does not exit!`"
                )
            )


client.run(os.environ["DISCORD_TOKEN"])
