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
import base64
import threading

from functions_s import (CONFIG, active_cgi, list_device, log, CGIS, message, addSlashes, checkAuthMode)
from parse_functions import (parseParam, parseCountReport, parseHeatmapData)
from db_functions import (updateSimpleParam, updateParam, updateSnapshot, updateCountReportTenmin, updateHeatmap, getDeviceListFromDB, getDeviceInfoFromDB, getWriteParams, completeWriteParam)

def writeParam():
    arr_cmd = getWriteParams()
    arr_ids = []
    for cmd in arr_cmd:
        authkey, dev = checkAuthMode(cmd['ip'], cmd['port'], cmd['user_id'], cmd['user_pw'], cmd['device_family'])
        ret = active_cgi(cmd['ip'], authkey, cmd['cmd'], cmd['port'])
        if ret:
            arr_ids.append(cmd['_id'])
        else:
            log.error(cmd['ip'] + " write param failed")
    if arr_ids:
        completeWriteParam(arr_ids)

def getParam(device_ip=None, port=80, authkey=None,  device_family='IPN'):
    if not device_family:
        return False
    data = b''
    for cgi in CGIS["query_device"]["param"][device_family]:
        rs = active_cgi(device_ip, authkey, cgi.strip(), port)
        if rs:
            data += rs

    data = data.replace(b"Brand.prodshortname", b"BRAND.Product.shortname")
    return (parseParam(data))

def getSnapshot(device_ip=None, port=80, authkey=None, device_family='IPN', format='b64'):
    if not device_family:
        return False    
    # cgi_str = arr_cgi_str["snapshot"][device_family]
    data = active_cgi(device_ip, authkey, CGIS["query_device"]["snapshot"][device_family], port)
    if format == 'b64':
        data = b'data:image/jpg;base64,' + base64.b64encode(data)
        data = addSlashes(data.decode('utf-8'))
    return data

def getCountReport(device_ip=None, port=80, authkey=None,  device_family='IPN', from_t='2022/01/01', to_t='now'):
    if not device_family:
        return False 
    cgi_str = CGIS["query_device"]["countreport"][device_family].replace("_FROM_T_", from_t).replace("_TO_T_", to_t)
    data = active_cgi(device_ip, authkey, cgi_str, port)
    if not data or data.find(b"Not enough data") >0 :
        return []
    data = data.replace(b'Time:', b'Records:')
    return (parseCountReport(data))

def getHeatmap(device_ip=None, port=80, authkey=None,  device_family='IPN', from_t='2022-01-01', to_t='now'):
    if not device_family:
        return False
    # if not arr_cgi_str["heatmap"][device_family]:
    if not CGIS["query_device"]["heatmap"][device_family]:
        return False

    # cgi_str = arr_cgi_str["heatmap"][device_family] %(from_t, to_t)
    data = active_cgi(device_ip, authkey, CGIS["query_device"]["heatmap"][device_family] %(from_t, to_t), port)
    if data.find(b"Not enough data") >0 :
        return []
    return (parseHeatmapData(data))

def testGetFunctions(dev_ip, userid, userpw):
    authkey, dev = checkAuthMode(dev_ip, 80, userid, userpw)
    print (authkey, dev)
    # param = getParam(device_ip=dev_ip, port=80, device_family=dev, authkey= authkey)
    # print (param)
    # snapshot = getSnapshot(device_ip=dev_ip, port=80, device_family=dev, authkey= authkey, format='b64')
    # print (snapshot)
    crpt = getCountReport(device_ip=dev_ip, port=80, authkey=authkey,  device_family=dev, from_t='2022/01/01', to_t='now')
    print (crpt)
    # hm = getHeatmap(device_ip=dev_ip, port=80, authkey=authkey,  device_family=dev, from_t='2022-01-01', to_t='now')
    # print(hm)

# testGetFunctions("192.168.3.10", "root", "pass")
# sys.exit()


def setDatetimeToDevice(device_ip=None, port=80, authkey=None,  device_family='IPN'):
    if not device_family:
        return False      
    # if not set_datetime_str["read"][device_family]:
    if not CGIS['datetime']['read'][device_family]:
        return False
    # cgi_str = set_datetime_str["read"][device_family]
    data = active_cgi(device_ip, authkey, CGIS['datetime']['read'][device_family], port)
    arr = dict()
    for line in data.splitlines():
        sp_line = line.split(b"=")
        if len(sp_line) <2:
            print (line)
            continue
        arr[sp_line[0].decode().lower().strip()] = sp_line[1].decode().lower().strip()

    # if arr.get('system.datetime.tz.name') != _TZ_NAME.lower().strip():
    #     print ("setting timezone")
    #     for tzname, desc, posixrule in CGIS['datetime']['timezone']:
    #         if tzname.lower().strip() == _TZ_NAME.lower().strip():
    #             break
        
    #     print (tzname, desc, posixrule)
    #     for cgi_str in CGIS['datetime']['set_tz'][device_family]:
    #         if (cgi_str.find("name=")) >0:
    #             cgi_str = cgi_str %tzname
    #         elif (cgi_str.find("posixrule=") >0):
    #             cgi_str = cgi_str %posixrule
    #         x = active_cgi(device_ip, authkey, cgi_str, port)
    #         print (x)
    #     time.sleep(2)

    x = active_cgi(device_ip, authkey, CGIS['datetime']['set_datetime'][device_family] %(time.strftime("%m%d%H%M%Y.%S")), port)
    print (x)
    log.info("%s: Setting datetimezone OK" %device_ip)

def testSetDatetime(dev_ip, userid, userpw) :
    authkey, dev = checkAuthMode(dev_ip, userid, userpw)
    setDatetimeToDevice(dev_ip, port=80, authkey=authkey,  device_family=dev)

# testSetDatetime("192.168.219.20", "root", "pass" )
# sys.exit()

def searchDeviceToDB():
# {'idx': 0, 'usn': 'HA0A0073A', 'url': 'http://192.168.1.58:49152/upnpdevicedesc.xml', 'location': '192.168.1.58', 'mac': '001323A0073A', 'model': 'NS202HD', 'brand': 'CAP'}
    arr_dev = list_device()
    regdate = time.strftime("%Y-%m-%d %H:%M:%S")
    
    for dev in arr_dev:
        if not (dev['mac'] and dev['brand'] and dev['model']) :
            msg = "device_info Error mac:%s, brand:%s, model:%s " %(dev['mac'], dev['brand'], dev['model'])
            log.warning (msg)
            message (msg)
            continue

        message(dev)
        dev['device_info'] = "mac=%s&brand=%s&model=%s" %(dev['mac'], dev['brand'], dev['model'])
        # dev['regdate'] = regdate
        dev['last_access'] = regdate
        updateSimpleParam(dev)
        
    strn = "browsing  %d devices and info to db succeed" %len(arr_dev)
    message (strn)
    log.info(strn)

    return True

def procActive():
    n = 0
    arr_dev = getDeviceListFromDB()
    print('arr_dev', arr_dev)
    for dev in arr_dev:
        print()
        if not dev['online']:
            print('not online', dev['device_info'], dev['ip'])
            continue
        # if dev.get('db_name') and dev.get('db_name') == 'none':
        #     print('db_name is none', dev)
        #     continue

        if not ( dev['authkey'] and dev['device_family']):
            strn = "%s: No authkey or device family" %dev['ip']
            message(strn)
            log.info(strn)
            continue
        
        # print('dev', dev)
        # try:
        # (device_info=dev['device_info'], device_ip=dev['ip'], port=80, authkey=dev['authkey'],  device_family=dev['device_family'])

        # except Exception as e:
        #     msg = "fail to write params: {0}".format(str(e))
        #     message(msg)
        #     log.error(msg)
        
        # if CONFIG['set_date_flag']:
        #     setDatetimeToDevice(device_ip=dev['ip'], port=80, authkey=dev['authkey'], device_family=dev['device_family'])
        param = dev.copy()
        param_data = getParam(device_ip=dev['ip'], port=int(dev['port']), authkey=dev['authkey'], device_family=dev['device_family'])
        if param_data:  # param_data가 False가 아닐 때만 업데이트
            param.update(param_data)
            param['snapshot'] = getSnapshot(device_ip=dev['ip'], port=int(dev['port']), authkey=dev['authkey'], device_family=dev['device_family'], format='b64')
            if param:
                updateParam(param)
            else:
                log.error(dev['ip'] + " param retrieve wrong")
        else:
            log.error(dev['ip'] + " failed to get parameters")

        
        print(dev)
        if not dev.get('db_name') or dev.get('db_name') == 'none':
            continue

        # dev.update(
        #     getDeviceInfoFromDB(dev['db_name'], dev['device_info'], fields=['device_info', 'authkey', 'heatmap', 'countrpt', 'enable_snapshot', 'enable_countrpt', 'enable_heatmap', 'user_id', 'user_pw', 'last_ts_count', 'last_ts_heatmap', 'last_ts_snapshot'])
        # )
        # {'_id': ObjectId('67814a73a1513313da4f0047'), 'device_info': 'mac=001323A00324&brand=CAP&model=IPN3102HD', 'db_name': 'cnt_demo', 'flag': False, 'last_access': '2025-01-11 01:27:31', 'ip': '192.168.3.18', 'port': '80', 'regdate': '2025-01-26 02:22:17', 'url': '192.168.3.18', 'method': '', 'user_id': 'root', 'user_pw': 'pass', 'online': True, 'authkey': <requests.auth.HTTPBasicAuth object at 0x7fda10edda00>, 'device_family': 'IPN', 'usn': 'G90A00324', 'brand': 'CAP', 'productid': 'B006', 'model': 'IPN3102HD', 'mac': '001323A00324', 'ip4mode': 'static', 'ip4address_dhcp': None, 'ip4address': '192.168.3.18', 'lic_pro': 'y', 'lic_count': 'n', 'lic_surv': 'n', 'heatmap': 'n', 'countrpt': 'n', 'macsniff': 'n', 'face_det': 'n', 'ret': True, 'dhcp_ip': '0.0.0.0', 'last_ts_count': 0.0, 'enable_countrpt': 'y', 'enable_heatmap': 'y', 'enable_snapshot': 'y', 'last_ts_snapshot': 1737830858}
        
        if dev.get('countrpt')=='y' and dev.get('enable_countrpt') == 'y':
            last_ts_count = dev['last_ts_count'] if dev.get('last_ts_count') else 0
            from_t = time.strftime("%Y/%m/%d%%20%H:%M", time.gmtime(last_ts_count))
            to_t = time.strftime("%Y/%m/%d%%20%H:%M", time.gmtime(int(time.time())//600*600 + int(CONFIG['TIMEZONE']['tz_offset'])))
            readflag = int(time.time()) + int(CONFIG['TIMEZONE']['tz_offset']) - last_ts_count
            print(from_t, to_t, readflag)

            if readflag > 600:
                dev['authkey'], dev['device_family'] = checkAuthMode(dev['ip'], int(dev['port']), dev['user_id'], dev['user_pw'], dev['device_family'])
                crpt = getCountReport(dev['ip'], int(dev['port']), dev['authkey'], dev['device_family'], from_t, to_t)
                if crpt:
                    updateCountReportTenmin(db_name=dev['db_name'], device_info=dev['device_info'], arr_crpt=crpt)
                else :
                    log.error(dev['ip'] + "CRTP is bool or wrong")

        if dev.get('enable_snapshot') == 'y':
            last_ts_snapshot = dev['last_ts_snapshot'] if dev.get('last_ts_snapshot') else 0
            if int(time.time()) + int(CONFIG['TIMEZONE']['tz_offset']) - last_ts_snapshot >= 3600:
                if param.get('snapshot'):
                    updateSnapshot(db_name=dev['db_name'], device_info=dev['device_info'], snapshot=param['snapshot'])
                else:
                    log.error(dev['ip'] + " snapshot data not available")

        if dev.get('heatmap') == 'y' and dev.get('enable_heatmap') == 'y':
            last_ts_heatmap = dev['last_ts_heatmap'] if dev.get('last_ts_heatmap') else 0
            from_t = time.strftime("%Y/%m/%d%%20%H:%M", time.gmtime(last_ts_heatmap))
            to_t = time.strftime("%Y/%m/%d%%20%H:%M", time.gmtime(int(time.time())//3600*3600 + int(CONFIG['TIMEZONE']['tz_offset'])))

            if int(time.time()) + int(CONFIG['TIMEZONE']['tz_offset']) - last_ts_heatmap >= 3600:
                dev['authkey'], dev['device_family'] = checkAuthMode(dev['ip'], int(dev['port']), dev['user_id'], dev['user_pw'], dev['device_family'])
                hm = getHeatmap(device_ip=dev['ip'], port=80, authkey=dev['authkey'], device_family=dev['device_family'], from_t=from_t, to_t=to_t)
                if hm:
                    updateHeatmap(db_name=dev['db_name'], device_info=dev['device_info'], arr_hm=hm)
                else :
                    log.error(dev['ip'] + "Heatmap is bool or wrong")

        

        n+=1

    # if set_date_flag:
    #     modifyConfig('software.status.datetime_sync', int(time.time()))
    #     set_date_flag = False

    return n


class thActiveCountingTimer():
    def __init__(self, t=60):
        self.name = "active_count"
        self.t = t
        self.last = 0
        self.i = 0
        self.thread = threading.Timer(1, self.handle_function)

    def handle_function(self):
        self.main_function()
        self.last = int(time.time())
        self.thread = threading.Timer(self.t, self.handle_function)
        self.thread.start()
    
    def main_function(self):
        ts = time.time()
        str_s = "======== Active Counting, starting %d ========" %self.i
        log.info (str_s)
        message (str_s)
        # every 1 minute
        writeParam()
        searchDeviceToDB()

        n = procActive()

        te = time.time()
        # self.t = 300 - int(te - ts) 
        # if self.t  < 0:
        #     self.t  = 1
        str_s = "Online %d, elaspe time: %d, need %d sec sleep" %(n, (te-ts), self.t )
        message (str_s)
        log.info(str_s)
        
        self.i += 1

    def start(self):
        str_s = "starting Active Counting Service"
        message(str_s)
        log.info (str_s)
        self.last = int(time.time())
        self.thread.start()

    def is_alive(self):
        if int(time.time()) - self.last > 600 :
            return False
        return True
    
    def cancel(self):
        str_s = "stopping Active Counting Servce"
        message(str_s)
        log.info (str_s)
        self.thread.cancel()
    
    def stop(self):
        self.cancel()

if __name__ == '__main__':
    # searchDeviceToDB()
    # print(getDeviceListFromDB())
    # import json
    # with open('sample_arr_crpt.js', 'r') as f:
    #     arr_crpt = json.loads(f.read())
    # print (arr_crpt)
    # updateCountReportTenmin(db_name='cnt_demo',device_info='mac=001323A00322&brand=CAP&model=IPN3502HDIR', arr_crpt=arr_crpt)
    procActive()
    # tc = thActiveCountingTimer()
    # tc.start()
    # while True:
    #     time.sleep (100)
    
