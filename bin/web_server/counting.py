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
import datetime
import pymysql
import json, re, hashlib
from functions_s import (CONFIG, MONGO, db_connect, log)

def getPlaceData(db_name='cnt_demo'):
    print ('getPlaceData', db_name)
    client = db_connect()
    collection = client[db_name][MONGO['customDeviceTree']]
    rows = collection.find()
    arr = {}
    arr_store_code = []
    arr_camear_code = []
    arr_device_info = []
    i = 0
    for row in rows:
        if not row['square_code'] in arr:
            arr[row['square_code']] = {"code":row['square_code'], "name": row['square_name'], "store":[]}
            i+=1
        if not row['store_code'] in arr_store_code:
            arr_store_code.append(row['store_code'])
            arr[row['square_code']]['store'].append({"code": row['store_code'], "name":row['store_name'], "camera":[]})
        if not row['camera_code'] in arr_camear_code:
            arr_camear_code.append(row['camera_code'])
            arr[row['square_code']]['store'][len(arr[row['square_code']]['store'])-1]['camera'].append({"code": row['camera_code'], "name":row['camera_name'], "device_info":[]})
        if not row['device_info'] in arr_device_info:
            arr_device_info.append(row['device_info'])
            arr[row['square_code']]['store'][len(arr[row['square_code']]['store'])-1]['camera'][len(arr[row['square_code']]['store'][len(arr[row['square_code']]['store'])-1]['camera'])-1]['device_info'].append(row['device_info'])


    print (json.dumps(arr, indent=4))
    client.close()
  
#   dbCon = dbconMaster()
#   sq = "select A.code as square_code, A.name as square_name, B.code as store_code, B.name as store_name from " + db_name + "." + MYSQL['customSquare']+" as A inner join " + db_name + "." + MYSQL['customStore'] + " as B on A.code=B.square_code order by A.code asc; "
#   arr = dict()
#   with dbCon:
#     cur = dbCon.cursor(pymysql.cursors.DictCursor)
#     cur.execute(sq)
#     rows = cur.fetchall()
    
#     for row in rows:
#       if not row['square_code'] in arr:
#         arr[row['square_code']] = {"code":row['square_code'], "name": row['square_name'], "store":[]}
#       arr[row['square_code']]['store'].append({"code": row['store_code'], "name":row['store_name']})

  # print (arr)
  # return arr
    arr_data = [arr[r] for r in arr]
    return arr_data