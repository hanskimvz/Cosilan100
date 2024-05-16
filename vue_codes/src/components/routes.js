import {createRouter, createWebHistory} from 'vue-router';

const routes = [
  // main
  { path: '/',  redirect : '/dashboard' },
  { path: '/dashboard',                component: () => import('@/views/DashBoard.vue'),                  meta: {page: "main"}    },
  { path: '/dataglunt',                component: () => import('@/views/DataGlunt.vue'),                  meta: {page: "main"}    },
  { path: '/recentdata',               component: () => import('@/views/RecentData.vue'),                 meta: {page: "main"}    },
  { path: '/trendanalysis',            component: () => import('@/views/TrendAnalysis.vue'),              meta: {page: "main"}    },
  { path: '/advancedanalysis',         component: () => import('@/views/AdvancedAnalysis.vue'),           meta: {page: "main"}    },
  { path: '/promotionanalysis',        component: () => import('@/views/PromotionAnalysis.vue'),          meta: {page: "main"}    },
  { path: '/brandoverview',            component: () => import('@/views/BrandOverview.vue'),              meta: {page: "main"}    },
  { path: '/weatheranalysis',          component: () => import('@/views/WeatherAnalysis.vue'),            meta: {page: "main"}    },
  { path: '/kpi',                      component: () => import('@/views/KPI.vue'),                        meta: {page: "main"}    },
  { path: '/comparebytime',            component: () => import('@/views/CompareByTime.vue'),              meta: {page: "main"}    },
  { path: '/comparebyplace',           component: () => import('@/views/CompareByPlace.vue'),             meta: {page: "main"}    },
  { path: '/trafficdistribution',      component: () => import('@/views/TrafficDistribution.vue'),        meta: {page: "main"}    },
  { path: '/comparebylabel',           component: () => import('@/views/CompareByLabel.vue'),             meta: {page: "main"}    },
  { path: '/heatmap',                  component: () => import('@/views/HeatMap.vue'),                    meta: {page: "main"}    },
  { path: '/agegender',                component: () => import('@/views/GenderAge.vue'),                  meta: {page: "main"}    },
  { path: '/macsniff',                 component: () => import('@/views/MacSniff.vue'),                   meta: {page: "main"}    },
  { path: '/reportsummary',            component: () => import('@/views/ReportSummary.vue'),              meta: {page: "main"}    },
  { path: '/reportstandard',           component: () => import('@/views/ReportStandard.vue'),             meta: {page: "main"}    },
  { path: '/reportpremium',            component: () => import('@/views/ReportPremium.vue'),              meta: {page: "main"}    },
  { path: '/reportexport',             component: () => import('@/views/QueryDatabase.vue'),              meta: {page: "main"}    },
  { path: '/sensors',                  component: () => import('@/views/ListSensors.vue'),                meta: {page: "main"}    },
  { path: '/sitemap',                  component: () => import('@/views/DeviceMap.vue'),                  meta: {page: "main"}    }, 
  { path: '/about',                    component: () => import('@/views/AboutPage.vue'),                  meta: {page: "main"}    }, 
  { path: '/feedback',                 component: () => import('@/views/Feedback.vue'),                   meta: {page: "main"}    }, 

  // Admin page
  { path: '/admin', redirect: '/admin/account' },  
  { path: '/admin/devicetree',         component: () => import('@/views/admin/DeviceTree.vue'),           meta: {page: "admin"}   },
  { path: '/admin/listdevice',         component: () => import('@/views/admin/ListDevice.vue'),           meta: {page: "admin"}   },       
  { path: '/admin/counterlabel',       component: () => import('@/views/admin/CounterLabel.vue'),         meta: {page: "admin"}   },     
  { path: '/admin/db:custom:table',    component: () => import('@/views/admin/DataBase.vue'),             meta: {page: "admin"}   },         
  { path: '/admin/information',        component: () => import('@/views/admin/Information.vue'),          meta: {page: "admin"}   },     
  { path: '/admin/language',           component: () => import('@/views/admin/Language.vue'),             meta: {page: "admin"}   },        
  { path: '/admin/webconfigbasic',     component: () => import('@/views/admin/WebConfigBasic.vue'),       meta: {page: "admin"}   },   
  { path: '/admin/webconfigmenus',     component: () => import('@/views/admin/WebConfigMenus.vue'),       meta: {page: "admin"}   },   
  { path: '/admin/webconfigdashboard', component: () => import('@/views/admin/WebConfigDashboard.vue'),   meta: {page: "admin"}   },
  { path: '/admin/webconfiganalysis',  component: () => import('@/views/admin/WebConfigAnalysis.vue'),    meta: {page: "admin"}   }, 
  { path: '/admin/webconfigreport',    component: () => import('@/views/admin/WebConfigReport.vue'),      meta: {page: "admin"}   },  

  // system_page
  { path: '/system/software',          component: () => import('@/views/system/Software.vue'),            meta: {page: "admin"}   }, 
  { path: '/system/database',          component: () => import('@/views/system/Database.vue'),            meta: {page: "admin"}   },  
  { path: '/system/license',           component: () => import('@/views/system/License.vue'),             meta: {page: "admin"}   },   
  { path: '/system/tool',              component: () => import('@/views/system/Tool.vue'),                meta: {page: "admin"}   },     
  { path: '/system/log',               component: () => import('@/views/system/SystemLog.vue'),           meta: {page: "admin"}   },
      // Account page
  { path: '/admin/',                   component: () => import('@/views/account/AccountUser.vue'),        meta: {page: "admin"} },
  { path: '/admin/account',            component: () => import('@/views/account/AccountUser.vue'),        meta: {page: "admin"} },
  { path: '/profile',                  component: () => import('@/views/account/UserProfile.vue'),        meta: {page: "admin"} },
  { path: '/admin/profile',            component: () => import('@/views/account/UserProfile.vue'),        meta: {page: "admin"} }, 
  { path: '/login',                    component: () => import('@/views/account/Login.vue'),              meta: {page: "account"} },
  { path: '/logout',                   component: () => import('@/views/account/Logout.vue'),             meta: {page: "account"} },
  { path: '/pagesResetPassword',       component: () => import('@/views/account/pagesResetPassword.vue'), meta: {page: "account"} }, 
];


const router = createRouter({
    history: createWebHistory('/'),
    routes,
});

export default (router);
// export default (routes);
