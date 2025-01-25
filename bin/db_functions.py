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
import threading
from datetime import datetime, date
from functions_s import (MONGO, CONFIG, db_connect,  checkAuthMode, ts_to_tss, message, log)


def getWriteParams():
    arr_cmd = []
    regdate = time.strftime("%Y-%m-%d %H:%M:%S")
    client = db_connect()
    db = client[MONGO['db']]
    collection = {
        'cgis': db[MONGO['commonCgis']],
        'params': db[MONGO['commonDevice']]
    }
    rows = collection['cgis'].find({'flag':True})
    for row in rows:
        dev = collection['params'].find_one({'device_info':row['device_info']})
        if not dev:
            log.error("Retrieve Param faild from %s at %s" %(row['device_info'], regdate))
            client.close()
            return False
        dev_x =client[dev['db_name']][MONGO['customParam']].find_one({'device_info':row['device_info']},{'ip':1, 'port':1, 'user_id':1, 'user_pw':1})   
        if not dev_x:
            log.error("Retrieve Param faild from %s at %s" %(row['device_info'], regdate))
            client.close()
            return False
        dev.update (dev_x)
        arr_cmd.append({'_id':row['_id'], 'ip':dev['ip'], 'port':dev['port'], 'user_id':dev['user_id'], 'user_pw':dev['user_pw'], 'cmd':row['write_cgi_cmd']})

    client.close()
    return arr_cmd

def completeWriteParam(arr_ids):
    client = db_connect()
    db = client[MONGO['db']]
    collection = db[MONGO['commonCgis']]
    collection.update_many({'_id':{'$in':arr_ids}}, {'$set':{'flag':False, 'complete_date':time.strftime("%Y-%m-%d %H:%M:%S")}})
    client.close()
    return True

def convert_to_serializable(obj):
    try:
        if isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return str(obj)
        return obj
        
    except Exception as e:
        print(f"convert_to_serializable error: {str(e)}")
        return str(obj)
    
def updateSimpleParam(device):
    # device_info, usn, url only. for browsing devices
    regdate = time.strftime("%Y-%m-%d %H:%M:%S")
    client = db_connect()
    db = client[MONGO['db']]
    collection = db[MONGO['commonDevice']]
    dev = collection.find_one({'device_info':device['device_info']})
    if dev:
        collection.update_one({'device_info':device['device_info']}, {'$set':{'ip':device['ip'], 'port':device['port'], 'url':device['url'], 'regdate':regdate, 'last_access':regdate, 'method':'active'}})

    else:
        collection.insert_one({'device_info':device['device_info'], 'ip':device['ip'], 'port':device['port'], 'url':device['url'], 'last_access':regdate, 'db_name': 'none', 'method':'active', 'flag':False})

    client.close()

    return False if dev['db_name'] == 'none' else True

def updateParam(param) :
    # if param['db_name'] == 'none':
    #     return False
    regdate = time.strftime("%Y-%m-%d %H:%M:%S")
    if not param.get('ret') :
        log.error("Retrieve Param faild from %s at %s" %(param['device_info'], regdate))
        return False
    # print ('param:', param)
   
    print ("updating param from %s at %s to DB" %(param['device_info'], regdate))

    if not param.get('device_info'):
        param['device_info'] = "mac=%s&brand=%s&model=%s" %(param['mac'], param['brand'], param['model'])
    
    client = db_connect()
    if param.get('db_name') == 'none':
        collection = client[MONGO['db']][MONGO['floatingDevice']]
    else:
        collection = client[param['db_name']][MONGO['customParam']]
    num_records = collection.count_documents({'device_info':param['device_info']})
    if len(param['usn']) >9:
        param['usn'] = param['usn'][:9]
    
    if param.get('authkey'):
        param['authkey'] = convert_to_serializable(param['authkey'])

    if num_records:
        collection.update_one({'device_info':param['device_info']}, {'$set': param})
    else:
        collection.insert_one(param)
    client.close()
    # log.info ("%s update param OK" %device_info)
    # print ("update params from %s at %s" %(device_info, regdate))

    return param


def updateSnapshot(db_name='none', device_info='', snapshot=''):
    if db_name == 'none':
        return False
    regdate = time.strftime("%Y-%m-%d %H:%M:%S")
    strn = "updating snapshot from %s at %s to DB" %(device_info, regdate)
    message(strn)
    log.info(strn)
 
    client = db_connect()
    collection = client[db_name][MONGO['customSnapshot']]
    num_records = collection.count_documents({'device_info':device_info})
    if num_records>1000:
        collection.find_one_and_update(
            {'device_info':device_info},
            {'$set':{'snapshot':snapshot, 'timestamp':int(time.time()), 'regdate':regdate}},
            sort=[('timestamp', 1)]
        )
    else:
        collection.insert_one({'device_info':device_info, 'snapshot':snapshot, 'timestamp':int(time.time()), 'regdate':regdate})
    
    collection = client[db_name][MONGO['customParam']]
    collection.update_one({'device_info':device_info}, {'$set':{'last_ts_snapshot':int(time.time())}})
    client.close()

    return True    

def updateCountReportTenmin(db_name='none',device_info='', arr_crpt=[]):
    if db_name == 'none':
        return False
    regdate = time.strftime("%Y-%m-%d %H:%M:%S")
    strn =  "updating counting report from %s at %s to DB" %(device_info, regdate)
    message(strn)
    log.info(strn)

    client = db_connect()
    db = client[db_name]

    # find device_info, counter_name, counter_label
    arr_label = dict()
    collection = db[MONGO['customDeviceTree']]
    rows = collection.find({'device_info': device_info})
    for row in rows:
        arr_label[row['counter_name']] = row['counter_label'] if row.get('counter_label') else ''
        camera_code = row['camera_code']   if row.get('camera_code')   else ''
        camera_name = row['camera_name']   if row.get('camera_name')   else ''
        store_code  = row['store_code']    if row.get('store_code')    else ''
        store_name  = row['store_name']    if row.get('store_name')    else ''
        square_code = row['square_code']   if row.get('square_code')   else ''
        square_name = row['square_name']   if row.get('square_name')   else ''
    # print (arr_label)
    ts_min = 0xFFFFFFFF
    ts_max = 0
    for crpt in arr_crpt:
        if crpt['timestamp'] < ts_min:
            ts_min = crpt['timestamp']
        if crpt['timestamp'] > ts_max:
            ts_max = crpt['timestamp']        
        crpt['device_info'] = device_info
        crpt['ct_label']    = arr_label[crpt['ct_name']]
        crpt['camera_code'] = camera_code
        crpt['camera_name'] = camera_name
        crpt['store_code']  = store_code
        crpt['store_name']  = store_name
        crpt['square_code'] = square_code
        crpt['square_name'] = square_name
        crpt['status']      = 0
        crpt['year'], crpt['month'], crpt['day'], crpt['hour'], crpt['min'], crpt['wday'], crpt['week'] = ts_to_tss(crpt['timestamp'])
    
    print ('ts_min:%d, ts_max:%d' %(ts_min, ts_max))
        
    collection = db[MONGO['customCount']['tenmin']]
    rows = collection.find({'device_info': device_info, 'timestamp': {'$gte': ts_min}}) 
    
    # rows와 arr_crpt에서 중복 제거
    arr_ts_ct = set()
    for row in rows:
        arr_ts_ct.add("%s_%d_%s" %(row['device_info'], row['timestamp'], row['ct_name']))
    
    # print(arr_ts_ct)
    
    # arr_crpt에서 rows의 timestamp_ct_name와 중복되지 않는 데이터만 arr_record에 추가
    arr_record = []
    for crpt in arr_crpt:
        if not ("%s_%d_%s" %(crpt['device_info'], crpt['timestamp'], crpt['ct_name']) in arr_ts_ct):
            arr_record.append(crpt)
    for arr in arr_record:
        print (arr)
    if arr_record:
        collection = db[MONGO['customCount']['tenmin']]
        try:
            collection.insert_many(arr_record)
            log.info(f"{device_info}: customCount, insert_many OK")
            print (f"{device_info}: {time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ts_min))} ~ {time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ts_max))} customCount, insert_many OK")
        except Exception as e:
            log.error(f"{device_info}: customCount, insert_many failed: {str(e)}")
            print (f"{device_info}: {time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ts_min))} ~ {time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ts_max))} customCount, insert_many failed: {str(e)}")
    
        collection = db[MONGO['customParam']]
        try:
            collection.update_one({'device_info': device_info}, {'$set': {'last_ts_count': ts_max}})
            print (f"{device_info}: customParam, set last_ts_count OK")
        except Exception as e:
            print (f"{device_info}: customParam, set last_ts_count failed: {str(e)}")
            log.error(f"{device_info}: customParam, set last_ts_count failed: {str(e)}")

    client.close()
    return True          



def updateHeatmap(db_name='none', device_info='', arr_hm=[]):
    if db_name == 'none':
        return False
    regdate = time.strftime("%Y-%m-%d %H:%M:%S")
    strn = "updating heatmap reports from %s at %s to DB" %(device_info, regdate)
    message(strn)
    log.info(strn)

    client = db_connect()
    db = client[db_name]

    collection = db[MONGO['customDeviceTree']]
    rows = collection.find_one({'device_info': device_info})
    camera_code = rows['camera_code']   if rows.get('camera_code')   else ''
    camera_name = rows['camera_name']   if rows.get('camera_name')   else ''
    store_code = rows['store_code']    if rows.get('store_code')    else ''
    store_name = rows['store_name']    if rows.get('store_name')    else ''
    square_code = rows['square_code']   if rows.get('square_code')   else ''
    square_name = rows['square_name']   if rows.get('square_name')   else ''

    ts_min = 0xFFFFFFFF
    ts_max = 0
    for hm in arr_hm:
        if hm['timestamp'] < ts_min:
            ts_min = hm['timestamp']
        if hm['timestamp'] > ts_max:
            ts_max = hm['timestamp']

        hm['device_info'] = device_info
        hm['camera_code'] = camera_code
        hm['camera_name'] = camera_name
        hm['store_code']  = store_code
        hm['store_name']  = store_name
        hm['square_code'] = square_code
        hm['square_name'] = square_name
        hm['status']      = 0
        hm['year'], hm['month'], hm['day'], hm['hour'], hm['min'], hm['wday'], hm['week'] = ts_to_tss(hm['timestamp'])

    print ('ts_min:%d, ts_max:%d' %(ts_min, ts_max))

    arr_ts_hm = set()
    collection = db[MONGO['customHeatmap']]
    rows = collection.find({'device_info': device_info, 'timestamp': {'$gte': ts_min}}) 
    for row in rows:
        arr_ts_hm.add("%s_%d" %(row['device_info'], row['timestamp']))
    print (arr_ts_hm)

    arr_record = []
    for hm in arr_hm:
        if not ("%s_%d" %(hm['device_info'], hm['timestamp']) in arr_ts_hm):
            arr_record.append(hm)
    # print (arr_record)

    if arr_record:
        collection = db[MONGO['customHeatmap']]
        try:
            collection.insert_many(arr_record)
            log.info(f"{device_info}: customHeatmap, insert_many OK")
            print (f"{device_info}: {time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ts_min))} ~ {time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ts_max))} customHeatmap, insert_many OK")
        except Exception as e:
            log.error(f"{device_info}: customHeatmap, insert_many failed: {str(e)}")
            print (f"{device_info}: {time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ts_min))} ~ {time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ts_max))} customHeatmap, insert_many failed: {str(e)}")

        collection = db[MONGO['customParam']]
        try:
            collection.update_one({'device_info': device_info}, {'$set': {'last_ts_heatmap': ts_max}})
            print (f"{device_info}: customParam, set last_ts_heatmap OK")
        except Exception as e:
            print (f"{device_info}: customParam, set last_ts_heatmap failed: {str(e)}")
            log.error(f"{device_info}: customParam, set last_ts_heatmap failed: {str(e)}")

    client.close()
    return True   


def getDeviceListFromDB(flag=None):
    arr_dev = []
    client = db_connect()
    collection = client[MONGO['db']][MONGO['commonDevice']]
    rows = collection.find({'method':'active'}) if flag == None else collection.find({'flag': flag})
    
    for row in rows:
        if row.get('db_name') == 'none':
            continue
        collection = client[row['db_name']][MONGO['customParam']]
        dev = collection.find_one({'device_info': row['device_info']})

        if not dev.get('user_id'):
            dev['user_id'] = 'root'
        if not dev.get('user_pw'):
            dev['user_pw'] = 'pass'        
        authkey, devfamily = checkAuthMode(dev['ip'], dev['port'], dev['user_id'], dev['user_pw'])
       
        arr_dev.append({
            "device_info": dev['device_info'],
            "ip": dev['ip'],
            "port": dev['port'],
            "url": dev['url'],
            "db_name": dev['db_name'],
            "user_id": dev['user_id'],
            "user_pw": dev['user_pw'],
            "online": True if devfamily else False,
            "authkey": authkey,
            "device_family": devfamily,
            "flag": dev['flag'] if dev.get('flag') else False,
        })
    client.close()
    return arr_dev

def getDeviceInfoFromDB(db_name, device_info, fields={}):
    client = db_connect()
    collection = client[db_name][MONGO['customParam']]
    
    flags = {f:1 for f in fields }
    rows = collection.find_one({'device_info': device_info}, flags)
    arr_param = rows if rows else {}
    client.close()
    return arr_param


def updateFaceThumnmail(face_dict):
    regdate =  time.strftime("%Y-%m-%d %H:%M:%S")
    dbconn0 = dbconMaster()
    with dbconn0:
        cur = dbconn0.cursor()
        sq = "select device_info from " +  MYSQL['commonParam'] + " where usn=%s and (product_id=%s or url=%s)"
        cur.execute(sq, (face_dict['usn'], face_dict['productid'], face_dict['ip']) )
        row = cur.fetchone()
        if not row :
            msg =  "usn:%s, ip:%s, productid:%s, Device is not registerd" %(face_dict['usn'], face_dict['ip'], face_dict['productid'])
            print (msg)
            log.error(msg)
            return False

        deviceinfo = row[0]
        sq = "select pk from " + MYSQL['commonFace'] + " where (flag = 'n') or (flag_fd='y' and  flag_ud='y' and timestamp < %d) order by timestamp asc limit 1 " %(int(time.time()) - int(configVars('software.mysql.recycling_time'))) 
        cur.execute(sq)
        row = cur.fetchone()

        record = [deviceinfo, regdate, face_dict['timestamp'], face_dict['datetime'], face_dict['img_b64'], face_dict['getstr'][:255], face_dict['eventinfo'][:255]]
        if row:
            record.append(row[0])
            sq = "update " + MYSQL['commonFace'] + " set device_info=%s, regdate=%s, timestamp=%s, datetime=%s, thumbnail=%s, get_str=%s, event_info=%s, age=0, gender='', face_token='',flag = 'y', flag_fd='n', flag_ud='n', flag_fs='n' where pk=%s" 
        else :
            sq = "insert into " + MYSQL['commonFace'] + "(device_info, regdate, timestamp, datetime, thumbnail, get_str, event_info, flag) values(%s, %s, %s, %s, %s, %s, %s, 'y')" 

        log.info(deviceinfo + ": Get Thumnail")
        cur.execute(sq, tuple(record))
        dbconn0.commit()


def updateEventCount(event_rs):
    dbconn0 = dbconMaster()
    with dbconn0:
        cur = dbconn0.cursor()
        sq = "select device_info, db_name from " + MYSQL['commonParam'] + " where url=%s "
        cur.execute(sq, event_rs['ip'])
        deviceinfo, db_name = cur.fetchone()
        if db_name == 'none' or not db_name:
            return False
        sq = "select A.counter_label from %s.%s as A inner join %s.%s as B on A.camera_code=B.code where A.counter_name='%s' and B.device_info='%s'"  %(db_name, MYSQL['customCounterLabel'], db_name, MYSQL['customCamera'], event_rs['ct_name'], deviceinfo)
        # print (sq)
        cur.execute(sq)
        ct_label = cur.fetchone()[0]
        record = [event_rs['ip'], deviceinfo, time.strftime("%Y-%m-%d %H:%M:%S"), event_rs['timestamp'], event_rs['ct_name'], event_rs['ct_val'], event_rs['getstr'][:255], db_name, ct_label]

        sq = "select pk from " + MYSQL['commonCountEvent'] + "  where timestamp < %s order by timestamp asc limit 1 "
        cur.execute(sq, (int(time.time()) - int(configVars('software.mysql.recycling_time'))) )
        row = cur.fetchone()
        if row:
            record.append(row[0])
            sq = "update " + MYSQL['commonCountEvent'] + " set device_ip=%s, device_info=%s, regdate=%s, timestamp=%s, counter_name=%s, counter_val=%s, message=%s, flag='y', status=0, db_name=%s, counter_label=%s where pk = %s"
        else:
            sq = "insert into " + MYSQL['commonCountEvent'] + "(device_ip, device_info, regdate, timestamp, counter_name, counter_val, message, flag, status, db_name, counter_label)  values(%s, %s, %s, %s, %s, %s, %s, 'y', 0, %s, %s) "
        # print (sq, tuple(record))
        cur.execute(sq, tuple(record))
        # log.info("count Event %s, %s, %s, %s, %s, %s" %(tuple(record[:6])))
        # updateRtCounting(dbconn0, db_name)
        dbconn0.commit()


def getDatabaseNames():
    try:
        client = db_connect()
        db_names = client.list_database_names()
        client.close()
        # 시스템 데이터베이스 제외
        db_names = [db for db in db_names if db not in ['admin', 'config', 'local', 'none', 'cnt_common']]
        return db_names
    except Exception as e:
        log.error(f"Failed to get database names: {str(e)}")
        return []

def updateCountReportExt(db_name='none'):

    if db_name == 'none':
        return False
    client = db_connect()
    db = client[db_name]
    collection = {
        'tenmin': db[MONGO['customCount']['tenmin']],
        'hour':   db[MONGO['customCount']['hour']],
        'day':    db[MONGO['customCount']['day']],
        'week':   db[MONGO['customCount']['week']],
        'month':  db[MONGO['customCount']['month']],
        'year':   db[MONGO['customCount']['year']]
    }
    # rows = collection['tenmin'].find({'status':{'$lt':31}}) 
    query = {'status':{'$lt':31}}
    total_record = collection['tenmin'].count_documents(query)
    print (f"total_record: {total_record}")

    batch_size = 1000
    ts_start = time.time()

    rows = collection['tenmin'].find(query).limit(batch_size)
    for row in rows:
        for key, value in row.items():
            if isinstance(value, (int, float)):
                row[key] = int(value)
            if isinstance(value, (datetime, date)):
                row[key] = value.isoformat()

        ts = int(row['timestamp'])
        wflag = int(row['status'])
        # print ('wflag', wflag, row['device_info'], row['datetime'])
        if((wflag & 1) == 0): # count hour
            query = {
                'device_info': row['device_info'],
                'timestamp': ts // 3600 * 3600,
                'ct_name': row['ct_name']
            }
            rt = collection['hour'].find_one(query)
            # print ('hour', rt)
            if rt:
                ret = collection['hour'].find_one_and_update(query, {'$set':{'ct_value':rt['ct_value']+row['ct_value']}})
            else:
                del(row['min'])
                row['timestamp'] = ts//3600*3600
                row['datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(row['timestamp']))
                ret = collection['hour'].insert_one(row)
            if(ret):
                wflag |= 1

        if((wflag & 2) == 0):
            query = {
                'device_info': row['device_info'],
                'timestamp': ts // 86400 * 86400,
                'ct_name': row['ct_name']
            }
            rt = collection['day'].find_one(query)
            # print ('day', rt)
            if rt:
                ret = collection['day'].find_one_and_update(query, {'$set':{'ct_value':rt['ct_value']+row['ct_value']}})
            else:
                del(row['hour'])
                row['timestamp'] = ts//86400*86400
                row['datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(row['timestamp']))
                ret = collection['day'].insert_one(row)
            if(ret):
                wflag |= 2

        if((wflag & 4) == 0):
            query = {
                'device_info':row['device_info'],
                'timestamp':ts//604800*604800,
                'ct_name':row['ct_name']
            }
            rt = collection['week'].find_one(query)
            # print ('week', rt)
            if rt:
                ret = collection['week'].find_one_and_update(query, {'$set':{'ct_value':rt['ct_value']+row['ct_value']}})
            else:
                del(row['day'])
                row['timestamp'] = ts//604800*604800
                row['datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(row['timestamp']))
                row['week'] = int(time.strftime("%U", time.gmtime(row['timestamp'])))
                ret = collection['week'].insert_one(row)
        
            if(ret):
                wflag |= 4

        if((wflag & 8) == 0):
            query = {
                'device_info':row['device_info'],
                'year':row['year'],
                'month':row['month'],
                'ct_name':row['ct_name']
            }
            rt = collection['month'].find_one(query)
            # print ('month', rt)
            if rt:
                ret = collection['month'].find_one_and_update(query, {'$set':{'ct_value':rt['ct_value']+row['ct_value']}})
            else:
                del(row['week'])
                row['timestamp'] = time.mktime(time.strptime(f"{row['year']}-{row['month']}-01 00:00:00", "%Y-%m-%d %H:%M:%S")) + CONFIG['TIMEZONE']['tz_offset']
                row['datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(row['timestamp']))
                ret = collection['month'].insert_one(row)
            
            if(ret):
                wflag |= 8

        if((wflag & 16) == 0):
            query = {
                'device_info':row['device_info'],
                'year':row['year'],
                'ct_name':row['ct_name']
            }
            rt = collection['year'].find_one(query)
            # print ('year', rt)
            if rt:
                ret = collection['year'].find_one_and_update(query, {'$set':{'ct_value':rt['ct_value']+row['ct_value']}})
            else:
                del(row['month'])
                row['timestamp'] = time.mktime(time.strptime(f"{row['year']}-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")) + CONFIG['TIMEZONE']['tz_offset']
                row['datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(row['timestamp']))
                ret = collection['year'].insert_one(row)

            if(ret):
                wflag |= 16

        if(wflag):
            collection['tenmin'].find_one_and_update({'_id':row['_id']}, {'$set':{'status':wflag}})
            wflag = 0
            
    print(f"Processed: {min(batch_size, total_record)}/{total_record}, elapsed: {round(time.time() - ts_start, 2)} secs")

    client.close()
    return True

class thUpdateCountReportExtTimer():
    def __init__(self, t=1800):
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
        db_names = ['cnt_demo']
        for db_name in db_names:
            updateCountReportExt(db_name)

    def start(self):
        self.handle_function()
    
    def is_alive(self):
        return self.thread.is_alive()
    
    def stop(self):
        self.thread.cancel()
        self.thread = None
    
    def restart(self):
        self.stop()
        self.start()
    def get_name(self):
        return self.name
    
    

if __name__ == '__main__':
    # x = getLatestTimestamp( MYSQL['commonCounting'], 'mac=001323A00326&brand=CAP&model=NS602HD' )
    # print(x)
    # x = getLatestTimestamp( MYSQL['commonHeatmap'], 'mac=001323A00326&brand=CAP&model=NS602HD' )
    # print(x)
    # x = getDeviceListFromDB()
    # for xx in x:
    #     print(xx)
    # dbconn0 = dbconMaster()
    # with dbconn0:    
    #     updateRtCounting(dbconn0, 'cnt_demo')
    updateCountReportExt('cnt_demo')    
    # x = getWriteParams()
    # print(x)
    # completeWriteParam([x[0]['_id']])
    # s = getDatabaseNames()
    # print(s)
    sys.exit()