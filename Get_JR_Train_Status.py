import os
import discord
from discord import app_commands
from discord.ext import commands
import time
import math
import json
import codecs
import urllib.request
import re
from dotenv import load_dotenv

load_dotenv()
test_guild = int(os.getenv("GuildID"))

class senku_status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=discord.Object(test_guild))
    
    @discord.app_commands.command(name = "gaiyou", description = "列車運行情報取得")
    @discord.app_commands.guilds(test_guild)
    @discord.app_commands.describe(text="today or tomorrow ", text2="個人表示 true or false")
    @discord.app_commands.rename(text="日付", text2="個人表示")
    @discord.app_commands.choices(text=[
        app_commands.Choice(name="today", value="today"),
        app_commands.Choice(name="tomorrow", value="tomorrow")
        ])
    
    async def gaiyou(self, ctx: discord.Interaction, text: str = "today", text2: bool = True):
        
        query = str(math.floor(time.time()))
        gaiyou_url = "https://www3.jrhokkaido.co.jp/webunkou/data/senku/senku_03.json?" + query
        gaiyou_response = urllib.request.urlopen(gaiyou_url)
        gaiyou_jsondata = json.load(codecs.getreader('utf-8-sig')(gaiyou_response))

        status_code = gaiyou_jsondata[text]["senkuStatus"]["hakochise"]
        print(status_code)
        if (status_code != 0):
            top = "**列車運行情報 概況　札幌近郊　函館・千歳線**\n" + ":warning: 遅延が発生しています！"
            gaikyo_detail = gaiyou_jsondata[text]["gaikyo"]
            gaikyo_length = len(gaikyo_detail)
            gaikyo_title = ""
            gaikyo_honbun = ""
            for i in range(gaikyo_length):
                gaikyo_title = gaikyo_title + gaikyo_detail[i]["title"] + "\n"
                gaikyo_honbun = gaikyo_honbun + gaikyo_detail[i]["honbun"] + "\n\n"
                gaikyo_honbun = re.sub(r'<BR><BR><a href=.*?</a>', '', gaikyo_honbun, flags=re.DOTALL)
                gaikyo_honbun = re.sub(r'<BR>', '\n', gaikyo_honbun, flags=re.DOTALL)
                
            unkyu_train = ""

            unkyu_length = len(gaiyou_jsondata[text]["unkyuTrains"])
            for j in range(unkyu_length):
                jokyo = gaiyou_jsondata[text]["unkyuTrains"][j]["jokyo"]
                haEki = gaiyou_jsondata[text]["unkyuTrains"][j]["haEki"]
                haTime = gaiyou_jsondata[text]["unkyuTrains"][j]["haTime"]
                toEki = gaiyou_jsondata[text]["unkyuTrains"][j]["toEki"]
                toTime = gaiyou_jsondata[text]["unkyuTrains"][j]["toTime"]
                class_name = gaiyou_jsondata[text]["unkyuTrains"][j]["name"]
                unkyu_train += jokyo +"　"+ haEki + "(" + haTime + ") ⇒ " + toEki + " (" + toTime + ")　" + class_name + "\n"

            chien_length = len(gaiyou_jsondata[text]["chienTrains"])
            for k in range(chien_length):
                jokyo = gaiyou_jsondata[text]["chienTrains"][j]["jokyo"]
                haEki = gaiyou_jsondata[text]["chienTrains"][j]["haEki"]
                haTime = gaiyou_jsondata[text]["chienTrains"][j]["haTime"]
                toEki = gaiyou_jsondata[text]["chienTrains"][j]["toEki"]
                toTime = gaiyou_jsondata[text]["chienTrains"][j]["toTime"]
                class_name = gaiyou_jsondata[text]["chienTrains"][j]["name"]
                unkyu_train += jokyo +"　" + haEki + "(" + haTime + ") ⇒ " + toEki + " (" + toTime + ")　" + class_name + "\n"

            gaikyo_honbun += unkyu_train
            embed = discord.Embed(title=gaikyo_title, description=gaikyo_honbun, color=11194195)
            await ctx.response.send_message(top, embed=embed, ephemeral=text2)
        else:
            status_honbun = gaiyou_jsondata[text]["gaikyo"][0]["honbun"]
            top = "**列車運行情報 概況　札幌近郊　函館・千歳線**\n" + ":o: 通常運行"

            embed = discord.Embed(title=status_honbun, 
                                  color=11194195)
            await ctx.response.send_message(top, embed=embed, ephemeral=text2)

async def setup(bot):
    await bot.add_cog(senku_status(bot))