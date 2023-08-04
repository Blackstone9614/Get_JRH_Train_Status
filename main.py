import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
test_guild = int(os.getenv("GuildID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# cogを登録する処理
@bot.event
async def on_ready():
    print("botを起動します")
    await bot.load_extension('Get_JR_Train_Status')
    await bot.load_extension('Get_ST_Train_Status')
    await bot.load_extension('Get_JR_Train_Info_A')
    await bot.load_extension('Get_JR_Train_Info_G')
    await bot.load_extension('Get_JR_Train_Info_H')
    await bot.load_extension('Get_JR_Train_Info_S')
    await bot.tree.sync(guild=discord.Object(test_guild))

bot.run(TOKEN)