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

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, urlsplit, parse_qsl, uses_params
import os, sys, time, datetime
import json

from web_server.users           import procLogin, getUserList, updateUser, changePassword
from web_server.language        import getLanguagePack
from web_server.webpage_config  import getWebConfig
from web_server.counting        import getPlaceData
from web_server.database        import queryDatabase, updateDatabase, insertDatabase

# from web_server.query_db import getCountData, getPlaceData, getTrafficData, listDevices, siteMap, queryDatabase, getLanguagePack, getWebConfig, procLogin
# from web_server.update_db import updateLanguage, updateWebConfig, updateDatabase

def getJsonFromFile(filename, cat = "systemlog"):
  ts_start = time.time()
  with open (filename, 'r')  as f:
    body = f.read()

  if cat == "systemlog":
    arr_rs = {"total_records":0, "fields":['no', 'levelname', 'asctime', 'module', 'funcName', 'lineno',  'threadName', 'message'], "data":[]}
    for i, line in enumerate(body.splitlines()):
      # arr_rs['total_records'] += 1
      lx = line[34:].split(" ")
      arr_rs['data'].append({
        'no':i+1, 
        'level':line[0:8], 
        'date':line[10:29], 
        'module': lx[0], 
        'function':lx[1], 
        'line':lx[2], 
        'thread': lx[-1], 
        'message': " ".join(lx[3:-1])
      })
    arr_rs['total_records'] = i
  else:
    lines = body.splilines()
    arr_rs = {
      "total_records":len(lines), 
      "fields":[], 
      "data":lines
    }

  ts_end = time.time()
  arr_rs['elaspe_time'] = round(ts_end-ts_start, 2)  
  return arr_rs

def getConfig():
  with open ('config/config.json', 'r') as f:
    body = f.read()
  return body


def proc_api(url_parts, post_data = {}):
    script_name = url_parts.path.split("/")[-1]
    query = dict(parse_qsl(urlsplit(url_parts.query).path))
    # {'data': 'count', 'fmt': 'json', 'sq': '0', 'st': '0', 'cam': '0', 'date_from': '2024-04-19', 'date_to': '2024-04-20', 'view_by': 'hourly'}
    print ('query:',query)
    print ('post_data:',post_data)
    arr= {}
    if not query.get('db_name'):
      query['db_name'] = 'cnt_demo'

    if script_name == 'login': # post
      arr = procLogin(post_data)

    elif script_name == 'getconfig':
      arr = getConfig()

    elif script_name == 'query':
      if query['data'] == 'language': # get
        if not query.get('action'):
          query['action'] = 'pack'

        arr = getLanguagePack(query['db_name'], query['action'])

      elif query['data'] == 'place': # get
        arr = getPlaceData(query['db_name'])

      elif query['data'] == 'webconfig': # get
        arr = getWebConfig(query['db_name'], query['page'])

      elif query['data'] == 'jsonfromfile': # get
        arr = getJsonFromFile(query['filename'], query['cat'])

      elif query['data'] == 'querydb': # post
        arr = queryDatabase(post_data)
      elif query['data'] == 'getUserList': # post
        arr = getUserList(post_data)        




      # elif query['data'] == 'count': # post
      #   arr = getCountData(post_data)
      
      # elif query['data']=='trafficdistribution': # post
      #   arr = getTrafficData(post_data)

      # elif query['data'] == 'listdevice': # post
      #   arr = listDevices(post_data)

      # elif query['data'] == 'sitemap': # post
      #   arr = siteMap(post_data)



    elif script_name == 'update':
      if query['data'] == 'language':
        arr = updateLanguage(post_data)
      
      elif query['data'] == 'webconfig':
        # print (post_data)
        updateWebConfig(db_name=query['db_name'], page=query['page'], body=post_data['data'])

      elif query['data'] == 'updatedb':
        arr = updateDatabase(post_data)

      elif query['data'] == 'updateUser':
        arr = updateUser(post_data)

      elif query['data'] == 'changePassword':
        arr = changePassword(post_data)

    elif query['data'] == 'insertdb':
      arr = insertDatabase(post_data)
    
    if query.get('fmt') == 'json' or post_data.get('format') == 'json':
      body = json.dumps(arr)
      # print (body)
      return 'text/json', body.encode()
    
    elif isinstance(arr, str):
      return 'text/json', arr.encode()

