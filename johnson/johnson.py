import os
import discord
import random
import glob
from johnson_quotes import quotes
from datetime import date

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(".image"):
        images = glob.glob("/workspaces/discord_bots/johnson/ArtOfHaloInfiniteHD/*.jpg")
        random_image = random.choice(images)
        await message.channel.send(
            "There you go, Marine!",
            file=discord.File(random_image),
        )

    if message.content.startswith(".sir"):
        await message.channel.send(random.choice(quotes))
    if message.content.startswith(".born"):
        d = date(2552, 12, 11)
        delta = d - date.today()
        await message.channel.send(
            f"There are {delta.days} days left for me to be born!"
        )


client.run(os.environ["DISCORD_TOKEN"])
