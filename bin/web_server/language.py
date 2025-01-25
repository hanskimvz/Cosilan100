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

from functions_s import (MONGO, db_connect)

def getLanguagePack(db_name='cnt_demo', action='pack'):
  arr_rs = {
    "eng":{},
    "kor":{},
    "chi":{},
    # "fre":{},
  }
  client = db_connect()
  collection = client[db_name][MONGO['customLanguage']]
  if action == 'pack':
    rows = collection.find()
    for row in rows:
      if not row.get('varstr'):
        continue
      arr_rs['kor'][row['varstr']] = row['kor'] if row.get('kor') else row.get('varstr')
      arr_rs['eng'][row['varstr']] = row['eng'] if row.get('eng') else row.get('varstr')
      arr_rs['chi'][row['varstr']] = row['chi'] if row.get('chi') else row.get('varstr')
  
  elif action == 'list':
    rows = collection.find()
    for row in rows:
      arr_rs.append(row)

  client.close()
#   print(arr_rs)
  return arr_rs
