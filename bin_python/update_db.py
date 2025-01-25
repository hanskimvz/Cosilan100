# # Copyright (c) 2022, Hans kim

# # Redistribution and use in source and binary forms, with or without
# # modification, are permitted provided that the following conditions are met:
# # 1. Redistributions of source code must retain the above copyright
# # notice, this list of conditions and the following disclaimer.
# # 2. Redistributions in binary form must reproduce the above copyright
# # notice, this list of conditions and the following disclaimer in the
# # documentation and/or other materials provided with the distribution.

# # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# # CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# # INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# # MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# # DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# # CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# # SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# # BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# # SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# # INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# # WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# # NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# # OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# import os, time, sys
# import datetime
# import pymysql
# import json, re
# from functions_s import (configVars, dbconMaster, log, TZ_OFFSET)

# MYSQL = { 
#     "commonParam": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.param'),
#     "commonSnapshot": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.snapshot'),
#     "commonCount": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.counting'),
#     "commonHeatmap": configVars('software.mysql.db') +"." + configVars('software.mysql.db_common.table.heatmap'),
#     "commonCountEvent": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.count_event'),
#     "commonFace": configVars('software.mysql.db') + "." + configVars('software.mysql.db_common.table.face'),
#     "customCount": configVars('software.mysql.db_custom.table.count'),
#     "customHeatmap": configVars('software.mysql.db_custom.table.heatmap'),
#     "customAgeGender": configVars('software.mysql.db_custom.table.age_gender'),
#     "customSquare": configVars('software.mysql.db_custom.table.square'),
#     "customStore": configVars('software.mysql.db_custom.table.store'),
#     "customCamera": configVars('software.mysql.db_custom.table.camera'),
#     "customCounterLabel": configVars('software.mysql.db_custom.table.counter_label'),
#     "customRtCount": "realtime_counting",
# }
# MYSQL['customCount'] = 'count_tenmin_p'
# MYSQL['customLanguage'] = 'language'
# _selected_language = "eng"

# def updateLanguage(db_name='cnt_demo', post_data = {}):
#   d = post_data['data']
#   sq = "update " + db_name + "." + MYSQL['customLanguage'] + " set varstr=\"%s\", eng=\"%s\", kor=\"%s\", chi=\"%s\", flag=\"%s\", page=\"%s\" where pk=%d" %(d['varstr'], d['eng'], d['kor'], d['chi'], d['flag'], d['page'], d['pk'])
#   print (sq)
#   dbCon = dbconMaster()
#   with dbCon:
#     cur = dbCon.cursor()
#     xt = cur.execute(sq)
#     dbCon.commit()

#   return {"code": xt}
