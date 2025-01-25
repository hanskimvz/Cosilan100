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

import json
from functions_s import (db_connect, MONGO)


def getWebConfig(db_name='cnt_demo', page = 'main'):
  ex_page = page.split(":")
  client = db_connect()
  collection = client[db_name][MONGO['customWebConfig']]

  if ex_page[0] == 'main' or ex_page[0] == 'admin':
    query = {
        '$and': [
            {'$or': [
                {'page': ex_page[0]},
                {'page': 'logo'}
            ]},
            {'flag': 'y'}
        ]
    }
  else:
    query = {
        'page': ex_page[0],
        'flag': 'y'
    }

  arr = {}
  rows = collection.find(query)
  for row in rows:
    if row['page'] == 'logo':
      arr['logo'] = row['body']
    else:
      arr['body'] = json.loads(row['body'])

  client.close()
#   print(arr)
  return arr

  ex_page = page.split(":")
  sq = "select page, body from " + db_name + "." + MYSQL['customWebConfig']; 
  if ex_page[0] == 'main' or ex_page[0] == 'admin':
    sq += " where (page='" + ex_page[0] + "' or page='logo') and flag='y'"
  else:
    sq += " where page='" + ex_page[0] + "' and flag='y'"

  # print (sq)
  dbCon = dbconMaster()
  arr = {}
  with dbCon:
    cur = dbCon.cursor(pymysql.cursors.DictCursor)
    cur.execute(sq)
    rows = cur.fetchall()
    for row in rows:
      # print (row)
      if row['page'] == 'logo':
        arr['logo'] = row['body']
      else:
        arr['body'] = json.loads(row['body'])
  
  # print (arr)
  if len(ex_page) >1:
    for p in arr['body']:
      if p['page'] == ex_page[1]:
        return p

  return arr