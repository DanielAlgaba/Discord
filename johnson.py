import discord
import random

client = discord.Client()
quotes = [
    "You heard the lady! Move like you've got a purpose!",
    "All you greenhorns who wanted to see Covenant up close... this is your lucky day.",
    "It's a mess, sir. We're scattered all over this valley. We called for evac, but until you showed up, I thought we were cooked.",
    "Hit it, Marines—go, go, go! The Corps ain't payin' us by the hour!",
    "Don't even THINK about it, Marine!",
    "Goddamnit Jenkins, fire your weapon!",
]


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content

    if message.content.startswith(".sir"):
        await message.channel.send(random.choice(quotes))


client.run("ODkyNTIwNTk0MTI0NDcyMzIx.YVOGkw.1zFM9BrJDzONP0wooQ7zLGhWnqc")
