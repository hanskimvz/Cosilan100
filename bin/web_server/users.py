
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

import os, sys, time, datetime
import hashlib
from bson import ObjectId

from functions_s import (MONGO, db_connect)



def procLogin(post_data= {}):
  if not post_data.get('id'):
    return {"code": 1002, "description": "no_id"}
  if not post_data.get('password'):
    return {"code": 1003, "description": "no_password"}
  
  client = db_connect()
  collection = client[MONGO['db']][MONGO['commonUser']]
  row = collection.find_one({"id": post_data.get('id').strip()})

  if not row:
    client.close()
    return {"code": 1004, "description": "no_user_id"}
  
  db_name = row['db_name']
  if db_name == 'none':
    client.close()
    return {"code": 1005, "description": "no_db_name"}
  
  collection = client[db_name][MONGO['customUser']]
  row_custom = collection.find_one({"id": post_data.get('id').strip()})

  if row_custom['pw'] != post_data['password']:
    client.close()
    return {"code": 1005, "description": "password_not_match"}

  del(row_custom['pw'])
  for r in row_custom:
    if isinstance(row_custom[r], datetime.datetime):
      row_custom[r] = str(row_custom[r])
    elif isinstance(row_custom[r], ObjectId):
      row_custom[r] = str(row_custom[r])

  row_custom['userseq'] = hashlib.md5((row_custom['id'] + 'hanskim').encode()).hexdigest()
  row_custom['db_name'] = db_name

  print ('row_custom', row_custom)
  client.close()
  return {"code": 1000, "description": row_custom }
  
def checkUserseq(headers):
# cookie: _temp=123456; _selected_language=kor; _login_id=hanskim; _db_name=cnt_demo; _role=admin; _name=Hans%20Kim; _userseq=ca29e7325bf9825817bc185cb3435f49
# accept-language: en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,zh-CN;q=0.6,zh;q=0.5
# accept-encoding: gzip, deflate
# referer: http://192.168.1.252:5173/recentdata
# user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36
# accept: application/json, text/plain, */*
# connection: close
# host: 192.168.1.252:9999

# Host: 192.168.1.252:9999
# Connection: keep-alive
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
# Accept-Encoding: gzip, deflate
# Accept-Language: en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,zh-CN;q=0.6,zh;q=0.5
# Cookie: _temp=123456


#   print (headers)
  arr = {'host':'', 'connection': 'keep-alive', 'user-agent':'', 'cookie':'', 'cookies':{}}
  for head in headers :
    arr[head.lower()] = headers[head]
  
#   print ('referer', arr['referer'])
  if arr['referer'].split("/")[-2] == 'account' and arr['referer'].split("/")[-1] == 'register':
    return True
  
  if not arr.get('cookie'):
    # print ('no cookie')
    return False
  
  for key, val in [tuple(x.strip().split("=")) for x in arr['cookie'].split(";")]:
      arr['cookies'][key] = val
  # if headers.get('referer')  and headers['referer'].split("/")[-1] == 'login':
  #   return True
  # print (hashlib.md5((arr['cookies']['_login_id'] + 'hanskim').encode()).hexdigest() )
  # print (arr['cookies']['_userseq'])
  print (arr)
  if not arr['cookies'].get('_userseq'):
    # print ('no userseq')
    return False
  if not arr['cookies'].get('_login_id'):
    # print ('no login_id')
    return False
  if arr['cookies']['_userseq'] == hashlib.md5((arr['cookies']['_login_id'] + 'hanskim').encode()).hexdigest():
    # print ('userseq ok')
    return True
  return False

def getUserList(post_data= {}):
  print (post_data)
  client = db_connect()
  collection = client[post_data['db_name']][MONGO['customUser']]

  rows = collection.find({})
  arr_rs = []
  for row in rows:
    row['_id'] = str(row['_id'])
    del(row['pw'])
    for key, value in row.items():
      if isinstance(value, (datetime.datetime, datetime.date)):
        row[key] = value.isoformat()    
    arr_rs.append(row)
  print (arr_rs)
  client.close()
  return {"code": 1000, "description": "success", "data": arr_rs }


def updateUser(post_data= {}):
    print(post_data)
    arr_rs = {"code": 1000, "description": "success"}
    ts_start = time.time()

    if not post_data.get('update'):
        return {"code": 1002, "description": "no_update"}

    if  not (post_data['role'] == 'admin' or post_data['id'] == post_data['update']['id']):
        return {"code": 1002, "description": "cannot_update"}

    client = db_connect()
    collection = client[post_data['db_name']][MONGO['customUser']]

    if '_id' in post_data['filter'] and isinstance(post_data['filter']['_id'], str):
        post_data['filter']['_id'] = ObjectId(post_data['filter']['_id'])

    x = collection.update_one(post_data['filter'], {'$set': post_data['update']})
    print('result:', x)
    client.close()
    arr_rs['elapsed_time'] = round(time.time() - ts_start, 2)
    return arr_rs

def deleteUser(post_data= {}):
    print(post_data)
    arr_rs = {"code": 1000, "description": "success"}
    ts_start = time.time()
    client = db_connect()
    collection = client[post_data['db_name']][MONGO['customUser']]
    x = collection.delete_one(post_data['filter'])
    if x.deleted_count == 0:
        client.close()
        return {"code": 1002, "description": "no_delete"}

    collection = client[MONGO['db']][MONGO['commonUser']]
    x = collection.update_one({'id':post_data['update']['id']}, {'$set': {'db_name':'none'}})
    print('result:', x)
    client.close()
    arr_rs['elapsed_time'] = round(time.time() - ts_start, 2)
    return arr_rs

def changePassword(post_data= {}):
    print(post_data)
    arr_rs = {"code": 1000, "description": "success"}
    ts_start = time.time()
    client = db_connect()

    collection = client[post_data['db_name']][MONGO['customUser']]
    user = collection.find_one({'id':post_data['update']['id']})
    if user['pw'] != post_data['update']['current']:
      client.close()
      return {"code": 1002, "description": "current_pw_not_match"}
    
    x = collection.update_one({'id':post_data['update']['id']}, {'$set': {'pw':post_data['update']['new']}})
    print('result:', x)
    client.close()
    arr_rs['elapsed_time'] = round(time.time() - ts_start, 2)
    return arr_rs
  