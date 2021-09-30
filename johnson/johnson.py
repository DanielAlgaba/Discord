import discord
import random
import glob
from johnson_quotes import quotes

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(".image"):
        images = glob.glob(".\ArtOfHaloInfiniteHD\*.jpg")
        random_image = random.choice(images)
        await message.channel.send(
            "There you go, Marine!", file=discord.File(random_image),
        )

    if message.content.startswith(".sir"):
        await message.channel.send(random.choice(quotes))


client.run("ODkyNTIwNTk0MTI0NDcyMzIx.YVOGkw.1zFM9BrJDzONP0wooQ7zLGhWnqc")
