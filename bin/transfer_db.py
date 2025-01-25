import time
import pymysql
import pymongo
import json
from datetime import datetime, date

CONFIG = {
    'MYSQL': {
        'host': '192.168.1.250',
        'user': 'rt_user',
        'password': '13579',
        'port': 3306,
        'charset': 'utf8mb4',
        'common_db': 'common',
        'database': 'cnt_demo'
    },
    'MONGODB': {
        'host': '192.168.1.250',
        'port': 5090,
        'user': 'ct_user',
        'password': '13579',
        'common_db': 'cnt_common',
        'database': 'cnt_demo'
    },
    'TIMEZONE': {
        'tz_offset': 3600*9
    }
}

def connect_mysql():
    """MySQL 연결"""
    try:
        conn = pymysql.connect(
            host=CONFIG['MYSQL']['host'],
            user=CONFIG['MYSQL']['user'],
            password=CONFIG['MYSQL']['password'],
            db=CONFIG['MYSQL']['database'],
            charset='utf8mb4'
        )
        return conn
    except Exception as e:
        print(f"MySQL 연결 실패: {str(e)}")
        return None

def connect_mongodb():
    """MongoDB 연결"""
    try:
        client = pymongo.MongoClient(f"mongodb://{CONFIG['MONGODB']['user']}:{CONFIG['MONGODB']['password']}@{CONFIG['MONGODB']['host']}:{CONFIG['MONGODB']['port']}/")
        return client
    except Exception as e:
        print(f"MongoDB 연결 실패: {str(e)}")
        return None

def transfer_table(table_name, batch_size=1000):
    """MySQL 테이블을 MongoDB로 이전"""
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    mongo_client = connect_mongodb()
    if not mongo_client:
        mysql_conn.close()
        return False

    try:
        # MySQL 커서 생성
        with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 전체 레코드 수 확인
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            total_records = cursor.fetchone()['count']
            
            # MongoDB 컬렉션 선택
            db = mongo_client[CONFIG['MONGODB']['database']]
            collection = db[table_name]
            
            # 배치 처리
            for offset in range(0, total_records, batch_size):
                cursor.execute(f"SELECT * FROM {table_name} LIMIT {offset}, {batch_size}")
                records = cursor.fetchall()
                
                # datetime과 date 객체를 ISO 형식 문자열로 변환
                for record in records:
                    for key, value in record.items():
                        if isinstance(value, (datetime, date)):
                            record[key] = value.isoformat()
                
                if records:
                    collection.insert_many(records)
                
                print(f"처리됨: {min(offset + batch_size, total_records)}/{total_records}")
                
        print(f"테이블 {table_name} 이전 완료")
        return True

    except Exception as e:
        print(f"이전 중 오류 발생: {str(e)}")
        return False

    finally:
        mysql_conn.close()
        mongo_client.close()


def transfer_users():
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    mongo_client = connect_mongodb()
    if not mongo_client:
        mysql_conn.close()
        return False

    try:
        # sq = "select A.regdate, A.code, A.ID, A.email, A.passwd, A.db_name, A.flag, A.role, B.name, B.name_eng, B.telephone, B.address, B.address_b, B.date_in, B.date_out, B.comment from common.users as A inner join cnt_demo.users as B on A.code=B.code"

        sq = "select A.regdate, A.code, A.ID as id, A.email, A.passwd as pw, A.db_name, A.flag, A.role, B.name, B.name_eng, B.telephone, concat(B.address,' ', B.address_b) as address, B.date_in, B.date_out, B.comment from common.users as A  left join cnt_demo.users as B on A.code=B.code"
        with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("show databases")
            rows = cursor.fetchall()
            print (rows)

           
            cursor.execute(sq)
            rows = cursor.fetchall()
            # print (rows)

            arr_mysql = {}
            arr_route = []
            for row in rows:
                for key, value in row.items():
                    if isinstance(value, (datetime, date)):
                        row[key] = value.isoformat()
                    if isinstance(value, (int, float)):
                        row[key] = int(value)
                if not row['db_name'] in arr_mysql:
                    arr_mysql[row['db_name']] = []

                arr_mysql[row['db_name']].append(row)
                arr_route.append({'id':row['id'], 'db_name':row['db_name']})

            print (arr_mysql)
            print (arr_route)

            db = mongo_client[CONFIG['MONGODB']['common_db']]    
            collection = db['user_route']

            arr_mongo = []
            for row in arr_route:
                x = collection.find_one(row)
                if not x:
                    arr_mongo.append(row)

            t = collection.insert_many(arr_mongo)   
            print (t)

            db = mongo_client[CONFIG['MONGODB']['database']]    
            collection = db['users']

            arr_mongo = []
            for row in arr_mysql['cnt_demo']:
                x = collection.find_one(row)
                if not x:
                    arr_mongo.append(row)

            t = collection.insert_many(arr_mongo)   
            print (t)



            return True

    except Exception as e:
        print(f"error: : {str(e)}")
        return False

    finally:
        mysql_conn.close()
        mongo_client.close()

def transfer_camera_params():
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    mongo_client = connect_mongodb()
    if not mongo_client:
        mysql_conn.close()
        return False

    try:
        sq = "select A.device_info as device_info, A.usn as usn, A.product_id as productid, A.lic_pro as lic_pro, A.lic_surv as lic_surv, A.lic_count as lic_count, A.face_det as face_det, A.heatmap as heatmap, A.countrpt as countrpt, A.macsniff as macsniff, A.initial_access as initial_access, A.last_access as last_access, A.db_name as db_name, A.param as param, A.url as url, A.method as method, A.user_id as user_id, A.user_pw as user_pw, B.body as snapshot from common.params as A inner join common.snapshot as B on A.device_info=B.device_info"

        with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sq)
            rows = cursor.fetchall()
            arr_mysql = []
            for row in rows:
                dev = row['device_info'].split('&')
                row['ip'] = row['url']
                row['port'] = 80
                row['device_family'] = 'IPN'
                row['flag'] = False
                row['usn'] = row['usn']
                row['mac'] = dev[0].split("=")[1]
                row['brand'] = dev[1].split("=")[1]
                row['model'] = dev[2].split("=")[1]
                row['ip4mode'] = 'static'
                row['ip4address_dhcp'] = None
                for key, value in row.items():
                    if isinstance(value, (datetime, date)):
                        row[key] = value.isoformat()
                    if isinstance(value, (int, float)):
                        row[key] = int(value)
                    # if key=='param' or key=='snapshot':
                    #     row[key] = ''
                print (row)

                if row['db_name'] != 'none':
                    sqx = "select enable_countingline as enable_countrpt, enable_heatmap as enable_heatmap, enable_macsniff as enable_macsniff, enable_face_det as enable_face_det from " + row['db_name'] + ".camera where device_info='" + row['device_info'] + "'"
                    cursor.execute(sqx)
                    rowx = cursor.fetchall()
                    for r in rowx:
                        row['enable_countrpt'] = r['enable_countrpt']
                        row['enable_heatmap'] = r['enable_heatmap']
                        row['enable_macsniff'] = r['enable_macsniff']
                        row['enable_face_det'] = r['enable_face_det']

                    
                arr_mysql.append(row)

            print (arr_mysql)

            db = mongo_client[CONFIG['MONGODB']['common_db']]    
            collection = db['device_route']
            for row in arr_mysql:
                dev_filter = {'device_info':row['device_info']}
                x = collection.find_one(dev_filter)
                if not x:
                    collection.insert_one({'device_info':row['device_info'], 'db_name':row['db_name']})

            for row in arr_mysql:
                if row['db_name'] == 'none':
                    continue
                collection = mongo_client[row['db_name']]['params']
                dev_filter = {'device_info':row['device_info']}
                x = collection.find_one(dev_filter)
                if  x:
                    collection.update_one(dev_filter, {'$set':row})
                
                else:
                    print('db_name:', row['db_name'], 'device_info:', row['device_info'])
                    collection.insert_one(row)


            # t = collection.insert_many(arr_mongo)   
            # print (t)


    except Exception as e:
        print(f"error: : {str(e)}")
        return False

    finally:
        mysql_conn.close()
        mongo_client.close()

def transfer_language():
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    mongo_client = connect_mongodb()
    if not mongo_client:
        mysql_conn.close()
        return False

    try:
        with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("select * from language")
            rows = cursor.fetchall()

            arr_mysql = []
            for row in rows:
                del row['pk']
                for key, value in row.items():
                    if isinstance(value, (datetime, date)):
                        row[key] = value.isoformat()
                    if isinstance(value, (int, float)):
                        row[key] = int(value)
                arr_mysql.append(row)

            db = mongo_client[CONFIG['MONGODB']['common_db']]    
            collection = db['language']

            arr_mongo = []
            for row in arr_mysql:
                x = collection.find_one(row)
                if not x:
                    arr_mongo.append(row)

            t = collection.insert_many(arr_mongo)   
            print (t)

            return True

    except Exception as e:
        print(f"이전 중 오류 발생: {str(e)}")
        return False

    finally:
        mysql_conn.close()
        mongo_client.close()


def transfer_device_tree():
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    mongo_client = connect_mongodb()
    if not mongo_client:
        mysql_conn.close()
        return False

    try:
        # MySQL 커서 생성
        with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 전체 레코드 수 확인
            sq = "select A.device_info, B.counter_name, B.counter_label, A.code as camera_code, A.name as camera_name, A.store_code, A.square_code, C.name as store_name, D.name as square_name from camera as A inner join counter_label as B on A.code=B.camera_code inner join store as C on A.store_code=C.code inner join square as D on A.square_code=D.code"
            cursor.execute(sq)
            rows = cursor.fetchall()
            arr_mysql = []
            for row in rows:
                del row['pk']
                for key, value in row.items():
                    if isinstance(value, (datetime, date)):
                        row[key] = value.isoformat()
                    if isinstance(value, (int, float)):
                        row[key] = int(value)
                arr_mysql.append(row)
            # print (arr_mysql)

            db = mongo_client[CONFIG['MONGODB']['database']]
            collection = db['device_tree']

            arr_mongo = []
            for row in arr_mysql:
                x = collection.find_one(row)
                if not x:
                    arr_mongo.append(row)

            t = collection.insert_many(arr_mongo)
            print (t)
        return True

    except Exception as e:
        print(f"이전 중 오류 발생: {str(e)}")
        return False

    finally:
        mysql_conn.close()
        mongo_client.close()

def filter_duplicate_data(arr_mongo, record):
    for row_mongo in arr_mongo:
        if row_mongo['timestamp'] == record['timestamp'] and row_mongo['ct_label'] == record['ct_label'] and row_mongo['ct_name'] == record['ct_name'] and row_mongo['camera_code'] == record['camera_code'] and row_mongo['store_code'] == record['store_code'] and row_mongo['square_code'] == record['square_code']:
            return True
    return False

def transfer_count_data():
    mysql_table_name = 'count_tenmin_p'
    mongo_table_name = 'count_tenmin'
    batch_size = 1000
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    mongo_client = connect_mongodb()
    if not mongo_client:
        mysql_conn.close()
        return False
    try:
        # MySQL 커서 생성
        # sql = "select A.device_info, from_unixtime(A.timestamp -3600*9) as datetime, A.timestamp, A.year, A.month, A.day, A.hour, A.min, A.wday, A.week, A.counter_name as ct_name, A.counter_val as ct_value, A.counter_label as ct_label, A.camera_code, B.name as camera_name, A.store_code,  C.name as store_name, A.square_code, D.name as square_name, 0 as status from " + mysql_table_name + " as A inner join camera as B inner join store as C inner join square as D on A.camera_code=B.code and A.store_code=C.code and A.square_code= D.code where A.year=2024 and A.month=12"

        sql = "select A.device_info, from_unixtime(A.timestamp -3600*9) as datetime, A.timestamp, A.year, A.month, A.day, A.hour, A.min, A.wday, A.week, A.counter_name as ct_name, A.counter_val as ct_value, A.counter_label as ct_label, A.camera_code, A.store_code, A.square_code, 0 as status from " + mysql_table_name + " as A where A.year=2024 and A.month=12"

        with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            arr = {}
            cursor.execute("select code, name from camera")
            rows = cursor.fetchall()
            for row in rows:
                arr[row['code']] = row['name']
            cursor.execute("select code, name from store")
            rows = cursor.fetchall()
            for row in rows:
                arr[row['code']] = row['name']
            cursor.execute("select code, name from square")
            rows = cursor.fetchall()
            for row in rows:
                arr[row['code']] = row['name']



            # cursor.execute("select A.code as camera_code, A.name as camera_name, B.code as store_code, B.name as store_name, C.code as square_code, C.name as square_name from camera as A left join store as B left join square as C  on A.store_code=B.code and A.square_code=C.code")
            # rows = cursor.fetchall()
            # arr = {}
            # for row in rows:
            #     arr[row['camera_code']] = row['camera_name']
            #     arr[row['store_code']] = row['store_name']
            #     arr[row['square_code']] = row['square_name']
            
            print (arr)

            db = mongo_client[CONFIG['MONGODB']['database']]
            collection = db[mongo_table_name]

            thisyear = datetime.now().year
            for year in range(thisyear, 2018, -1):
                for month in range(1, 13):
                    ts_start = time.time()
                    overlap = 0
                    sql = "select A.device_info, from_unixtime(A.timestamp -3600*9) as datetime, A.timestamp, A.year, A.month, A.day, A.hour, A.min, A.wday, A.week, A.counter_name as ct_name, A.counter_val as ct_value, A.counter_label as ct_label, A.camera_code, A.store_code, A.square_code, 0 as status from " + mysql_table_name + " as A where A.year=" + str(year) + " and A.month=" + str(month)
                    
                    cursor.execute("select count(*) as count from " + mysql_table_name + " where year=" + str(year) + " and month=" + str(month))
                    total_records = cursor.fetchone()['count']
                    print ('total_records, year:', year, 'month:', month, ':', total_records)
                    
                    rows = collection.find({'year': year, 'month': month})
                    arr_mongo = []
                    for row in rows:
                        arr_mongo.append(row)
                    print("mongo query completed:", round(time.time() - ts_start, 2))


                    for offset in range(0, total_records, batch_size):
                        cursor.execute(sql + " LIMIT " + str(offset) + ", " + str(batch_size))
                        records = cursor.fetchall()

                        print("mysql query completed:", round(time.time() - ts_start, 2))
                        arr_rs = []
                        overlap = 0
                        for record in records:
                            for key, value in record.items():
                                if isinstance(value, (datetime, date)):
                                    record[key] = value.isoformat()

                            record['camera_name'] = arr[record['camera_code']]
                            record['store_name'] = arr[record['store_code']]
                            record['square_name'] = arr[record['square_code']]
                        
                            xp = filter_duplicate_data(arr_mongo, record)
                            if xp :
                                overlap += 1
                                continue
                            arr_rs.append(record)
                        print("arr_rs completed:", round(time.time() - ts_start, 2), "overlap:", overlap)

                        for rs in arr_rs:
                            print (rs)
                        if len(arr_rs) > 0:
                            collection.insert_many(arr_rs)
                            print("mongo insert completed:", round(time.time() - ts_start, 2))
                    
                        print(f"Processed: {year} - {month} {min(offset + batch_size, total_records)}/{total_records} - {round(time.time() - ts_start, 2)} secs")
                        print()


        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

    finally:
        mysql_conn.close()
        mongo_client.close()
    
def updateCountReportExt(db_name='cnt_demo'):

    if db_name == 'none':
        return False
    client = connect_mongodb()
    if not client:
        return False
    
    db = client[db_name]
    collection = {
        'tenmin': db['count_tenmin'],
        'hour':   db['count_hour'],
        'day':    db['count_day'],
        'week':   db['count_week'],
        'month':  db['count_month'],
        'year':   db['count_year']
    }
    # rows = collection['tenmin'].find({'status':{'$lt':31}}) 
    batch_size = 100
    thisyear = datetime.now().year
    for year in range(thisyear, 2018, -1):
        query = {'status':{'$lt':31}, 'year':year}
        total_record = collection['tenmin'].count_documents(query)
        if total_record == 0:
            continue        
        for month in range(12, 0, -1):
            if thisyear == year and month > datetime.now().month:
                continue
            query = {'status':{'$lt':31}, 'year':year, 'month':month}
            total_record = collection['tenmin'].count_documents(query)
            if total_record == 0:
                continue
            for day in range(31, 0, -1):
                query = {'status':{'$lt':31}, 'year':year, 'month':month, 'day':day}
                total_record = collection['tenmin'].count_documents(query)
                print (f"total_record({year}-{month}-{day}): {total_record}")
                if total_record == 0:
                    continue

                ts_start = time.time()
                rows = collection['tenmin'].find(query).sort('hour', 1)
                # count_tenmin에서 count_hour 데이터 추출
                i=0
                for row in rows:
                    for key, value in row.items():
                        if isinstance(value, (int, float)):
                            row[key] = int(value)
                        if isinstance(value, (datetime, date)):
                            row[key] = value.isoformat()

                    ts = int(row['timestamp'])

                    wflag = int(row['status'])
                    print ('wflag', wflag, row['status'], row['device_info'], row['datetime'], time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(row['timestamp'])), row['timestamp'], i, '/', total_record)
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
                    i+=1
                print(f"Processed: {year}-{month}-{day} {i}/{total_record}, elapsed: {round(time.time() - ts_start, 2)} secs")

    client.close()
    return True


def transfer_heatmap_data():
    mysql_table_name = 'heatmap'
    mongo_table_name = 'heatmap_hour'
    batch_size = 1000
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    mongo_client = connect_mongodb()
    if not mongo_client:
        mysql_conn.close()
        return False
    try:
        # MySQL 커서 생성
        sql = "select A.device_info, from_unixtime(A.timestamp -3600*9) as datetime, A.timestamp, A.year, A.month, A.day, A.hour, A.wday, A.week, A.body_csv as body_csv, A.camera_code, B.name as camera_name, A.store_code, C.name as store_name, A.square_code, D.name as square_name, 0 as status from heatmap as A inner join camera as B inner join store as C inner join square as D on A.camera_code=B.code and A.store_code=C.code and A.square_code= D.code"

        with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 전체 레코드 수 확인
            cursor.execute(f"SELECT COUNT(*) as count FROM {mysql_table_name}")
            total_records = cursor.fetchone()['count']

            # MongoDB 컬렉션 선택
            db = mongo_client[CONFIG['MONGODB']['database']]
            collection = db[mongo_table_name]
            
            # # 배치 처리
            
            for offset in range(0, total_records, batch_size):
            # for offset in range(0, 1):
                cursor.execute(f"{sql} LIMIT {offset}, {batch_size}")
                records = cursor.fetchall()
                
                arr_rs = []
                # datetime과 date 객체를 ISO 형식 문자열로 변환
                for record in records:
                    for key, value in record.items():
                        if isinstance(value, (datetime, date)):
                            record[key] = value.isoformat()

                    x = collection.find_one(record)
                    if not x:
                        arr_rs.append(record)
                
                print(len(arr_rs))
                if len(arr_rs) > 0:
                    collection.insert_many(arr_rs)
                
                print(f"Processed: {min(offset + batch_size, total_records)}/{total_records}")
                
        print(f"Table {mysql_table_name} transfer completed")

        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

    finally:
        mysql_conn.close()
        mongo_client.close()

if __name__ == "__main__":
    # transfer_users()
    transfer_camera_params()
    # transfer_device_tree()
    # transfer_count_data()
    # updateCountReportExt()
    # main()