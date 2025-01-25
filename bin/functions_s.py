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
# from http.client import HTTPConnection
from configparser import ConfigParser
import socket
import re, base64, struct
# from urllib.parse import urlparse, parse_qsl, unquote
import threading
import logging, logging.handlers
from pymongo import MongoClient
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import optparse

op = optparse.OptionParser()
op.add_option("-V", "--version", action="store_true", dest="_VERSION")
op.add_option("-D", "--debug-display", action="store_true", dest="_DEBUG_DISPLAY")
op.add_option("-P", "--debug-port", action="store", dest="_MANAGER_PORT")
opt, args = op.parse_args()


def get_config():
	fname = os.path.dirname(os.path.abspath(__file__)) + "/config/config.json"
	if not os.path.isfile(fname):
		print("No config file")
		return None
	with open(fname, 'r') as f:
		return json.load(f)
	
CONFIG = get_config()



def modifyConfig(groupPath, entryValue):
	# 경로를 점(.)으로 분리
	keys = groupPath.split('.')
	print (keys)
	
	fname = os.path.dirname(os.path.abspath(__file__)) + "/config/config.json"
	with open(fname, 'r') as f:
		config = json.load(f)

	current = config
	for i, key in enumerate(keys[:-1]):
		if key not in current:
			current[key] = {}
		current = current[key]
	current[keys[-1]] = entryValue
	print (config)

	with open(fname, 'w') as f:
		json.dump(config, f, indent=4)

def db_connect():
	try:
		# MongoDB 연결 문자열에 authSource 명시적으로 추가
		uri = "mongodb://%s:%s@%s:%s/?authSource=admin" % (
			CONFIG['MONGODB']['user'],
			CONFIG['MONGODB']['password'],
			CONFIG['MONGODB']['host'],
			CONFIG['MONGODB']['port']
		)
		client = MongoClient(uri)
		# 연결 테스트
		client.admin.command('ping')
		return client
	except Exception as e:
		print(f"MongoDB Connection Error: {str(e)}")
		return None


def check_mongodb_users(admin_id, admin_passwd):
	try:
		# MongoDB 연결 (인증 없이)
		client = MongoClient(f"mongodb://{admin_id}:{admin_passwd}@{CONFIG['MONGODB']['host']}:{CONFIG['MONGODB']['port']}/")
		
		# admin 데이터베이스 선택
		admin_db = client.admin
		
		# 사용자 목록 조회
		users = admin_db.command('usersInfo')
		for user in users['users']:
			if user['user'] == CONFIG['MONGODB']['user']:
				client.close()
				return True
		
		# 사용자가 없으면 새로 생성 - 수정된 문법
		admin_db.command(
			'createUser', 
			CONFIG['MONGODB']['user'],
			pwd=CONFIG['MONGODB']['password'],
			roles=[
				{ "role": "readWriteAnyDatabase", "db": "admin" },
			]
		)
		
		# 생성 확인
		users = admin_db.command('usersInfo')
		for user in users['users']:
			if user['user'] == CONFIG['MONGODB']['user']:
				client.close()
				return True        
		client.close()
		return False
		
	except Exception as e:
		print(f"MongoDB 사용자 조회 오류: {str(e)}")
		return None

def test_mongo():
	client = db_connect()
	if not client:
		print("MongoDB 연결 실패")
		return
		
	try:
		db = client["cnt_common"]
		collection = db["testCollection"]
		data = {"name": "Alice", "age": 30, "city": "New York"}
		collection.insert_one(data)
		for doc in collection.find():
			print(doc)
	except Exception as e:
		print(f"MongoDB 작업 오류: {str(e)}")
	finally:
		client.close()

########################### log  ###########################
log = logging.getLogger("startBI")
if not os.path.exists(os.path.dirname(CONFIG['log']['file'])):
	os.makedirs(os.path.dirname(CONFIG['log']['file']))

log.setLevel(logging.INFO)
file_handler = logging.handlers.TimedRotatingFileHandler(filename = CONFIG['log']['file'], when = 'midnight', interval=1, encoding='utf-8')
file_handler.suffix = '%Y%m%d'
log.addHandler(file_handler)
formatter = logging.Formatter("%(levelname)-8s  %(asctime)s %(module)s %(funcName)s %(lineno)s %(message)s %(threadName)s")
file_handler.setFormatter(formatter)


def is_online(ip, port=80):
	#  if port is not 80 ??
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server = (ip, port)
	s.settimeout(1)
	try:
		s.connect(server)
	except Exception as e:
		# print(e)
		s.close()
		return False
	
	s.close()
	return True	


def checkServerStatus():
	if is_online (CONFIG['server']['ip'], CONFIG['server']['port']):
		return True
	return False

def checkAuthMode(dev_ip, dev_port = 80, userid='root', userpw='pass', dev_family=None):
	dev_type= None
	auth = None
	if dev_family == 'IPN':
		return (HTTPBasicAuth(userid, userpw), 'IPN')
	elif dev_family == 'IPAI':
		return (HTTPDigestAuth(userid, userpw), 'IPAI')
	elif dev_family == 'IPE':
		return (HTTPDigestAuth(userid, userpw), 'IPE')
	
	arr_dev = [
		('IPN',  'http://' + dev_ip + ':' + str(dev_port) + '/uapi-cgi/network.cgi'),
		('IPAI', 'http://' + dev_ip + ':' + str(dev_port) + '/cgi-bin/admin/network.cgi'),
		('IPE',  'http://' + dev_ip + ':' + str(dev_port) + '/cgi-bin/admin/tcpstatus.cgi')
	]
	arr_auth = [HTTPBasicAuth(userid, userpw), HTTPDigestAuth(userid, userpw)]
	if not is_online(dev_ip):
		return (auth, dev_type)
	
	for authkey in arr_auth:
		for dev, url in arr_dev:
			try:
				r = requests.get(url,  auth=authkey, timeout=2)
				if int(r.status_code) == 200:
					return authkey, dev
			except Exception as e:
				log.error(url + "," +str(e))
				pass
	return (auth, dev_type)
	# auth,   	dev_type
	# None, 	x		 ==> userid and password are not correct
	# x         None     ==> dev_ip cannot be reachable or not valid device

def active_cgi(dev_ip, authkey='', cgi_str='', port=80):
	url = '%s:%d/%s' %(dev_ip, port, cgi_str)
	url = 'http://'+ url.replace("//", "/").strip()
	print (url)
	try:
		r= requests.get(url , auth=authkey, timeout=10)
	except Exception as e:
		log.error(url + "," + str(e))
		print(url + "," + str(e))
		return False
		
	return r.content

def recv_timeout(conn,timeout=2): 
	# TLSS only since 2022.03.20
	conn.setblocking(0)
	total_data=[]
	data=''
	begin=time.time()
	while 1:
		if total_data and time.time()-begin > timeout:
			break
		elif time.time()-begin > timeout*2:
			break
			
		try:
			data = conn.recv(1024)
			if data:
				total_data.append(data)
				begin=time.time()
			else:
				time.sleep(0.1)
		except:
			pass
	return  b''.join(total_data)

def send_tlss_command(conn, cmd=''):
    length = len(cmd)
    s_num = struct.pack("BBBB", length&0xFF, (length>>8)&0xFF, (length>>16)&0xFF, (length>>24)&0xFF)
    rs = "send_message: length:%d, num:%d, %s" %(length, len(s_num), cmd)
    try:
        conn.send(s_num)
        conn.send(cmd.encode('ascii')) # send byte type
    except:
        pass
    return rs

def recv_tlss_message(conn, timeout=2):
    conn.setblocking(1)
    data_num =  conn.recv(4)
    try: 
        num = int("%02X%02X%02X%02X" %(data_num[3],data_num[2],data_num[1],data_num[0]), 16)
    except:
        num=0

    rs = recv_timeout(conn, timeout)
    return rs

def getUpnpInfo(url, timeout=2) :
	rs = dict()
	url_regex      = re.compile(r"<modelURL>http://[ ]*(.+):(\d+)</modelURL>", re.IGNORECASE)
	usn_regex  = re.compile(r"<serialNumber>(.+)</serialNumber>", re.IGNORECASE)	
	mac_regex  = re.compile(r"<UDN>uuid:((.+))</UDN>", re.IGNORECASE)	
	model_regex    = re.compile(r"<modelName>(.+)</modelName>", re.IGNORECASE)	
	brand_regex    = re.compile(r"<manufacturer>(.+)</manufacturer>", re.IGNORECASE)	
	
	try:
		r = requests.get(url, timeout=timeout)
		# print (r.reason)
		if r.reason != 'OK':
			return False
		rs_t = r.content.decode()
	except Exception as e:
		# print(e)
		return False

	if url_regex.search(rs_t):
		rs['ip']   = url_regex.search(rs_t).group(1)
		rs['port']   = url_regex.search(rs_t).group(2)
		rs['url']   = url_regex.search(rs_t).group(0).replace("<modelURL>", "").replace("</modelURL>", "")
	else:
		rs['ip']   = ''
		rs['port']   = 80
		rs['url']   = ''

	rs['model'] = model_regex.search(rs_t).group(1) if model_regex.search(rs_t) else ''
	rs['brand'] = brand_regex.search(rs_t).group(1) if brand_regex.search(rs_t) else ''
	rs['usn']   = usn_regex.search(rs_t).group(1) if usn_regex.search(rs_t) else ''
	rs['mac']   = mac_regex.search(rs_t).group(2) if mac_regex.search(rs_t) else ''
	rs['mac'] = rs['mac'].replace(':','').strip()

	return rs


def arp_device():
	dev_idx =[]
	try_port = [80, 49152, 49153]
	try_page = ['upnpdevicedesc.xml', 'DigitalSecurityCamera1.xml']
	locations = set()
	if os.name == 'nt':
		cmd = 'arp -a |findstr "00-13-2"'
	else :
		cmd = "arp -n |grep 00:13:2"

	arp_regex = re.compile(r"([0-9.]+)(\s+)([\w:]+)(.+)", re.IGNORECASE)
	p = os.popen(cmd).read()
	p = p.replace("ether",""); 	p = p.replace("-",""); 	p = p.replace(":","")
	# print (p)
	
	lines = p.splitlines()
	for i, line in enumerate(lines):
		regex = arp_regex.search(line)
		if regex:
			location = regex.group(1)
			mac = regex.group(3).upper()
			# print (location, mac)
		else :
			continue

		if not mac.startswith("00132"):
			continue

		if not is_online(location):
			continue
		
		for port in try_port:
			for page in try_page:
				if location in locations :
					continue
				url = 'http://%s:%d/%s' %(location, port, page)
				arr= getUpnpInfo(url,1)
				if not arr:
					continue
				if not mac:
					mac = arr['mac']

				dev_idx.append({"idx":i, "usn" : arr['usn'], "ip":arr['ip'], "port":arr['port'], "url":arr['url'], "mac":mac, "model":arr['model'], "brand":arr['brand']})
				locations.add(location) # add succeeded ip
	
	return dev_idx


def ssdp_device(): # discover upnp devices
	dev_idx =[]
	locations = set()
	body = set()
	ST = 'ssdp:all'
	# ST = 'urn:schemas-upnp-org:device:nvcdevice'
	msg = \
		'M-SEARCH * HTTP/1.1\r\n' \
		'HOST:239.255.255.250:1900\r\n' \
		'ST:' + ST + '\r\n'\
		'MX:2\r\n' \
		'MAN:"ssdp:discover"\r\n' \
		'\r\n'
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	s.settimeout(2)
	try:
		s.sendto(msg.encode('ascii'),('239.255.255.250', 1900))
	except:
		s.close()
		return dev_idx	


	try:
		while True: 
			# buffer size is 1024 bytes
			data, addr = s.recvfrom(1024) 
			# body.add(data.decode('ASCII'))
			body.add(data)

	except socket.error as e:
		s.close()

	if not body: #upnp not working
		return False

# HTTP/1.1 200 OK\r\n
# CACHE-CONTROL: max-age=100\r\n
# DATE: Sat, 05 Sep 2020 12:11:34 GMT\r\n
# EXT:\r\n
# LOCATION: http://192.168.4.173:49152/upnpdevicedesc.xml\r\n
# OPT: "http://schemas.upnp.org/upnp/1/0/"; ns=01\r\n
# 01-NLS: 1246cd92-ef52-11ea-9c79-dc56e6e75747\r\n
# SERVER: Linux/2.6.18_IPNX_PRODUCT_1.1.2-g3532e87a, UPnP/1.0, Portable SDK for UPnP devices/1.8.4\r\n
# X-User-Agent: redsonic\r\n
# ST: urn:schemas-upnp-org:device:nvcdevice\r\n
# USN: uuid:H10A004AD-00:13:24:A0:04:AD::urn:schemas-upnp-org:device:nvcdevice\r\n\r\n'

# HTTP/1.1 200 OK\r\n
# CACHE-CONTROL: max-age=360\r\n
# DATE: Sat, 19 Mar 2022 04:59:43 GMT\r\n
# EXT:\r\n
# LOCATION: http://192.168.132.6/DigitalSecurityCamera1.xml\r\n
# OPT: "http://schemas.upnp.org/upnp/1/0/"; ns=01\r\
# n01-NLS: d6baf0b4-a666-11ec-8f24-d7a4623af24a\r\n
# SERVER: Linux/5.4.61, UPnP/1.0, Portable SDK for UPnP devices/1.6.25\r\n
# X-User-Agent: redsonic\r\n
# ST: urn:schemas-upnp-org:device:DigitalSecurityCamera:1\r\n
# USN: uuid:30623834-3036-6666-3661-0013230b8406::urn:schemas-upnp-org:device:DigitalSecurityCamera:1\r\n\r\n'
	
	url_regex = re.compile(r"location:(.+)\r\n", re.IGNORECASE)
	location_regex = re.compile(r"http://[ ]*(\d+).(\d+).(\d+).(\d+)(.+)", re.IGNORECASE)
	uuid_regex  = re.compile(r"USN: uuid:(.+)::urn:schemas-upnp-org:device:(.+):1", re.IGNORECASE)	
	i=0
	for block in body:
		try:
			block = block.decode('utf-8')
		except:
			continue
		if block.find('ST: urn:schemas-upnp-org:device:DigitalSecurityCamera') <0 and  block.find('ST: urn:schemas-upnp-org:device:nvcdevice') <0:
			continue
		url_result = url_regex.search(block)
		url = url_result.group(1).strip() if url_result else None
		if (not url) or (url in locations) :
			continue

		uuid = uuid_regex.search(block)
		if uuid:
			ex = uuid.group(1).split("-")
			usn = ex[0]
			mac = ''.join(ex.pop().split(':'))

		loc = location_regex.search(url)
		location = loc.group(1) + '.' + loc.group(2) + '.' + loc.group(3) + '.' + loc.group(4) if loc else ''
		if not is_online(location):
			continue
		
		arr = getUpnpInfo(url)
		if not arr:
			print (arr)
			continue
		if not mac:
			mac = arr['mac']		
		if not usn:
			usn = arr['usn']

		dev_idx.append({"idx":i, "usn" : usn, "ip":arr['ip'], "port":arr['port'], "url": arr['url'], "mac":mac, "model":arr['model'], "brand":arr['brand']})
		locations.add(url)
		i+=1
	
	return dev_idx

def list_device() :
	dev_idx = ssdp_device()
	if not dev_idx:
		print ("discover with arp")
		return arp_device()
	return dev_idx

def load_cgis():
	with open (CONFIG['cgis'], "r", encoding="utf8") as f:
		body = f.read()

	return json.loads(body)

def addSlashes(strings):
	if isinstance(strings, bytes):
		try:
			strings = strings.decode("utf-8")
		except :
			strings = strings.decode("utf-16")
	symbols = ["\\", '"', "'", "\0", "$" ]
	for i in symbols:
		if i in strings: 
			strings = strings.replace(i, '\\' + i)
	return strings

def ts_to_tss(ts):
    # tm_year=2021, tm_mon=3, tm_mday=22, tm_hour=21, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=81, tm_isdst=-1
	tss = time.gmtime(ts)
	year = int(tss.tm_year)
	month = int(tss.tm_mon) 
	day = int(tss.tm_mday)
	hour = int(tss.tm_hour)
	min = int(tss.tm_min)
	wday = int((tss.tm_wday+1)%7)
	week = int(time.strftime("%U", tss))

	return (year, month, day, hour, min, wday, week)

def message(strs):
	print (strs)

MONGO = {
	"db": CONFIG['MONGODB']['db'],
    "commonData":     CONFIG['MONGODB']['tables']['common_data'],
	"commonDevice":   CONFIG['MONGODB']['tables']['common_device'],
	"commonCgis":     CONFIG['MONGODB']['tables']['common_cgis'],
	"commonUser":     CONFIG['MONGODB']['tables']['common_user'],
	"floatingUser":   CONFIG['MONGODB']['tables']['floating_user'],
	"floatingDevice": CONFIG['MONGODB']['tables']['floating_device'],

	"customParam":  CONFIG['MONGODB']['tables']['params'],
    "customCount":{
		"tenmin": CONFIG['MONGODB']['tables']['count_tenmin'],
		"hour":   CONFIG['MONGODB']['tables']['count_hour'],
		"day":    CONFIG['MONGODB']['tables']['count_day'],
		"week":   CONFIG['MONGODB']['tables']['count_week'],
		"month":  CONFIG['MONGODB']['tables']['count_month'],
		"year":   CONFIG['MONGODB']['tables']['count_year'],
		"total":  CONFIG['MONGODB']['tables']['count_total'],
    },
	"customSnapshot":     CONFIG['MONGODB']['tables']['snapshot'],
    "customHeatmap":      CONFIG['MONGODB']['tables']['heatmap'],
    "customAgeGender":    CONFIG['MONGODB']['tables']['age_gender'],
    
    "customRtCount":      CONFIG['MONGODB']['tables']['rtscreen'],
    "customDeviceTree":   CONFIG['MONGODB']['tables']['device_tree'],
	"customLanguage":     CONFIG['MONGODB']['tables']['language'],
	"customUser":         CONFIG['MONGODB']['tables']['user'],
	"customWebConfig":    CONFIG['MONGODB']['tables']['web_config'],
}

CGIS = load_cgis()

if __name__ == '__main__':

	# print(CONFIG)
	# test_mongo()
	# check_mongodb_users('hanskim', 'wjdtjd')
	# test_mongo()
	# devlist = list_device()
	# for dev in devlist:
	# 	print(dev)

	# print(MYSQL)
	# print(CGIS)
	
	# modifyConfig("goal", {"a":1, "b":2})

	client = db_connect()
	collection = client[MONGO['db']][MONGO['commonDevice']]
	total_records = collection.count_documents({'device_info':'mac=00132307A2EF&brand=CAP&model=KPN2102HD'})
	print(total_records	   )
	# collection.insert_one({'device_info':'mac=00132307A2EF&brand=CAP&model=KPN2102HD', 'usn':'D3007A2EF', 'url':'192.168.3.18'})
	rows = collection.find({})
	for row in rows:
		print(row)








