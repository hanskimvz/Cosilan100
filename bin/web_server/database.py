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
from functions_s import (CONFIG, MONGO, db_connect, log)
from bson.objectid import ObjectId

def queryDatabase(post_data): # using post data
    print (post_data)
    ts_start = time.time()
    arr_rs = {"total_records":0, "fields": [], "data":[]}

    if not post_data.get('table'):
        return {"code": 1002, "description": "no_table"}

    client = db_connect()
    collection = client[post_data['db_name']][post_data['table']]

    
    # 기존 필터와 결합

    print(post_data['filter'])
        
    if post_data.get('fields'):
        rows = collection.find(post_data['filter'], post_data['fields'])
    else:
        rows = collection.find(post_data['filter'])

    # if post_data.get('sort'):
    #     sort_option = post_data.get('sort', {})
    #     rows = collection.find(post_data['filter']).sort(list(sort_option.items()))
    # else:
    #     rows = collection.find(post_data['filter'])
    if post_data.get('sort'):
        rows = rows.sort(list(post_data['sort'].items()))

    for row in rows:
        row['_id'] = str(row['_id'])
        for key, value in row.items():
            if isinstance(value, (datetime.datetime, datetime.date)):
                row[key] = value.isoformat()
            if isinstance(value, ObjectId):
                row[key] = str(value)
            if isinstance(value, bytes):
                row[key] = value.decode('utf-8')
        arr_rs['data'].append(row)
    
    client.close()
    arr_rs['total_records'] = len(arr_rs['data'])
    if arr_rs['total_records'] > 0:
        arr_rs['fields'] = list(arr_rs['data'][0].keys())
    arr_rs['elapsed_time'] = round(time.time() - ts_start, 2)

    print(f"queryDatabase, arr_rs: {arr_rs}")
    return arr_rs

def updateDatabase(post_data):
    print('updateDatabase', post_data)
    arr_rs = {"code": 1000, "description": "success"}
    ts_start = time.time()
    if not post_data.get('table'):
        return {"code": 1002, "description": "no_table"}
    if not post_data.get('update'):
        return {"code": 1002, "description": "no_update"}
    
    client = db_connect()
    collection = client[post_data['db_name']][post_data['table']]
    if '_id' in post_data['filter'] and isinstance(post_data['filter']['_id'], str):
        post_data['filter']['_id'] = ObjectId(post_data['filter']['_id'])

    if len(post_data['update']) > 1:
        x = collection.update_many(post_data['filter'], {'$set': post_data['update']})
    else:
        x = collection.update_one(post_data['filter'], {'$set': post_data['update']})
    print('결과:', x)
    client.close()
    arr_rs['elapsed_time'] = round(time.time() - ts_start, 2)
    return arr_rs

def insertDatabase(post_data):
    print(post_data)
    arr_rs = {"code": 1000, "description": "success"}
    ts_start = time.time()
    client = db_connect()
    collection = client[post_data['db_name']][post_data['table']]
    x = collection.insert_one(post_data['update'])
    print('result:', x)
    client.close()
    arr_rs['elapsed_time'] = round(time.time() - ts_start, 2)
    return arr_rs


def update_one(self, table, filter_dict, update_dict):
    # _id가 문자열로 전달된 경우 ObjectId로 변환
    if '_id' in filter_dict and isinstance(filter_dict['_id'], str):
        filter_dict['_id'] = ObjectId(filter_dict['_id'])
        
    collection = self.db[table]
    return collection.update_one(filter_dict, {'$set': update_dict})

if __name__ == "__main__":
    post_data = {
        "db_name": "cnt_demo",
        "table": "device_tree",
        "filter": {}
    }
    print(queryDatabase(post_data))
