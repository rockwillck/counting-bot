# bot.py
import os
import random
import dotenv

import discord
from discord.utils import find, get
from discord.ext import tasks

import dbPy

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

dbPy.initiate()

@client.event
async def on_message(message):
    admin = message.author.guild_permissions.administrator

    emojis = ["🐶", "🐱", "🐭", "🐹", "🐷", "🍌", "🍓", "🤖", "🌂", "🧢", "🐒", "🐬", "🕸", "🌏", "🍎", "🥑", "🧊", "🛸"]
    random.shuffle(emojis)

    messageC = message.content

    if messageC == ";help":
        embedVar = discord.Embed(title="CountingBot Help", color=discord.Color.orange())
        embedVar.add_field(name="Rules", value="""CountingBot is a very simple counting game bot.
You play with the following rules:
- Count in succession
- You can't count more than once
- You can only count in one channel""")
        embedVar.add_field(name="Setup", value="Use `;start` in whatever channel you want to count in. Then, just start counting!")
        embedVar.set_image(url="https://cdn.discordapp.com/attachments/858062576667328601/858069351268876288/Screen_Shot_2021-06-25_at_2.41.00_PM.png")
        embedVar.set_footer(text="Copyright 2021 rockwill")
        await message.channel.send(embed=embedVar)
    elif messageC == ";start":
        if admin:
            dbPy.storeDBValue(f"channel-{message.guild.id}", message.channel.id)
            await message.channel.send("✅ Done!")
        else:
            await message.channel.send("❌ You're not an admin...")
    else:
        try:
            number = int(messageC)
        except:
            return

        try:
            channel = get(message.guild.channels, id=int(dbPy.getDBValue(f"channel-{message.guild.id}")))
        except:
            return
        
        if message.channel == channel:
            pass
        else:
            return

        try:
            lastNumber = int(dbPy.getDBList(f"last-{message.guild.id}")[0])
            lastUser = int(dbPy.getDBList(f"last-{message.guild.id}")[1])
        except:
            if number == 1:
                await message.add_reaction("✅")
                dbPy.storeDBList(f"last-{message.guild.id}", [1, message.author.id])
                return
            else:
                await message.add_reaction("❌")
                await message.channel.send("❌ Wrong number. Next number is `1`.")
                dbPy.storeDBList(f"last-{message.guild.id}", [0, "COUNTINGLOSER"])
                return

        if number == lastNumber + 1:
            if int(lastUser) != message.author.id:
                await message.add_reaction("✅")
                dbPy.storeDBList(f"last-{message.guild.id}", [number, message.author.id])
                return
            else:
                await message.add_reaction("❌")
                await message.channel.send("❌ You can't count twice in a row. Next number is `1`.")
                dbPy.storeDBList(f"last-{message.guild.id}", [0,"COUNTINGLOSER"])
                return
        else:
            await message.add_reaction("❌")
            await message.channel.send("❌ Wrong number. Next number is `1`.")
            dbPy.storeDBList(f"last-{message.guild.id}", [0,"COUNTINGLOSER"])
            return
            

client.run(TOKEN)