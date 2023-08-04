import os
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv

load_dotenv()
test_guild = int(os.getenv("GuildID"))

class st_status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=discord.Object(test_guild))
    
    @discord.app_commands.command(name = "st", description = "地下鉄運行情報")
    @discord.app_commands.guilds(test_guild)
    @discord.app_commands.describe(text="個人表示 true or false")
    @discord.app_commands.rename(text="個人表示")
    
    # 運行情報を取得する処理
    async def gaiyou(self, ctx: discord.Interaction, text: bool = True):
        
        content = ""
        rosen_status_hyouji = 0

        # 地下鉄３路線全てを取得
        for j in range(3):
            url = "https://transit.yahoo.co.jp/diainfo/" + str( j + 13 ) + "/0"
            res = requests.get(url)

            soup =  BeautifulSoup(res.content,'html.parser')
            rosen_name = "**" + soup.find('h1',class_='title').text + "**"
            rosen_name = re.sub(r'札幌市営', '', rosen_name, flags=re.DOTALL)
            rosen_status = soup.find('dt').text
            rosen_gaikyo = soup.find('dd').text
            
            if (rosen_status != "平常運転"):
                rosen_status_code = ":warning:"
                rosen_status_hyouji = 1
            else:
                rosen_status_code = ":o:"
            
            content += rosen_name + "：" + rosen_status_code + "\n" + rosen_gaikyo + "\n"
            j = j + 1
            
        if(rosen_status_hyouji == 0):
            rosen_status_hyouji = ":o: 通常運行"
        else:
            rosen_status_hyouji = ":warning: 遅れがあります"
            
        title = "**札幌市営地下鉄　運行情報**\n" +  rosen_status_hyouji
        embed = discord.Embed(title=rosen_status_hyouji, description=content)
        await ctx.response.send_message(content=title, embed=embed, ephemeral=text)

async def setup(bot):
    await bot.add_cog(st_status(bot))