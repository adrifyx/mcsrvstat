import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import io
import base64

load_dotenv()

bot = commands.Bot(command_prefix="mc!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} command(s).")
    except Exception as e:
        print(e)
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="MC Servers"), status=discord.Status.idle)

    print(f"Bot logged in as {bot.user}")

@bot.hybrid_command(name="check")
async def check(ctx, ip: str):
    """Checks the status of a Minecraft Server provided."""
    r = requests.get(f"https://api.mcsrvstat.us/3/{ip}")
    json_data = r.json()
    address = json_data["hostname"]
    motd = str(json_data["motd"]["clean"][0]) + "\n" + str(json_data["motd"]["clean"][1])
    online = json_data["online"]
    playerCount =  str(json_data["players"]["online"]) + '/' + str(json_data["players"]["max"])
    embed = discord.Embed(title=f"{address}", color=0x2b2d31)
    embed.add_field(name="__MOTD:__", value=f"{motd}", inline=False)
    embed.add_field(name="__Online:__", value=f"{online}", inline=True)
    embed.add_field(name="__Players:__", value=f"{playerCount}", inline=True)
    icon = json_data["icon"]
    *_, icon = icon.partition(',')
    decoded_icon = io.BytesIO(base64.b64decode(icon + '=='))
    file = discord.File(decoded_icon, filename="icon.png")
    embed.set_thumbnail(url="attachment://icon.png")
    await ctx.send(file=file, embed=embed)

bot.run(os.getenv("TOKEN"))
