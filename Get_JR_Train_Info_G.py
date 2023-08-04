import os
import discord
from discord.ext import commands
import csv
import Get_JR_Train_Info_all
from dotenv import load_dotenv

load_dotenv()
test_guild = int(os.getenv("GuildID"))

with open('station_list.csv', 'r', encoding='utf-8') as codelist:
  reader = csv.DictReader(codelist)
  codelist = [row for row in reader]

class JR_Train_Info_G(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.tree.sync(guild=discord.Object(test_guild))

  @discord.app_commands.command(name = "g", description = "学園都市線　列車運行情報")
  @discord.app_commands.guilds(test_guild)
  @discord.app_commands.rename(text="駅番号", text2="方面", text3="表示本数", x="快速表示", y="個人表示")
  @discord.app_commands.describe(text="駅番号",
                                 text2="s…札幌方面 t…当別方面 到着は末尾にa",
                                 text3="表示本数（通常：５）",
                                 x="快速表示 true or false",
                                 y="個人表示 true or false")
  @discord.app_commands.choices(text2=[
    discord.app_commands.Choice(name="s", value="s"),
    discord.app_commands.Choice(name="sa", value="sa"),
    discord.app_commands.Choice(name="t", value="t"),
    discord.app_commands.Choice(name="ta", value="ta")
  ])

  async def g(self, ctx: discord.Interaction, text: int, text2: str, text3: int=5, x: bool = False, y: bool = True):
      
    gyou = ""
    retu = ""
    command_name = ""

    for i in range(15):
      if (int(codelist[i+46]["駅番号"]) == int(text)):
        gyou = text + 45

        if(text2 == "t"):
          retu = "小樽方面発車"
          in_out = "departures"
          setumei = "当別 方面 発車時刻"
        elif(text2 == "s"):
          in_out = "departures"
          retu = "札幌方面発車"
          setumei = "札幌 方面 発車時刻"
        elif (text2 == "ta"):
          retu = "小樽方面到着"
          in_out = "arrivals"
          setumei = "当別 方面 到着時刻"
        elif (text2 == "sa"):
          retu = "札幌方面到着"
          in_out = "arrivals"
          setumei = "札幌 方面 到着時刻"
        break
      else:
        i += 1

    if (gyou == "" or retu == ""):
      await ctx.response.send_message("そのコマンドは存在しません", ephemeral=y)
      return 1
        
    command_code = codelist[gyou]["コマンド"]
    command_name = codelist[gyou]["コマンド"] + text2
    station_code = codelist[gyou]["駅コード"]
    station_name = codelist[gyou]["駅名"]
    direction = codelist[gyou][retu]
    rapid = x
    display_number_max = text3
    explanation = "【" + command_code + " " + station_name + "】" + setumei
    print(codelist[gyou][retu])

    if (command_name == ""):
      await ctx.response.send_message("そのコマンドは存在しません", ephemeral=y)
      return 1
    elif (direction == "0"):
      await ctx.response.send_message("そのコマンドは使用できません", ephemeral=y)
      return 1
    else:
      print(command_name)
        
    status, description = Get_JR_Train_Info_all.GetTrainStatus(station_code, in_out, direction, display_number_max, rapid)

    print("コマンドを送信します")

    embed = discord.Embed(title=status, description=description, color=11194195)
    await ctx.response.defer(thinking=True, ephemeral=y)
    await ctx.followup.send(explanation, embed=embed, ephemeral=y)

async def setup(bot):
  await bot.add_cog(JR_Train_Info_G(bot))