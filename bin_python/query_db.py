# # Copyright (c) 2022, Hans kim

# # Redistribution and use in source and binary forms, with or without
# # modification, are permitted provided that the following conditions are met:
# # 1. Redistributions of source code must retain the above copyright
# # notice, this list of conditions and the following disclaimer.
# # 2. Redistributions in binary form must reproduce the above copyright
# # notice, this list of conditions and the following disclaimer in the
# # documentation and/or other materials provided with the distribution.

# # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# # CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# # INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# # MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# # DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# # CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# # SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# # BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# # SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# # INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# # WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# # NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# # OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# import os, time, sys
# import datetime
# import pymysql
# import json, re
# from functions_s import (configVars, dbconMaster, log, TZ_OFFSET)

# MYSQL = { 
#     "commonParam": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.param'),
#     "commonSnapshot": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.snapshot'),
#     "commonCount": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.counting'),
#     "commonHeatmap": configVars('software.mysql.db') +"." + configVars('software.mysql.db_common.table.heatmap'),
#     "commonCountEvent": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.count_event'),
#     "commonFace": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.face'),
#     "customCount": configVars('software.mysql.db_custom.table.count'),
#     "customHeatmap": configVars('software.mysql.db_custom.table.heatmap'),
#     "customAgeGender": configVars('software.mysql.db_custom.table.age_gender'),
#     "customSquare": configVars('software.mysql.db_custom.table.square'),
#     "customStore": configVars('software.mysql.db_custom.table.store'),
#     "customCamera": configVars('software.mysql.db_custom.table.camera'),
#     "customCounterLabel": configVars('software.mysql.db_custom.table.counter_label'),
#     "customRtCount": "realtime_counting",
# }
# MYSQL['customDB'] = 'cnt_demo'
# MYSQL['customCount'] = 'count_tenmin_p'
# MYSQL['customLanguage'] = 'language'
# _selected_language = "eng"


# def getLanguage(db_name='cnt_demo', action='pack'):
#   arr_rs = {
#     "eng":{},
#     "kor":{},
#     "chi":{},
#     # "fre":{},
#   }
#   sq = "select * from " + db_name + "." + MYSQL['customLanguage'] + " "
#   sq_pack = "select * from " + db_name + "." + MYSQL['customLanguage'] + " where flag='y' "
#   print (sq)
#   dbCon = dbconMaster()
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
    
#     if action == 'pack':
#       cur.execute(sq_pack)
#       rows = cur.fetchall()
#       for row in rows:
#         arr_rs['kor'][row['varstr']] = row['kor']
#         arr_rs['eng'][row['varstr']] = row['eng']
#         arr_rs['chi'][row['varstr']] = row['chi']
#         # arr_rs['chi'][row['varstr'].lower().replace(" ","_")] = row['chi']

#     else :
#       cur.execute(sq)
#       rows = cur.fetchall()
#       for row in rows:
#         for r in row:
#           if isinstance(row[r], datetime.datetime):
#             row[r] = str(row[r])
#           elif isinstance(row[r], bytes):
#             row[r] = str(row[r].decode())
#       arr_rs = rows

#   return arr_rs


# PLACE_DATA = []
# def getPlaceData(db_name='cnt_demo'):
#   dbCon = dbconMaster()
#   sq = "select A.code as square_code, A.name as square_name, B.code as store_code, B.name as store_name from " + db_name + "."+MYSQL['customSquare']+" as A inner join " + db_name + "."+MYSQL['customStore']+" as B on A.code=B.square_code order by A.code asc; "
#   arr = dict()
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq)
#     rows = cur.fetchall()
    
#     for row in rows:
#       if not row['square_code'] in arr:
#         arr[row['square_code']] = {"code":row['square_code'], "name": row['square_name'], "store":[]}
#       arr[row['square_code']]['store'].append({"code": row['store_code'], "name":row['store_name']})

#   # print (arr)
#   # return arr
#   arr_data = [arr[r] for r in arr]
#   return arr_data

# PLACE_DATA = getPlaceData()
# def getWebConfig(db_name='cnt_demo', page = 'main'):
# # """
# #   CREATE TABLE `web_config` (
# #     ->   `pk` int(11) unsigned NOT NULL AUTO_INCREMENT,
# #     ->   `page` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
# #     ->   `body` medium COLLATE utf8mb4_unicode_ci DEFAULT NULL,
# #     ->   `flag` enum('y','n') COLLATE utf8mb4_unicode_ci DEFAULT 'n',
# #     ->   PRIMARY KEY (`pk`)
# #     -> ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;
# # """
#   sq = "select body from cnt_demo.web_config where page='" + page + "'"
#   dbCon = dbconMaster()
#   arr = []
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq)
#     rows = cur.fetchall()

# def getWebpageConfig(db_name='cnt_demo', page='main'):
#   s_page = page.split(":")
#   sq = "select body from " + db_name + "." + "webpage_config " + " where page='" + s_page[0] + "'"
#   if len(s_page) > 1:
#     sq += " and frame='" + s_page[1] + "'"
#   if len(s_page) > 2:
#     sq += " and depth='" + s_page[2] + "'"
#   # print (sq)
#   # dbCon = dbconMaster()
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)
#   arr = []
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq)
#     rows = cur.fetchall()
    
#     for row in rows:
#       arr.append(json.loads(row['body']))
      
#   if len(arr) == 1:
#     return arr[0]
#   return arr


# def getParamByViewBy(view_by = 'hourly', date_from='', date_to=''):
#   _tz_offset = int(time.mktime(time.localtime()) -time.mktime(time.gmtime()))
#   if not view_by in ['tenmin', 'hourly', 'daily', 'weekly', 'monthly','yearly']:
#     return False
  
#   ts = time.time()
#   if not date_to:
#     date_to = time.strftime("%Y-%m-%d", time.gmtime(ts))
#   if not date_from:
#     date_from = time.strftime("%Y-%m-%d", time.gmtime(ts-3600*24))
  
#   s_date_from = date_from.split("-")
#   s_date_to = date_to.split("-")

#   param = {
#     'hourly':{
#       'group' : "year, month, day, hour, counter_label",
#       'interval' : 3600,
#       'date_format' : "%Y-%m-%d %H:%M",
#       'js_tooltip_format' : "yyyy/MM/dd HH:mm",
#       'q_datetime': "concat(year, '-', lpad(month,2,0), '-', lpad(day,2,0), ' ', lpad(hour,2,0), ':00')"
#     },
#     'daily':{
#       'group': "year, month, day, counter_label",
#       'interval' : 3600*24,
#       'date_format' : "%Y-%m-%d",
#       'js_tooltip_format' : "yyyy/MM/dd",
#       'q_datetime' : "concat(year, '-', lpad(month,2,0), '-', lpad(day,2,0))"
#     },
#     'monthly':{
#       'group': "year, month, counter_label",
#       'interval' : 3600*24*29,
#       'date_format' : "%Y-%m",
#       'js_tooltip_format' : "yyyy/MM",
#       'q_datetime' : "concat(year, '-', lpad(month,2,0))"
#     },
#     'tenmin':{
#       'group' : "year, month, day, hour, min, counter_label",
#       'interval' : 600,
#       'date_format' : "%Y-%m-%d %H:%M",
#       'js_tooltip_format' : "yyyy/MM/dd HH:mm",
#       'q_datetime' : "concat(year, '-', lpad(month,2,0), '-', lpad(day,2,0), ' ', lpad(hour,2,0), ':',lpad(min,2,0))"
#     },
#     'weekly':{
#       'group' : "year, week, counter_label",
#       'interval' : 3600*24*7,
#       'date_format' : "%Y-%m-%d",
#       'js_tooltip_format' : "yyyy/MM/dd",
#       'q_datetime' : "concat(year, '-', lpad(month,2,0), '-', lpad(day,2,0))"
#     },
#     'yearly':{
#       'group' : "year, counter_label",
#       'interval' : 3600*24*365,
#       'date_format' : "%Y",
#       'js_tooltip_format' : "yyyy",
#       'q_datetime': "year"
#     }
#   }
#   if view_by == 'monthly':
#     date_from = s_date_from[0] + '-' + s_date_from[1] + '-01'
#     date_to = str( datetime.date(int(s_date_to[0]) + int(int(s_date_to[1])/12), int(s_date_to[1])%12+1, 1) - datetime.timedelta(days=1) )
  
#   xaxis_category = []
#   ts_s = time.mktime(time.strptime(date_from, "%Y-%m-%d")) + _tz_offset
#   ts_e = time.mktime(time.strptime(date_to,   "%Y-%m-%d")) + _tz_offset + 3600*24

#   for ts in range (int(ts_s), int(ts_e), param[view_by]['interval']):
#     tss = time.gmtime(ts)
#     datetime_tag = time.strftime(param[view_by]['date_format'], tss)
#     if not datetime_tag in  xaxis_category:
#       xaxis_category.append(datetime_tag)
  
#   param[view_by]['where_timstamp'] = "(year >= %d or year <=%d) and timestamp >=%d and timestamp <%d" %(int(s_date_from[0]), int(s_date_to[0]), ts_s, ts_e)
#   param[view_by]['xaxis'] = xaxis_category
#   del(param[view_by]['interval'])
#   # del(param[view_by]['date_format'])
  
#   return param[view_by]

# def getCountData(db_name='cnt_demo', places=[], label=[], view_by='hourly', date_from='2019-01-01', date_to='', option=""):
#   ts_start = time.time()
#   # dbCon = dbconMaster()
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)
  
#   arr_where = list()
#   sfilter = list()
#   if places:
#     if not isinstance(places, list):
#       places = [places]
#     for place in places:
#       if place.startswith("SQ"):
#         sfilter.append("square_code='" + place + "'")
#       elif place.startswith("ST"):
#         sfilter.append("store_code='" + place + "'")
#       elif place.startswith("C"):
#         sfilter.append("camera_code='" + place + "'")
#   if label:
#     arr = []
#     for l in label:
#       arr.append("counter_label='" + l + "'")
#     sfilter.append("(" + " or ".join(arr) + ")")

#   if sfilter:
#     arr_where.append("(" + " and ".join(sfilter) + ")")

#   params =  getParamByViewBy(view_by, date_from, date_to)

#   arr_rs = {
#     'series': [],
#     'xaxis':{
#       'labels': {
#         'show': True,
#         'datetimeFormatter': {
#           'year': 'yyyy',
#           'month': "yyyy MM",
#           'day': 'MM/dd',
#           'hour': 'HH:mm',
#         },
#       },
#       'type': "datetime",
#       'categories': params['xaxis']
#     },
#     'yaxis': {'show': True },
#     'tooltip': {
#       'x': { 'format': params['js_tooltip_format'] }
#     }
#   }
#   # arr_rs['xaxis']['categories'] = params['xaxis']
#   arr_data = dict()
#   for xaxis in params['xaxis']:
#     arr_data[xaxis] = dict()

#   # print (json.dumps(arr_rs, indent=4))
#     # time_bt = " year >= %d and year <=%d and timestamp >=%d and timestamp <%d" %(int(date_from.split("-")[0]), int(date_to.split("-")[0]),ts_s, ts_e)
#   if params['where_timstamp']:
#     arr_where.append("(" + params['where_timstamp'] +")")

#   sq = "select " + params['q_datetime'] + " as datetime, counter_label as label, sum(counter_val) as value from " + db_name + "." + MYSQL['customCount'] + ""
#   sq += " where " + " and ".join(arr_where)
#   if params['group']:
#     sq += " group by " + params['group']
  
#   print (sq)
  
#   labels = dict()
  
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq)
#     rows = cur.fetchall()
    
#     for row in rows:
#       # print (row)
#       arr_data[row['datetime']][row['label']]= row['value']
#       if not row['label'] in labels:
#         # labels.append(row['label'])
#         labels[row['label']] = {}
    
#     if labels:
#       sq = "select  varstr, eng, kor, chi from " + db_name + "." + MYSQL['customLanguage'] + " where " + (" or ".join(["varstr='"+ l + "'" for l in labels])) + " group by varstr"
#       cur.execute(sq)
#       rows = cur.fetchall()
#       for row in rows:
#         labels[row['varstr']] = { "eng":row['eng'], "chi": row['chi'], "kor":row['kor']}

#   # return 0

#   # print (arr_data)
#   # print (arr_rs)
#   ts_now = time.time()
#   for label in labels:
#     arr = []
#     for dt in  arr_data:
#       dts = int(time.mktime(time.strptime(dt, params['date_format'])))
#       if label in arr_data[dt]:
#         arr.append(int(arr_data[dt][label]))
#       elif dts < ts_now:
#         arr.append(0)
#       else : # if dt > now => None
#         arr.append(None)
#     arr_rs['series'].append({"name": labels[label][_selected_language], "data":arr})
  
#   # if view_by =='hourly' or view_by == 'tenmin':
#   #   for i, x in enumerate(arr_rs['xaxis']['categories']):
#   #     arr_rs['xaxis']['categories'][i] = x

#   if not arr_rs['series']:
#     arr_rs['series'] = [{"data":[]}]
#     # del(arr_rs['series'])
#     # arr_rs['noData']: { text: "No Data" }
#     arr_rs['xaxis']= {'labels': {'show': False }}
#     arr_rs['yaxis']= {'show': False }
#   ts_end = time.time()
#   arr_rs['elaspe_time'] = round(ts_end-ts_start, 2)
#   return arr_rs


# def getCountByTimeData(db_name='cnt_demo', places=[], label=[], view_by='hourly', date_from0='', date_to0='', date_from1='', date_to1='', date_from2='', date_to2='', option="") :
#   ts_start = time.time()
#   # dbCon = dbconMaster()
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)
  
#   arr_where = list()
#   sfilter = list()
#   if places:
#     if not isinstance(places, list):
#       places = [places]
#     for place in places:
#       if place.startswith("SQ"):
#         sfilter.append("square_code='" + place + "'")
#       elif place.startswith("ST"):
#         sfilter.append("store_code='" + place + "'")
#       elif place.startswith("C"):
#         sfilter.append("camera_code='" + place + "'")
#   if label:
#     arr = []
#     for l in label:
#       arr.append("counter_label='" + l + "'")
#     sfilter.append("(" + " or ".join(arr) + ")")

#   if sfilter:
#     arr_where.append("(" + " and ".join(sfilter) + ")")

#   params  = getParamByViewBy(view_by, date_from0, date_to0)
#   params1 = getParamByViewBy(view_by, date_from1, date_to1)
#   params2 = getParamByViewBy(view_by, date_from2, date_to2)
  
#   arr_rs = {
#     'series': [],
#     'xaxis':{
#       'labels': {
#         'show': True,
#         'datetimeFormatter': {
#           'year': 'yyyy',
#           'month': "yyyy MM",
#           'day': 'MM/dd',
#           'hour': 'HH:mm',
#         },
#       },
#       'type': "datetime",
#       'categories': params['xaxis']
#     },
#     'yaxis': {'show': True },
#     'tooltip': {
#       'x': { 'format': params['js_tooltip_format'] }
#     }
#   }
  
#   # print (json.dumps(arr_rs, indent=4))

#   arr_where.append("(" + " or ".join([params['where_timstamp'],params1['where_timstamp'],params2['where_timstamp']]) +")")

#   arr_data = dict()
#   for xaxis in params['xaxis'] + params1['xaxis'] + params2['xaxis']:
#     arr_data[xaxis] = dict()
  
#     # if params['where_timstamp']:
#   #   arr_where.append("(" + params['where_timstamp'] +")")

#   sq = "select " + params['q_datetime'] + " as datetime, counter_label as label, sum(counter_val) as value from " + db_name + "." + MYSQL['customCount'] + ""
#   sq += " where " + " and ".join(arr_where)
#   if params['group']:
#     sq += " group by " + params['group']
  
#   print (sq)
#   labels = dict()
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq)
#     rows = cur.fetchall()
    
#     for row in rows:
#       # print (row)
#       # if not row['datetime'] in arr_data:
#       #   arr_data[row['datetime']] = dict()
#       arr_data[row['datetime']][row['label']]= row['value']
#       if not row['label'] in labels:
#       #   # labels.append(row['label'])
#         labels[row['label']] = {}

#     if labels:
#       sq = "select  varstr, eng, kor, chi from " + db_name + "." + MYSQL['customLanguage'] + " where " + (" or ".join(["varstr='"+ l + "'" for l in labels])) + " group by varstr"
#       cur.execute(sq)
#       rows = cur.fetchall()
#       for row in rows:
#         labels[row['varstr']] = { "eng":row['eng'], "chi": row['chi'], "kor":row['kor']}

#   size_xaxis = len(arr_rs['xaxis']['categories'])
#   if view_by == 'hourly' or view_by == 'tenmin':
#     date_tag0 = '(' + date_to0 + ')'
#     date_tag1 = '(' + date_to1 + ')'
#     date_tag2 = '(' + date_to2 + ')'
#   else:
#     date_tag0 = '(' + date_from0 + '~' + date_to0 + ')'
#     date_tag1 = '(' + date_from1 + '~' + date_to1 + ')'
#     date_tag2 = '(' + date_from2 + '~' + date_to2 + ')'    
  
#   for label in labels:
#       arr = []
#       for dt in  arr_data:
#         if label in arr_data[dt]:
#           arr.append(int(arr_data[dt][label]))
#         elif time.mktime(datetime.datetime.strptime(dt,params['date_format']).timetuple()) >time.time():
#           arr.append(None)
#         else : # if dt > now => None
#           arr.append(0)
#       arr_rs['series'].append({"name": date_tag0+ labels[label][_selected_language], "data":arr[:size_xaxis]})
#       arr_rs['series'].append({"name": date_tag1+ labels[label][_selected_language], "data":arr[size_xaxis:size_xaxis*2]})
#       arr_rs['series'].append({"name": date_tag2+ labels[label][_selected_language], "data":arr[size_xaxis*2:]})


#   if not arr_rs['series']:
#     arr_rs['series'] = [{"data":[]}]
#     # arr_rs['xaxis']= {'labels': {'show': False }}
#     # arr_rs['yaxis']= {'show': False }
#   ts_end = time.time()
#   arr_rs['elaspe_time'] = round(ts_end-ts_start, 2)
#   return arr_rs


# def getCountByPlaceData(db_name='cnt_demo', places=[], label=[], view_by='hourly', date_from='', date_to='', option=""):
#   ts_start = time.time()
#   params  = getParamByViewBy(view_by, date_from, date_to)
#   arr_rs = {
#     'series': [],
#     'xaxis':{
#       'labels': {
#         'show': True,
#         'datetimeFormatter': {
#           'year': 'yyyy',
#           'month': "yyyy MM",
#           'day': 'MM/dd',
#           'hour': 'HH:mm',
#         },
#       },
#       'type': "datetime",
#       'categories': params['xaxis']
#     },
#     'yaxis': {'show': True },
#     'tooltip': {
#       'x': { 'format': params['js_tooltip_format'] }
#     }
#   }
#   for sq, st in places:
#     arr_place = []
#     if not (sq == '0' or sq == 0):
#       arr_place.append(sq)
#       if not (st == '0' or st == 0):
#         arr_place.append(st)
#       arr = getCountData(db_name=db_name, places=arr_place, label=label, view_by=view_by, date_from=date_from, date_to=date_to, option=option)
#       if (arr['series'][0]['data']):
#         for i in range(len(arr['series'])):
#           for sq_o in PLACE_DATA:
#             if sq_o['code'] == sq:
#               name = sq_o['name']
#             if st:
#               for st_o in sq_o['store']:
#                 if st_o['code'] == st:
#                   name += "/"+st_o['name']
#           arr['series'][i]['name'] = name + "/" + arr['series'][i]['name']
#           arr_rs['series'].append(arr['series'][i])

#   ts_end = time.time()
#   arr_rs['elaspe_time'] = round(ts_end-ts_start, 2)
#   return arr_rs

# def getTrafficData(db_name='cnt_demo', places=[], label=[], view_by='hourly', date_from='', date_to='', option=""):
#   ts_start = time.time()
#   # dbCon = dbconMaster()
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)
  
#   arr_where = list()
#   sfilter = list()
#   if places:
#     if not isinstance(places, list):
#       places = [places]
#     for place in places:
#       if place.startswith("SQ"):
#         sfilter.append("square_code='" + place + "'")
#       elif place.startswith("ST"):
#         sfilter.append("store_code='" + place + "'")
#       elif place.startswith("C"):
#         sfilter.append("camera_code='" + place + "'")
#   if label:
#     arr = []
#     for l in label:
#       arr.append("counter_label='" + l + "'")
#     sfilter.append("(" + " or ".join(arr) + ")")

#   if sfilter:
#     arr_where.append("(" + " and ".join(sfilter) + ")")

#   params =  getParamByViewBy(view_by, date_from, date_to)

#   arr_rs = {
#     'series': [],
#     'xaxis':{
#       'labels': {
#         'show': True,
#         'datetimeFormatter': {
#           'year': 'yyyy',
#           'month': "yyyy MM",
#           'day': 'MM/dd',
#           'hour': 'HH:mm',
#         },
#       },
#       'type': "datetime",
#       'categories': params['xaxis'][0:24]
#     },
#     'yaxis': {'show': True },
#     'tooltip': {
#       'x': { 'format': "HH:mm" }
#     }
#   }

#   # if view_by == 'hourly':
#   #   for i in range(24):
#   #     arr_rs['xaxis']['categories'].append("%02d:00" %i)
#   #   arr_rs['tooltip']['x']['format'] = "HH:mm"

#   # arr_rs['xaxis']['categories'] = params['xaxis']
#   arr_data = dict()
#   for xaxis in params['xaxis']:
#     arr_data[xaxis] = dict()

#   # print (json.dumps(arr_rs, indent=4))
#     # time_bt = " year >= %d and year <=%d and timestamp >=%d and timestamp <%d" %(int(date_from.split("-")[0]), int(date_to.split("-")[0]),ts_s, ts_e)
#   if params['where_timstamp']:
#     arr_where.append("(" + params['where_timstamp'] +")")

#   sq = "select " + params['q_datetime'] + " as datetime, counter_label as label, sum(counter_val) as value from " + db_name + "." + MYSQL['customCount'] + ""
#   sq += " where " + " and ".join(arr_where)
#   if params['group']:
#     sq += " group by " + params['group'] + ""
  
#   print (sq)
  
#   labels = dict()
  
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq)
#     rows = cur.fetchall()
    
#     for row in rows:
#       # print (row)
#       arr_data[row['datetime']][row['label']]= row['value']
#       if not row['label'] in labels:
#         # labels.append(row['label'])
#         labels[row['label']] = {}
    
#   ts_now = time.time()
#   for label in labels:
#     arr = []
#     for dt in  arr_data:
#       dtx = time.strptime(dt, params['date_format'])
#       if label in arr_data[dt]:
#         arr.append(int(arr_data[dt][label]))
#       elif int(time.mktime(dtx)) < ts_now:
#         arr.append(0)
#       else : # if dt > now => None
#         arr.append(None)
      
#       if dtx.tm_hour == 23:
#         date_str = time.strftime("%Y-%m-%d", dtx)
#         arr_rs['series'].append({"name": date_str, "data":arr})
#         arr = []

#   # if view_by =='hourly' or view_by == 'tenmin':
#   #   for i, x in enumerate(arr_rs['xaxis']['categories']):
#   #     arr_rs['xaxis']['categories'][i] = x

#   if not arr_rs['series']:
#     arr_rs['series'] = [{"data":[]}]
#     # del(arr_rs['series'])
#     # arr_rs['noData']: { text: "No Data" }
#     arr_rs['xaxis']= {'labels': {'show': True }}
#     arr_rs['yaxis']= {'show': False }
#   ts_end = time.time()
#   arr_rs['elaspe_time'] = round(ts_end-ts_start, 2)
#   return arr_rs

# def listDevicesX(db_name='cnt_demo', places=[]):
#   ts_start = time.time()
#   sfilter = list()
#   if places:
#     if not isinstance(places, list):
#       places = [places]
#     for place in places:
#       if place.startswith("SQ"):
#         sfilter.append("square_code='" + place + "'")
#       elif place.startswith("ST"):
#         sfilter.append("store_code='" + place + "'")
#       elif place.startswith("C"):
#         sfilter.append("camera_code='" + place + "'")

#   sq = "select code, usn, product_id, name, store_code, comment, enable_countingline, enable_heatmap, enable_snapshot, enable_face_det, enable_macsniff, flag, device_info from " + db_name + "." + MYSQL['customCamera']
#   if sfilter:
#     sq += " where " + " and ".join(sfilter)
  
#   arr_rs = {
#     'device': [],
#     'elaspe_time':0
#   }
#   # dbCon = dbconMaster()
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq)
#     rows = cur.fetchall()

#     for row in rows:
#       if not row['device_info']:
#         continue

#       arr = {
#         'device_info': row['device_info'],
#         'usn': row['usn'],
#         'product_id': row['product_id'],
#         'square_code': '',
#         'square_name': '',
#         'store_code': row['store_code'],
#         'store_name': '',
#         'camera_code': row['code'],
#         'camera_name' : row['name'],
#         'license': '',
#         'functions': {
#           'face_det': False,
#           'heatmap':  False,
#           'countrpt': False,
#           'macsniff': False,
#         },
#         'enable_function':{
#           'enable_countingline': True if row['enable_countingline'] == 'y' else False,
#           'enable_heatmap':      True if row['enable_heatmap'] == 'y'      else False,
#           'enable_snapshot':     True if row['enable_snapshot'] == 'y'     else False,
#           'enable_face_det':     True if row['enable_face_det'] == 'y'     else False,
#           'enable_macsniff':     True if row['enable_macsniff'] == 'y'     else False,
#         },
#         'snapshot': {
#           'date': '',
#           'body': ''
#         },
#         'last_access': ''
#       }

#       sq = "select regdate, body from " + MYSQL['commonSnapshot'] + " where device_info='" + row['device_info'] + "' order by regdate desc limit 1"
#       cur.execute(sq)
#       rs_snapshot = cur.fetchone()
#       if rs_snapshot:
#         arr['snapshot']['date'] = str(rs_snapshot['regdate'])
#         arr['snapshot']['body'] = str(rs_snapshot['body'].decode())

#       sq = "select last_access, lic_pro, lic_surv, lic_count, face_det, heatmap, countrpt, macsniff, initial_access from " + MYSQL['commonParam'] + " where device_info='" + row['device_info'] + "' order by last_access desc limit 1"
#       cur.execute(sq)
#       rs_param = cur.fetchone()
      
#       if rs_param :
#         lic = []
#         if rs_param['lic_pro'] == 'y': 
#           lic.append('PRO')
#         if rs_param['lic_surv'] == 'y':
#           lic.append('SURV')
#         if rs_param['lic_count'] == 'y':
#           lic.append('COUNT')
#         arr['license'] = "/".join(lic)
#         arr['last_access'] = str(rs_param['last_access'])

#       sq = "select A.code as store_code, A.name as store_name, B.code as square_code, B.name as square_name from " + db_name + "." + MYSQL['customStore'] + " as A inner join " + db_name + "." + MYSQL['customSquare'] + " as B on A.square_code = B.code where A.code='" + row['store_code'] + "'"
#       cur.execute(sq)
#       rs_place = cur.fetchone()
#       if rs_place:
#         arr['store_code']  = rs_place['store_code']
#         arr['store_name']  = rs_place['store_name']
#         arr['square_code'] = rs_place['square_code']
#         arr['square_name'] = rs_place['square_name']

#       arr_rs['device'].append(arr)
#   sorted(arr_rs['device'])  
#   ts_end = time.time()
#   arr_rs['elaspe_time'] = round(ts_end-ts_start, 2)  
#   return arr_rs

# # """
# # VCA.Ch0.Zn0.color=255,0,0
# # VCA.Ch0.Zn0.enable=yes
# # VCA.Ch0.Zn0.name=Zone 0
# # VCA.Ch0.Zn0.points=42598:40822,36450:53892
# # VCA.Ch0.Zn0.style=line
# # VCA.Ch0.Zn0.type=alarm
# # VCA.Ch0.Zn0.uid=0

# # VCA.Ch0.Zn1.color=0,0,255
# # VCA.Ch0.Zn1.enable=yes
# # VCA.Ch0.Zn1.name=Zone 1
# # VCA.Ch0.Zn1.points=40788:10073,44643:3653,53970:5977,64104:9741,63856:23579,57327:20590,51420:30774,44892:30110,40415:19483
# # VCA.Ch0.Zn1.style=polygon
# # VCA.Ch0.Zn1.type=alarm
# # VCA.Ch0.Zn1.uid=5

# # VCA.Ch0.Zn2.color=0,0,255
# # VCA.Ch0.Zn2.enable=yes
# # VCA.Ch0.Zn2.name=Zone 2
# # VCA.Ch0.Zn2.points=8643:26346,22384:21918,23689:31217,26176:41623,11565:48265
# # VCA.Ch0.Zn2.style=polygon
# # VCA.Ch0.Zn2.type=alarm
# # VCA.Ch0.Zn2.uid=8
# # """

# def getZone(param):
#   regex = re.compile(r"VCA.Ch0.Zn(\d+).(\w+)=(.+)", re.IGNORECASE)
#   arr = dict()
#   lines = param.splitlines()
#   for line in lines:
#     m = regex.search(line)
#     if m:
#       # print (m.group(1), m.group(2), m.group(3))
#       if not m.group(1) in arr:
#         arr[m.group(1)] = {}
#       arr[m.group(1)][m.group(2)] = m.group(3)
  
#   zone = [ arr[r] for r in arr]
#   return zone

# def listDevices(db_name='cnt_demo', places=[]):
#   ts_start = time.time()
#   sfilter = list()
#   if places:
#     if not isinstance(places, list):
#       places = [places]
#     for place in places:
#       if place.startswith("SQ"):
#         sfilter.append("square_code='" + place + "'")
#       elif place.startswith("ST"):
#         sfilter.append("store_code='" + place + "'")
#       elif place.startswith("C"):
#         sfilter.append("camera_code='" + place + "'")

#   sq = "select A.code, A.usn, A.product_id, A.name, A.store_code, A.comment, A.enable_countingline, A.enable_heatmap, A.enable_snapshot, A.enable_face_det, A.enable_macsniff, A.flag, A.device_info, B.last_access, B.lic_pro, B.lic_surv, B.lic_count, B.face_det, B.heatmap, B.countrpt, B.macsniff, B.initial_access, B.param, B.url as ip from " + db_name + "." + MYSQL['customCamera'] + " as A inner join " + MYSQL['commonParam'] + " as B on A.device_info = B.device_info "
#   if sfilter:
#     sq += " where " + " and ".join(sfilter)
#   sq +=  " order by B.last_access desc "
#   print (sq)
#   arr_rs = {
#     'device': [],
#     'elaspe_time':0
#   }
#   # dbCon = dbconMaster()
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq)
#     rows = cur.fetchall()

#     for row in rows:
#       if not row['device_info']:
#         continue

#       lic = []
#       if row['lic_pro'] == 'y': 
#         lic.append('PRO')
#       if row['lic_surv'] == 'y':
#         lic.append('SURV')
#       if row['lic_count'] == 'y':
#         lic.append('COUNT')

#       arr = {
#         'device_info': row['device_info'],
#         'usn': row['usn'],
#         'product_id': row['product_id'],
#         'square_code': '',
#         'square_name': '',
#         'store_code': row['store_code'],
#         'store_name': '',
#         'camera_code': row['code'],
#         'camera_name' : row['name'],
#         'license': "/".join(lic),
#         'functions': {
#           'face_det': True if row['face_det'] == 'y' else False,
#           'heatmap':  True if row['heatmap']  == 'y' else False,
#           'countrpt': True if row['countrpt'] == 'y' else False,
#           'macsniff': True if row['macsniff'] == 'y' else False,
#         },
#         'features':{
#           'enable_countingline': True if row['enable_countingline'] == 'y' else False,
#           'enable_heatmap':      True if row['enable_heatmap'] == 'y'      else False,
#           'enable_snapshot':     True if row['enable_snapshot'] == 'y'     else False,
#           'enable_face_det':     True if row['enable_face_det'] == 'y'     else False,
#           'enable_macsniff':     True if row['enable_macsniff'] == 'y'     else False,
#         },
#         'snapshot': {
#           'date': '',
#           'body': ''
#         },
#         'initial_access': str(row['initial_access']),
#         'last_access': str(row['last_access']),
#         'zone_info': getZone(row['param']),
#         'ip': row['ip']
#       }

#       sq = "select regdate, body from " + MYSQL['commonSnapshot'] + " where device_info='" + row['device_info'] + "' order by regdate desc limit 1"
#       cur.execute(sq)
#       rs_snapshot = cur.fetchone()
#       if rs_snapshot:
#         arr['snapshot']['date'] = str(rs_snapshot['regdate'])
#         arr['snapshot']['body'] = str(rs_snapshot['body'].decode())     

#       sq = "select A.code as store_code, A.name as store_name, B.code as square_code, B.name as square_name from " + db_name + "." + MYSQL['customStore'] + " as A inner join " + db_name + "." + MYSQL['customSquare'] + " as B on A.square_code = B.code where A.code='" + row['store_code'] + "'"
#       cur.execute(sq)
#       rs_place = cur.fetchone()
#       if rs_place:
#         arr['store_code']  = rs_place['store_code']
#         arr['store_name']  = rs_place['store_name']
#         arr['square_code'] = rs_place['square_code']
#         arr['square_name'] = rs_place['square_name']

#       arr_rs['device'].append(arr)

#   ts_end = time.time()
#   arr_rs['elaspe_time'] = round(ts_end-ts_start, 2)  
#   return arr_rs

# def siteMap(db_name='cnt_demo'):
#   arr_rs = list()
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)

#     sq = "select code, name from "+ db_name + "." + MYSQL['customSquare']
#     cur.execute(sq)
#     rows_square = cur.fetchall()
#     for i, row_sq in enumerate(rows_square):
#       # print (row_sq)
#       arr_rs.append({"code":row_sq['code'],"name": row_sq['name'], "store":[]})
#       sq = "select code, name from "+ db_name + "." + MYSQL['customStore'] + " where square_code='" + row_sq['code'] +"'"
#       cur.execute(sq)
#       rows_store = cur.fetchall()
#       for j, row_st in enumerate(rows_store):
#         # print (row_st)
#         arr_rs[i]['store'].append({"code": row_st['code'], "name":row_st['name'], "camera":[]})
#         sq = "select code, name, enable_countingline, enable_heatmap, enable_face_det, enable_macsniff, device_info from "+ db_name + "." + MYSQL['customCamera'] + " where store_code='" + row_st['code'] +"'"
#         cur.execute(sq)
#         rows_camera = cur.fetchall()
#         for k, row_cam in enumerate(rows_camera):
#           sq = "select body from " + MYSQL['commonSnapshot'] + " where device_info='" + row_cam['device_info'] +"' order by regdate desc limit 1"
#           cur.execute(sq)
#           print (cur.rowcount)
#           if cur.rowcount:
#             snapshot = cur.fetchone()['body'].decode()
#             # print (snapshot)

#           arr_rs[i]['store'][j]['camera'].append({
#             "code": row_cam['code'], 
#             "name":row_cam['name'],
#             "enable_countingline": row_cam['enable_countingline'],
#             "enable_heatmap": row_cam['enable_heatmap'],
#             "enable_face_det": row_cam['enable_face_det'],
#             "enable_macsniff": row_cam['enable_macsniff'],
#             "snapshot": snapshot,
#           })
#   return arr_rs

# def queryDatabase(post_data): # using post data
#   ts_start = time.time()
#   arr_rs = {"total_records":0, "fields": [], "data":[]}
#   sq_t = "select count(*) as total from " + post_data['db'] + "." + post_data['table'] + " "

#   if not post_data['fields']:
#     sq = "select *  from " + post_data['db']  + "." + post_data['table'] + " "
#   else:
#     sq = "select " + ",".join(post_data['fields']) + " from " +  post_data['db'] + "." +  post_data['table'] + " "
#   if post_data['search']:
#     sq += " where "

#   if not post_data['page_max']:
#     post_data['page_max'] = 20
#   if not post_data['page_no']:
#     post_data['page_no'] = 1
#   offset = (post_data['page_no'] -1 ) * post_data['page_max']

#   if post_data['orderby']:
#     sq += " order by " + post_data['orderby']
#   sq += " limit %d, %d"  %(offset, post_data['page_max'])

#   print (sq)
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)
  
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq_t)
#     arr_rs['total_records'] = cur.fetchone()['total']

#     cur.execute(sq)
#     rows = cur.fetchall()
#     for row in rows:
#       arr = []

#       for r in row:
#         if isinstance(row[r], datetime.datetime):
#           row[r] = str(row[r])
#         elif isinstance(row[r], bytes):
#           row[r] = str(row[r].decode())

#       arr_rs['data'].append(row)

#   arr_rs['fields']  = [x  for x in rows[0]]
#   ts_end = time.time()
#   arr_rs['elaspe_time'] = round(ts_end-ts_start, 2)  
#   return arr_rs


# def test_webconf():
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)
#   arr_rs = {}  
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     sq = "select * from cnt_demo.webpage_config"
#     cur.execute(sq)
#     rows = cur.fetchall()
#     for row in rows:
#       t = row['page']
#       if not t in arr_rs:
#         arr_rs[t] = []

#       if t == 'main_menu':
#         xt = json.loads(row['body'])
#         arr_rs[t].append({
#           "page": row['frame'].lower(),
#           "parent": 0,
#           "depth":row['depth'],
#           "i18n_t":xt['lang_key'].lower(),
#           "icon": xt['icon'],
#           "to": "/" + xt['href'].split("=")[1] if len(xt['href'].split("="))>1 else xt['href'],
#           "use" : row['flag'],
#           # "body": xt,
#           # "etc": row
#       })
#       elif t == 'admin_menu':
#         xt = json.loads(row['body'])
#         arr_rs[t].append({
#           "page": row['frame'].lower(),
#           "parent": 0,
#           "depth":row['depth'],
#           "i18n_t":xt['lang_key'].lower(),
#           "icon": xt['icon'],
#           "to": "/admin/" + xt['href'].split("=")[1] if len(xt['href'].split("="))>1 else xt['href'],
#           "use" : row['flag'],
#           # "body": xt,
#           # "etc": row
#       })      
#       elif (t == "dashboard"):
#         xt = json.loads(row['body'])
#         arr_rs[t].append({
#           "page": row['frame'].lower(),
#           "depth":row['depth'],
#           "i18n_t":xt['display'].lower() if xt.get('display') else xt['title'],
#           "color": xt.get('color'),
#           "labels": xt.get('labels'),
#           "use" : row['flag'],
#         })
#       elif ( t == 'analysis'):
#         try:
#           xt = json.loads(row['body'])
#         except: 
#           xt = [row['body']]

#         arr_rs[t].append({
#           "page": row['frame'].lower(),
#           "depth":row['depth'],
#           "i18n_t":row['frame'].lower(),
#           "labels": xt['labels'] if isinstance(xt, dict) else xt,
#           "use" : row['flag'],
#           # "body": xt,
#           # "etc": row
#         })
#       elif ( t == 'report'):
#         xt = json.loads(row['body'])
#         arr_rs[t].append({
#           "page": xt['category'],
#           "depth":row['depth'],
#           "i18n_t":xt['category'].lower(),
#           "labels": xt['labels'] if isinstance(xt, dict) else xt,
#           "use" : row['flag'],
#           # "body": xt,
#           # "etc": row
#           #     
#         })
#   # "report": [],
#   # "realtime_screen": [])
#     # print (json.dumps(arr_rs['report'],  ensure_ascii=False, indent=2))
#     # body = (json.dumps(arr_rs,  ensure_ascii=False, indent=2))
#     body = (json.dumps(arr_rs,  ensure_ascii=False, indent=2))
    
#     with open("./webpage_config.json", "w") as f:
#       f.write(body)
#       # f.write('{\n')
#       # for r in arr_rs:
#       #   f.write('"'+r+'":[')
#       #   for x in arr_rs[r]:
#       #     f.write(json.dumps(x,  ensure_ascii=False))
#       #     f.write(",\n")
#       #   f.write("],\n")

#       # f.write('}')
#       # f.write(body)
# def test_wr_wenconf():
#   dbCon = dbconMaster(host = '192.168.1.250', user = 'rt_user', password = '13579', db = 'cnt_demo', charset ='utf8', port=3306)

#   # with open("./webpage_config.js", "r") as f:
#   #   body = f.read()
  
#   arr = {
#     'path': '/#footfall',
#     'meta': { 'title': 'DataGlunt', 'icon': 'code' },
#     'children': [
#       {
#         'path': '/dataglunt',
#         'component':('@/views/DataGlunt.vue'),
#         'meta': { 'title': 'DataGlunt', 'icon': 'code' }
#       },
#       {
#         'path': '/recentdata',
#         'component':('@/views/RecentData.vue'),
#         'meta': { 'title': 'DataGlunt', 'icon': 'fa-code' }
#       },
#       {
#         'path': '/trendanalysis',
#         'component':('@/views/TrendAnalysis.vue'),
#       },
#       {
#         'path': '/advancedanalysis',
#         'component':('@/views/AdvancedAnalysis.vue'),
#       }
#     ]
#   }
  
#   print (arr)
#   return arr
#   # arr = json.loads(body)
#   # with dbCon:
#   #   cur = dbCon.cursor(pymysql.cursors.DictCursor)
#   #   for r in arr:
#   #     jbody = json.dumps(arr[r], ensure_ascii=False)
#   #     sq = "insert into cnt_demo.webconfig(page, body, flag ) values( '%s', '%s', '%s')" %(r, jbody, 'y')
#   #     print (sq)
#     # cur.execute(sq)

#     # print (json.loads(body))  
# if __name__ == '__main__':
#   # test_webconf()
#   test_wr_wenconf()
#   # x = getLanguage()
#   # print (json.dumps(x,  ensure_ascii=False, indent=4))

#   # getSystemLog()
#   # x = siteMap()
#   # print (json.dumps(x, indent=4))
#   # x = queryDatabase({'data': 'querydb', 'fmt': 'json', 'db': 'common', 'table': 'face_thumbnail', 'fields':['pk','thumbnail'], 'search':'', 'page_no':0, 'page_max':0, 'orderby':''})
#   # print (x)
#   # print (json.dumps(x, indent=4))

#   # x = getCountData('cnt_demo', 'C158684272141', ['entrance','exit'],  'hourly', '2024-04-19', '2024-04-21')
#   # print (json.dumps(x, indent=4))

#   # getCountData('cnt_demo', 'C158684272141', ['entrance','exit'],  'monthly', '2019-04-01', '2024-04-22')
#   # x = getPlaceData()
#   # print(json.dumps(x, indent=4))
#   # import datetime
#   # def lom(year, month, day):
#   #     d = datetime.date(year + int(month/12), month%12+1, 1)-datetime.timedelta(days=1)
#   #     return d
#   # print(lom(2021,12,16)) 

#   # x = getParamByViewBy(view_by = 'monthly', date_from='2021-12', date_to='2024-05')
#   # print (json.dumps(x, indent=4))
#   # {'data': 'countbytime', 'fmt': 'json', 'sq': '0', 'st': '0', 'cam': '0', 'label': 'entrance', 'date_from0': '2024-04-28', 'date_to0': '2024-04-28', 'date_from1': '2024-04-21', 'date_to1': '2024-04-21', 'date_from2': '2023-04-29', 'date_to2': '2023-04-29', 'view_by': 'hourly'}
#   # x = getCountByTimeData(db_name='cnt_demo', places=[], label=['entrance'], view_by='hourly', date_from0='2024-04-28', date_to0='2024-04-28', date_from1='2024-04-21', date_to1='2024-04-21', date_from2='2023-04-29', date_to2='2023-04-29', format='json', option="")
#   # print (json.dumps(x, indent=4))

#   # print (datetime.datetime.now())
#   # s = int(time.mktime(time.localtime()))


#   # for t in range(24):
#   #   x = int(time.mktime(time.strptime('2024-04-29 %02d:00' %t, '%Y-%m-%d %H:00')))
    
#   #   print(t, x, s, x-s)

#   # print (time.gmtime())
#   # print(time.localtime())

#   # print (time.mktime(time.gmtime()) - time.mktime(time.localtime()))
#   # x = getWebpageConfig(page='analysis:dataglunt')
#   # print (x)
#   # x = getWebpageConfig(page='dashboard:card_banner')
#   # print(x)
#   # for sq_o in PLACE_DATA:
#   #   print (sq_o['code'])
#   # x = getCountByPlaceData(db_name='cnt_demo', places=[('SQ1547972440547',0),('SQ1547972950349',0)], label=['entrance', 'exit'], view_by='hourly', date_from='2024-04-01', date_to='2024-04-01', option="")
#   # print (json.dumps(x, indent=4))

#   # x = getTrafficData(db_name='cnt_demo', places=[], label=['entrance'], view_by='hourly', date_from='2024-04-01', date_to='2024-04-07', option="")
#   # print (json.dumps(x, indent=4))
#   # x = listDevices('cnt_demo')
#   # print (json.dumps(x, indent=4))
  
# #   param = """
# # VCA.Ch0.Zn0.color=255,0,0
# # VCA.Ch0.Zn0.enable=yes
# # VCA.Ch0.Zn0.name=Zone 0
# # VCA.Ch0.Zn0.points=42598:40822,36450:53892
# # VCA.Ch0.Zn0.style=line
# # VCA.Ch0.Zn0.type=alarm
# # VCA.Ch0.Zn0.uid=0

# # VCA.Ch0.Zn1.color=0,0,255
# # VCA.Ch0.Zn1.enable=yes
# # VCA.Ch0.Zn1.name=Zone 1
# # VCA.Ch0.Zn1.points=40788:10073,44643:3653,53970:5977,64104:9741,63856:23579,57327:20590,51420:30774,44892:30110,40415:19483
# # VCA.Ch0.Zn1.style=polygon
# # VCA.Ch0.Zn1.type=alarm
# # VCA.Ch0.Zn1.uid=5

# # VCA.Ch0.Zn2.color=0,0,255
# # VCA.Ch0.Zn2.enable=yes
# # VCA.Ch0.Zn2.name=Zone 2
# # VCA.Ch0.Zn2.points=8643:26346,22384:21918,23689:31217,26176:41623,11565:48265
# # VCA.Ch0.Zn2.style=polygon
# # VCA.Ch0.Zn2.type=alarm
# # VCA.Ch0.Zn2.uid=8
# # """
#   # x = getZone(param)
#   # print (json.dumps(x, indent=4))
  
#   # zone = [
#   # {"color":"255,0,0","enable":"yes","name":"Zone 0","points":"42598:40822,36450:53892","style":"line","type":"alarm","uid":"0"},
#   # {"color":"0,0,255","enable":"yes","name":"Zone 1","points":"40788:10073,44643:3653,53970:5977,64104:9741,63856:23579,57327:20590,51420:30774,44892:30110,40415:19483","style":"polygon","type":"alarm","uid":"5"},
#   # {"color":"0,0,255","enable":"yes","name":"Zone 2","points":"8643:26346,22384:21918,23689:31217,26176:41623,11565:48265","style":"polygon","type":"alarm","uid":"8"}]


