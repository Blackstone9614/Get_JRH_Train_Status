import time
import math
import json
import codecs
import urllib.request

def GetTrainStatus(station_code, in_out, direction, display_number_max, rapid):

  global status
  global description

  query = str(math.floor(time.time()))
  url = "https://www3.jrhokkaido.co.jp/monitor/unkou_info/json/services" + station_code + ".json?_=" + query
  response = urllib.request.urlopen(url)
  status_jsondata = json.load(codecs.getreader('utf-8-sig')(response))
  status_data = status_jsondata["services"][station_code][in_out][direction]
  number = len(status_data)

  list = ["class", "name", "time", "to", "status", "now", "add", "dest"]
  status = ":o: 通常運行" + "\n"
  description = ""

  display_number = 0
  delay = 0

  for i in range(number):

    if (status_data[i][list[0]] != status_data[i][list[1]]):
      train_name_tmp = status_data[i][list[0]] + status_data[i][list[1]]
    else:
      train_name_tmp = status_data[i][list[0]]

    if (rapid == True or (status_data[i][list[0]] != "快速" and status_data[i][list[0]] != "特急")):
      if (display_number < display_number_max):

        if (status_data[i][list[4]] == 1):
          status_icon = ":warning: "
        elif (status_data[i][list[4]] == 2):
          status_icon = ":warning: "
        elif (status_data[i][list[4]] == 3):
          status_icon = ":x: "
        elif (status_data[i][list[4]] == 0 or status_data[i][list[4]] == 5 or status_data[i][list[4]] == 6):
          status_icon = ":o: "

        description += status_data[i][list[2]] + "　" + status_data[i][list[
          3]] + " 行" + "　" + train_name_tmp + "\n" + status_icon + status_data[
            i][list[5]] + status_data[i][list[6]] + status_data[i][
              list[7]] + "\n"

        if ((status_data[i][list[4]] != 0 and status_data[i][list[4]] != 5
             and status_data[i][list[4]] != 6) and delay == 0):
          delay = 1
          status = ":warning: 遅れが発生しています！！！" + "\n"
        elif (status_data[i][list[4]] == 3 or status_data[i][list[4]] == 2):
          status = ":x: 運休が発生してます！！！" + "\n"
        elif (number == 0):
          status = ":x: 電車がありません！" + "\n"

        display_number = display_number + 1
    i = i + 1

  print(status)
  print(description)

  return status, description