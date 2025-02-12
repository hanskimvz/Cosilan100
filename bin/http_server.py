# Copyright (c) 2024, Hans kim(hanskimvz@gmail.com)

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


import os, sys, time
import json, hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from functions_s import (CONFIG)
from web_server.proc_api import proc_api
from web_server.users import checkUserseq

HTTP_PORT = CONFIG['HTTP_SERVER']['port']
HTTP_HOST = CONFIG['HTTP_SERVER']['host']


def proc_web(url_parts):
    path =  url_parts.path
    if url_parts.path == '/':
        path = '/index.html'
    
    ext = path.split(".")[-1]
    if ext == 'html' or ext == 'htm':
        type_t = 'text/html'
    elif ext == 'js':
        type_t = 'text/javascript'
    elif ext =='css':
        type_t = 'text/css'
    elif ext == 'ico':
        type_t = 'image/x-icon'
    elif ext == 'png':
        type_t = 'image/png'
    elif ext == 'jpg':
        type_t = 'image/jpeg'
    elif ext == 'json':
        type_t = 'text/json'
    else :
        type_t = 'text/html'
        path = '/index.html'
        print ('Unknown', path)

    with open(path[1:], "rb") as f:
        body = f.read()

    return type_t, body

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    url = self.path
    for i in range(5):
        url = url.replace("//","/")
    url_parts = urlparse(url)
    print('get', url_parts)    

    if url_parts.path.startswith("/api"):
      type_t, body = proc_api(url_parts)
    else:
      type_t, body = proc_web(url_parts)

    self.send_response(200)
    self.send_header('Content-Type', type_t)
    self.end_headers()
    self.wfile.write(body)
        
  def do_POST(self):
    url = self.path
    for i in range(5):
        url = url.replace("//","/")
    url_parts = urlparse(url)
    print('post', url_parts)
    body = b''
    chk_user = checkUserseq(self.headers)
    print("cheked user", chk_user)

    content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
    post_data = self.rfile.read(content_length) # <--- Gets the data itself
    arr_post = json.loads(post_data)


    if url_parts.path.startswith("/api/login") :
      type_t, body = proc_api(url_parts, arr_post)

    elif url_parts.path.startswith("/api"):
        if chk_user:
          type_t, body = proc_api(url_parts, arr_post)
        else :
          type_t, body = 'text/json', json.dumps({'code': 403, 'message':'Unauthorized'}).encode()
    else :
      type_t, body = 'text/json', json.dumps({'code': 404, 'message':'Not found'}).encode()

    self.send_response(200)
    self.send_header('Content-Type', type_t)
    self.end_headers()
    self.wfile.write(body)


# print ("rootdir", _ROOT_DIR)

# web_dir = os.path.join(os.path.dirname(__file__), document_root)
# os.chdir(web_dir)
httpd = HTTPServer((HTTP_HOST, HTTP_PORT), SimpleHTTPRequestHandler)
print(f'Server running on port:{HTTP_PORT}, document_root:', os.getcwd())
httpd.serve_forever()

print ('end')