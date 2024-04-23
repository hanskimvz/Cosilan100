# Copyright (c) 2022, Hans kim

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os, time, sys
import pymysql
from functions_s import (configVars, dbconMaster, log, TZ_OFFSET)

MYSQL = { 
    "commonParam": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.param'),
    "commonSnapshot": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.snapshot'),
    "commonCount": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.counting'),
    "commonHeatmap": configVars('software.mysql.db') +"." + configVars('software.mysql.db_common.table.heatmap'),
    "commonCountEvent": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.count_event'),
    "commonFace": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.face'),
    "customCount": configVars('software.mysql.db_custom.table.count'),
    "customHeatmap": configVars('software.mysql.db_custom.table.heatmap'),
    "customAgeGender": configVars('software.mysql.db_custom.table.age_gender'),
    "customSquare": configVars('software.mysql.db_custom.table.square'),
    "customStore": configVars('software.mysql.db_custom.table.store'),
    "customCamera": configVars('software.mysql.db_custom.table.camera'),
    "customCounterLabel": configVars('software.mysql.db_custom.table.counter_label'),
    "customRtCount": "realtime_counting",
}
MYSQL['customCount'] = 'count_tenmin_p'

def getCountData(db_name='cnt_demo', places=[], label=[], view_by='hourly', date_from='2019-01-01', date_to='', format='json', option=""):
  dbCon = dbconMaster()
  
  sfilter = list()
  if places:
    if not isinstance(places, list):
      places = [places]
    for place in places:
      if place.startswith("SQ"):
        sfilter.append("square_code='" + place + "'")
      elif place.startswith("ST"):
        sfilter.append("store_code='" + place + "'")
      elif place.startswith("C"):
        sfilter.append("camera_code='" + place + "'")

  group = ""
  if view_by == 'hourly':
    group = "year, month, day, hour, counter_label"
    interval = 3600
    date_format = "%Y-%m-%d %H:%M"

  elif view_by == 'daily':
    group = "year, month, day, counter_label"
    interval = 3600*24
    date_format = "%Y-%m-%d"
  elif view_by == 'monthly':
    group = "year, month, counter_label"
    interval = 3600*24*31
    date_format = "%Y-%m"
  elif view_by == 'yearly':
    group = "year, counter_label"
    interval = 3600*24*365
    date_format = "%Y"
  elif view_by == 'tenmin':
    group = "year, month, day, hour, min, counter_label"
    interval = 600
    date_format = "%Y-%m-%d %H:%M"


  if not date_to:
    date_to = date_from
  
  ts_s = time.mktime(time.strptime(date_from, "%Y-%m-%d"))
  ts_e = time.mktime(time.strptime(date_to,   "%Y-%m-%d"))
  
  arr_rs = {
    'series': [],
    'xaxis':{
      'type': "datetime", 
      'categories':[]
    }
  }

  arr_data = dict()
  for ts in range (int(ts_s), int(ts_e), interval):
    tss = time.gmtime(ts)
    datetime_tag = time.strftime(date_format, tss)
    arr_rs['xaxis']['categories'].append(datetime_tag)
    arr_data[datetime_tag] = dict()

  print (arr_rs)
  

  time_bt = " year >= %d and year <=%d and timestamp >=%d and timestamp <%d" %(int(date_from.split("-")[0]), int(date_from.split("-")[0]),ts_s, ts_e)

  sq = "select timestamp, year, month, day, hour, min, wday, counter_label as label, sum(counter_val) as value from " + db_name + "." + MYSQL['customCount'] + " where "
  if sfilter:
    sq +=  "(" + " or ".join(sfilter) + ")"

  if time_bt:
    sq += " and (" + time_bt +")"

  if group:
    sq += " group by " + group
  
  print (sq)

  
  with dbCon:
    cur = dbCon.cursor(pymysql.cursors.DictCursor)
    cur.execute(sq)
    rows = cur.fetchall()
    
    for row in rows:
      ts = (row['timestamp'] // interval) * interval
      tss = time.gmtime(ts)
      datetime_tag = time.strftime(date_format, tss)
      arr_data[datetime_tag][row['label']]= row['value']
      # for ts in range (tst, int(ts_e), interval):
      #   tss = time.gmtime(ts)
      #   datetime_tag = time.strftime(date_format, tss)
      #   arr_rs['xaxis']['categories'].append(datetime_tag)
      #   print(datetime_tag)
      #   tst += interval

      #   if datetime_tag == datetime_tag_row:
      #     if not datetime_tag in arr:
      #       arr[datetime_tag] = []
      #     arr[datetime_tag].append(row)
      #     # tst += interval
      #     break
        # tst += interval

      # for ts in range (int(ts_s), int(ts_e), interval):
      #   tss = time.gmtime(ts)
      #   datetime_tag = time.strftime(date_format, tss)
      #   arr_rs['xaxis']['categories'].append(datetime_tag)
      
      # for j in range(0, 100):
      #   row = rows[i+j]
      #   # print(row)
      #   if ts == row['timestamp']:
      #     print (datetime_tag, end="  ")
      #     ts = (row['timestamp'] // interval) * interval
      #     tss = time.gmtime(ts)
      #     datetime_tag = time.strftime(date_format, tss)
      #     print (datetime_tag, end= " ")
      #     print (row)
      #     break
      # i= i+j+1
        

      # ts = (row['timestamp'] // interval) * interval
      # tss = time.gmtime(ts)
      # datetime_tag = time.strftime(date_format, tss)
      # 

      # if not datetime_tag in arr:
      #   arr[datetime_tag] = []


      # arr[datetime_tag].append(row)

  print (arr_data)
  # print (arr_rs)
  
  
# cwd = os.getcwd()
  # response = {
  #   "series": [
  #     {
  #       "name": "12weeks",
  #       "data": [17318, 17533, 17011, 14286, 16300, 14629, 15242, 15303, 14481, 13325, 13201, 10547, 10932, 10742, 10182, 10906, 11091, 11639, 12111, 12796, 15229, 15593, 15707, 15118, 15651, 17159, 16572, 15224, 16816, 16655, 16288, 15774, 17089, 15928, 16205, 16125, 12199, 12779, 17427, 19313, 16492, 15135, 16891, 17236, 18272, 17782, 18858, 17643, 17626, 17551, 17663, 18580, 18538, 18906, 18080, 18427, 18297, 18320, 18707, 18576, 18660, 18368, 17126, 17754, 18000, 19165, 18128, 15556, 14425, 16549, 17326, 17455, 18078, 18287, 19064, 18414, 18270, 18319, 18484, 18521, 17802, 17433, 15871, 15358]
  #     }
  #   ],
  #   "xaxis":{
  #     "type":"datetime",
  #     "categories": ["2024-01-29","2024-01-30","2024-01-31","2024-02-01","2024-02-02","2024-02-03","2024-02-04","2024-02-05","2024-02-06","2024-02-07","2024-02-08","2024-02-09","2024-02-10","2024-02-11","2024-02-12","2024-02-13","2024-02-14","2024-02-15","2024-02-16","2024-02-17","2024-02-18","2024-02-19","2024-02-20","2024-02-21","2024-02-22","2024-02-23","2024-02-24","2024-02-25","2024-02-26","2024-02-27","2024-02-28","2024-02-29","2024-03-01","2024-03-02","2024-03-03","2024-03-04","2024-03-05","2024-03-06","2024-03-07","2024-03-08","2024-03-09","2024-03-10","2024-03-11","2024-03-12","2024-03-13","2024-03-14","2024-03-15","2024-03-16","2024-03-17","2024-03-18","2024-03-19","2024-03-20","2024-03-21","2024-03-22","2024-03-23","2024-03-24","2024-03-25","2024-03-26","2024-03-27","2024-03-28","2024-03-29","2024-03-30","2024-03-31","2024-04-01","2024-04-02","2024-04-03","2024-04-04","2024-04-05","2024-04-06","2024-04-07","2024-04-08","2024-04-09","2024-04-10","2024-04-11","2024-04-12","2024-04-13","2024-04-14","2024-04-15","2024-04-16","2024-04-17","2024-04-18","2024-04-19","2024-04-20","2024-04-21"],
  #   }
  # }
if __name__ == '__main__':
  getCountData('cnt_demo', 'C158684272141', ['entrance','exit'],  'hourly', '2024-04-19', '2024-04-21')
  # getCountData('cnt_demo', 'C158684272141', ['entrance','exit'],  'monthly', '2019-04-01', '2024-04-22')
