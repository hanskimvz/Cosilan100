
import sys
# from web_server.proc_api import MYSQL
# print(MYSQL)
# sys.exit()


from web_server.query_db import *
from web_server.update_db import *


# print (getWebConfig('cnt_demo', 'main'))
main_body = [
    {
      "page": "split_line",
      "parent": 0,
      "depth": 0,
      "i18n_t": "main",
      "icon": "",
      "to": "",
      "use": True
    },
    {
      "page": "dashboard",
      "parent": 0,
      "depth": 0,
      "i18n_t": "dashboard",
      "icon": "monitor",
      "to": "/dashboard",
      "use": True
    },
    {
      "page": "footfall",
      "parent": 0,
      "depth": 0,
      "i18n_t": "footfall",
      "icon": "users",
      "to": "#footfall",
      "use": True,
      "children":[
        {
          "page": "dataglunt",
          "parent": 0,
          "depth": 0,
          "i18n_t": "data_glunt",
          "icon": "",
          "to": "/dataGlunt",
          "use": True
        },
        {
          "page": "latestflow",
          "parent": 0,
          "depth": 0,
          "i18n_t": "recent_data",
          "icon": "",
          "to": "/latestFlow",
          "use": True
        },
        {
          "page": "trendanalysis",
          "parent": 0,
          "depth": 0,
          "i18n_t": "trend_analysis",
          "icon": "",
          "to": "/trendAnalysis",
          "use": True
        },
        {
          "page": "advancedanalysis",
          "parent": 0,
          "depth": 0,
          "i18n_t": "advanced_analysis",
          "icon": "",
          "to": "/advancedAnalysis",
          "use": True
        },
        {
          "page": "promotionanalysis",
          "parent": 0,
          "depth": 0,
          "i18n_t": "promotion_analysis",
          "icon": "",
          "to": "/promotionAnalysis",
          "use": False
        },
        {
          "page": "brandoverview",
          "parent": 0,
          "depth": 0,
          "i18n_t": "brand_overview",
          "icon": "",
          "to": "/brandOverview",
          "use": False
        },
        {
          "page": "weatheranalysis",
          "parent": 0,
          "depth": 0,
          "i18n_t": "weather_analysis",
          "icon": "",
          "to": "/weatherAnalysis",
          "use": False
        },
        {
          "page": "kpi",
          "parent": 0,
          "depth": 0,
          "i18n_t": "kpi_overview",
          "icon": "aperture",
          "to": "/kpi",
          "use": False
        }
      ]
    },
    {
      "page": "datacompare",
      "parent": 0,
      "depth": 0,
      "i18n_t": "data_compare",
      "icon": "sliders",
      "to": "#dataCompare",
      "use": True,
      "children": [
        {
          "page": "comparebytime",
          "parent": 0,
          "depth": 0,
          "i18n_t": "compare_by_time",
          "icon": "",
          "to": "/compareByTime",
          "use": True
        },
        {
          "page": "comparebyplace",
          "parent": 0,
          "depth": 0,
          "i18n_t": "compare_by_place",
          "icon": "",
          "to": "/compareByPlace",
          "use": True
        },
        {
          "page": "trafficdistribution",
          "parent": 0,
          "depth": 0,
          "i18n_t": "traffic_distribution",
          "icon": "",
          "to": "/trafficDistribution",
          "use": True
        },
        {
          "page": "comparebylabel",
          "parent": 0,
          "depth": 0,
          "i18n_t": "compare_by_label",
          "icon": "",
          "to": "/compareByLabel",
          "use": True
        }
      ]
    },
    {
      "page": "heatmap",
      "parent": 0,
      "depth": 0,
      "i18n_t": "heatmap",
      "icon": "map-pin",
      "to": "/heatmap",
      "use": True
    },
    {
      "page": "agegender",
      "parent": 0,
      "depth": 0,
      "i18n_t": "age_gender",
      "icon": "slack",
      "to": "/agegender",
      "use": True
    },
    {
      "page": "macsniff",
      "parent": 0,
      "depth": 0,
      "i18n_t": "macsniff",
      "icon": "wifi",
      "to": "/macsniff",
      "use": False
    },
    {
      "page": "report",
      "parent": 0,
      "depth": 0,
      "i18n_t": "report",
      "icon": "book-open",
      "to": "#report",
      "use": True,
      "children":[
            {
          "page": "summary",
          "parent": 0,
          "depth": 0,
          "i18n_t": "summary",
          "icon": "",
          "to": "/summary",
          "use": True
        },
        {
          "page": "standard",
          "parent": 0,
          "depth": 0,
          "i18n_t": "standard",
          "icon": "",
          "to": "/standard",
          "use": True
        },
        {
          "page": "premium",
          "parent": 0,
          "depth": 0,
          "i18n_t": "premium",
          "icon": "",
          "to": "/premium",
          "use": True
        },
        {
          "page": "export",
          "parent": 0,
          "depth": 0,
          "i18n_t": "export_db",
          "icon": "",
          "to": "/export",
          "use": True
        }
      ]
    },
    {
      "page": "split_line",
      "parent": 0,
      "depth": 0,
      "i18n_t": "setting",
      "icon": "",
      "to": "",
      "use": True
    },

    {
      "page": "sensors",
      "parent": 0,
      "depth": 0,
      "i18n_t": "sensors",
      "icon": "camera",
      "to": "/sensors",
      "use": True
    },
    {
      "page": "sitemap",
      "parent": 0,
      "depth": 0,
      "i18n_t": "sitemap",
      "icon": "map",
      "to": "/sitemap",
      "use": True
    },
    {
      "page": "split_line",
      "parent": 0,
      "depth": 0,
      "i18n_t": "about",
      "icon": "",
      "to": "",
      "use": True
    },
    {
      "page": "aboout",
      "parent": 0,
      "depth": 0,
      "i18n_t": "about",
      "icon": "phone-call",
      "to": "/feedback",
      "use": False
    },
    {
      "page": "feedback",
      "parent": 0,
      "depth": 0,
      "i18n_t": "feedback",
      "icon": "pen-tool",
      "to": "/version",
      "use": False
    },
    
]

admin_body = [
    {
      "page": "account",
      "parent": 0,
      "depth": 0,
      "i18n_t": "account",
      "icon": "fa-id-card",
      "to": "/admin/account",
      "use": True
    },
    {
      "page": "device_tree",
      "parent": 0,
      "depth": 0,
      "i18n_t": "device_tree",
      "icon": "fa-sitemap",
      "to": "/admin/device_tree",
      "use": True
    },
    {
      "page": "list_device",
      "parent": 0,
      "depth": 0,
      "i18n_t": "camera",
      "icon": "fa-camera",
      "to": "/admin/list_device",
      "use": True
    },
    {
      "page": "counter_label_set",
      "parent": 0,
      "depth": 0,
      "i18n_t": "counter_label",
      "icon": "fa-clock",
      "to": "/admin/counter_label_set",
      "use": True
    },
    {
      "page": "custom_database",
      "parent": 0,
      "depth": 0,
      "i18n_t": "custom_database",
      "icon": "fa-database",
      "to": "#custom_database",
      "use": True,
      "children": [
        {
          "page": "counting",
          "parent": 0,
          "depth": 0,
          "i18n_t": "counting",
          "icon": "fa-user-plus",
          "to": "/admin/db:custom.count_tenmin_p",
          "use": True
        },
        {
          "page": "agegender",
          "parent": 0,
          "depth": 0,
          "i18n_t": "age_gender",
          "icon": "fa-venus-mars",
          "to": "/admin/db:custom.age_gender",
          "use": True
        },
        {
          "page": "heatmap",
          "parent": 0,
          "depth": 0,
          "i18n_t": "heatmap",
          "icon": "fa-street-view",
          "to": "/admin/db:custom.heatmap",
          "use": True
        },
        {
          "page": "weather",
          "parent": 0,
          "depth": 0,
          "i18n_t": "weather",
          "icon": "fa-cogs",
          "to": "/admin/db:custom.weather",
          "use": True
        }
      ]
    },
    {
      "page": "common_database",
      "parent": 0,
      "depth": 0,
      "i18n_t": "common_database",
      "icon": "fa-database",
      "to": "#common_database",
      "use": True,
      "children": [   
        {
          "page": "params",
          "parent": 0,
          "depth": 0,
          "i18n_t": "param",
          "icon": "fa-cogs",
          "to": "/admin/db:common.params",
          "use": True
        },
        {
          "page": "counting_common",
          "parent": 0,
          "depth": 0,
          "i18n_t": "counting",
          "icon": "fa-user-plus",
          "to": "/admin/db:common.counting_report_10min",
          "use": True
        },
        {
          "page": "event_counting_common",
          "parent": 0,
          "depth": 0,
          "i18n_t": "event_counting",
          "icon": "fa-user-plus",
          "to": "/admin/db:common.counting_event",
          "use": True
        },
        {
          "page": "face_thumbnail",
          "parent": 0,
          "depth": 0,
          "i18n_t": "face",
          "icon": "fa-smile",
          "to": "/admin/db:common.face_thumbnail",
          "use": True
        },
        {
          "page": "heatmap_common",
          "parent": 0,
          "depth": 0,
          "i18n_t": "heatmap",
          "icon": "fa-street-view",
          "to": "/admin/db:common.heatmap",
          "use": True
        },
        {
          "page": "snapshot",
          "parent": 0,
          "depth": 0,
          "i18n_t": "snapshot",
          "icon": "fa-film",
          "to": "/admin/db:common.snapshot",
          "use": True
        },
        {
          "page": "sniff",
          "parent": 0,
          "depth": 0,
          "i18n_t": "macsniff",
          "icon": "fa-cogs",
          "to": "/admin/db:common.mac_sniff",
          "use": True
        },
        {
          "page": "access_log",
          "parent": 0,
          "depth": 0,
          "i18n_t": "access_log",
          "icon": "fa-list-ol",
          "to": "/admin/db:common.access_log",
          "use": True
        }
      ]
    },        
    {
      "page": "language",
      "parent": 0,
      "depth": 0,
      "i18n_t": "language",
      "icon": "fa-language",
      "to": "/admin/language",
      "use": True
    },
    {
      "page": "information",
      "parent": 0,
      "depth": 0,
      "i18n_t": "information",
      "icon": "fa-language",
      "to": "/admin/information",
      "use": True
    },
    {
      "page": "system",
      "parent": 0,
      "depth": 0,
      "i18n_t": "system",
      "icon": "fa-database",
      "to": "#system",
      "use": True,
      "children": [  
        {
          "page": "software",
          "parent": 0,
          "depth": 0,
          "i18n_t": "software",
          "icon": "",
          "to": "/system/software",
          "use": True
        },
        {
          "page": "database",
          "parent": 0,
          "depth": 0,
          "i18n_t": "database",
          "icon": "",
          "to": "/system/database",
          "use": True
        },
        {
          "page": "license",
          "parent": 0,
          "depth": 0,
          "i18n_t": "license",
          "icon": "",
          "to": "/system/license",
          "use": True
        },
        {
          "page": "tool",
          "parent": 0,
          "depth": 0,
          "i18n_t": "tool",
          "icon": "",
          "to": "/system/tool",
          "use": True
        },
        {
          "page": "system_log",
          "parent": 0,
          "depth": 0,
          "i18n_t": "system_log",
          "icon": "",
          "to": "/system/log",
          "use": True
        }
      ]
    },
    {
      "page": "webpageconfig",
      "parent": 0,
      "depth": 0,
      "i18n_t": "webpage_config",
      "icon": "fa-database",
      "to": "#webpageconfig",
      "use": True,
      "children": [    
        {
          "page": "basic",
          "parent": 0,
          "depth": 0,
          "i18n_t": "basic",
          "icon": "",
          "to": "/admin/webconfigbasic",
          "use": True
        },
        {
          "page": "sidemenu",
          "parent": 0,
          "depth": 0,
          "i18n_t": "display_menu",
          "icon": "",
          "to": "/admin/webconfigmenus",
          "use": True
        },
        {
          "page": "dashboard",
          "parent": 0,
          "depth": 0,
          "i18n_t": "dashboard",
          "icon": "",
          "to": "/admin/webconfigdashboard",
          "use": True
        },
        {
          "page": "analysis",
          "parent": 0,
          "depth": 0,
          "i18n_t": "analysis",
          "icon": "",
          "to": "/admin/webconfiganalysis",
          "use": True
        },
        {
          "page": "report",
          "parent": 0,
          "depth": 0,
          "i18n_t": "report",
          "icon": "",
          "to": "/admin/webconfigreport",
          "use": True
        }
      ]
    }
  ]
logo_img = "data:image/png;base64,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"


analysis_body = [
  {
    "page": "data_glunt",
    "labels":["entrance"]
  },
  {
    "page": "recent_data",
    "labels":["entrance"]
  },
  {
    "page": "trend_analysis",
    "labels":["entrance"]
  },
  {
    "page": "advanced_analysis",
    "labels":["entrance","exit"]
  }, 
  {
    "page": "compare_by_time",
    "labels":["entrance"]
  }, 
  {
    "page": "compare_by_place",
    "labels":["entrance"]
  }, 
  {
    "page": "compare_by_label",
    "labels":["entrance","exit","outside","none"]
  }, 
  {
    "page": "traffic_distribution",
    "labels":["entrance"],
    "traffic_reset_hour": "04:00"
  }, 
  {
    "page": "age_gender",
    "labels":[0,18,30,45,65]
  }, 
]
# xbody =  (json.dumps(main_body, ensure_ascii=False))
# # print (xbody)
# updateWebConfig('cnt_demo', 'main', xbody)


# xbody =  json.dumps(admin_body, ensure_ascii=False)
# updateWebConfig('cnt_demo', 'admin', admin_body)

# updateWebConfig('cnt_demo', 'logo', logo_img)

# x = getWebConfig(db_name='cnt_demo', page = 'main')
# print (json.dumps(x, indent=4))

# x = updateWebConfig('cnt_demo', 'analysis', analysis_body)
# # x = getWebConfig(db_name='cnt_demo', page = 'analysis')
# print (json.dumps(x, indent=4))

postdata = {'db':'cnt_demo', 'table':'users', 'sets':[('id','hanskim'),('role',4)], 'condition':'pk=1'}
updateDatabase(postdata)