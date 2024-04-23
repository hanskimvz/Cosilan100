from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, parse_qsl, uses_params
import os, sys, time
import json

from functions_s import (configVars, dbconMaster, log, TZ_OFFSET)
from query_db import getCountData

port = 9999
document_root = '../vue_codes/dist/'



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

def proc_api(url_parts):
    script_name = url_parts.path.split("/")[-1]
    if script_name == 'query.do':
      body = queryDB(url_parts.query)

    return 'text/json', body.encode()


def queryDB(query):
  # ./api/query.do?fr=dataGlunt&fm=json&labels=undefined&sq=0&st=0&view_by=hour&time_ref=04/22/2024~04/22/2024
  response = {
    "series": [
      {
        "name": "12weeks",
        "data": [17318, 17533, 17011, 14286, 16300, 14629, 15242, 15303, 14481, 13325, 13201, 10547, 10932, 10742, 10182, 10906, 11091, 11639, 12111, 12796, 15229, 15593, 15707, 15118, 15651, 17159, 16572, 15224, 16816, 16655, 16288, 15774, 17089, 15928, 16205, 16125, 12199, 12779, 17427, 19313, 16492, 15135, 16891, 17236, 18272, 17782, 18858, 17643, 17626, 17551, 17663, 18580, 18538, 18906, 18080, 18427, 18297, 18320, 18707, 18576, 18660, 18368, 17126, 17754, 18000, 19165, 18128, 15556, 14425, 16549, 17326, 17455, 18078, 18287, 19064, 18414, 18270, 18319, 18484, 18521, 17802, 17433, 15871, 15358]
      }
    ],
    "xaxis":{
      "type":"datetime",
      "categories": ["2024-01-29","2024-01-30","2024-01-31","2024-02-01","2024-02-02","2024-02-03","2024-02-04","2024-02-05","2024-02-06","2024-02-07","2024-02-08","2024-02-09","2024-02-10","2024-02-11","2024-02-12","2024-02-13","2024-02-14","2024-02-15","2024-02-16","2024-02-17","2024-02-18","2024-02-19","2024-02-20","2024-02-21","2024-02-22","2024-02-23","2024-02-24","2024-02-25","2024-02-26","2024-02-27","2024-02-28","2024-02-29","2024-03-01","2024-03-02","2024-03-03","2024-03-04","2024-03-05","2024-03-06","2024-03-07","2024-03-08","2024-03-09","2024-03-10","2024-03-11","2024-03-12","2024-03-13","2024-03-14","2024-03-15","2024-03-16","2024-03-17","2024-03-18","2024-03-19","2024-03-20","2024-03-21","2024-03-22","2024-03-23","2024-03-24","2024-03-25","2024-03-26","2024-03-27","2024-03-28","2024-03-29","2024-03-30","2024-03-31","2024-04-01","2024-04-02","2024-04-03","2024-04-04","2024-04-05","2024-04-06","2024-04-07","2024-04-08","2024-04-09","2024-04-10","2024-04-11","2024-04-12","2024-04-13","2024-04-14","2024-04-15","2024-04-16","2024-04-17","2024-04-18","2024-04-19","2024-04-20","2024-04-21"],
    }
  }
  return json.dumps(response)


# uses_params.append('scheme')
# url = 'http://192.168.1.252:9999/api/query.do?fr=dashBoard&page=footfall&fm=json&sq=0&st=0&time_ref=04/21/2024'
# # par = urlparse("scheme://some.domain/some/nested/endpoint;param1=value1;param2=othervalue2?query1=val1&query2=val2#fragment")
# par = urlparse(url)
# # ParseResult(scheme='scheme', netloc='some.domain', path='/some/nested/endpoint;param1=value1;param2=othervalue2', params='', query='query1=val1&query2=val2', fragment='fragment')
# print (par)
# sys.exit()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        for i in range(5):
            url = url.replace("//","/")
        url_parts = urlparse(url)
        print(url_parts)
        if url_parts.path.startswith("/api"):
            type_t, body = proc_api(url_parts)
        else:
            type_t, body = proc_web(url_parts)

        self.send_response(200)
        self.send_header('Content-Type', type_t)
        self.end_headers()
        self.wfile.write(body)
        
web_dir = os.path.join(os.path.dirname(__file__), document_root)
os.chdir(web_dir)
httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
print(f'Server running on port:{port}, document_root:', os.getcwd())
httpd.serve_forever()