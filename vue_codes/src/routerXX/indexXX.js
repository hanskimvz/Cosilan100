// import {createRouter, createWebHistory} from 'vue-router';

const routes = [
  // main
  {
    path: '/',
    redirect : '/dashboard'
  },
  {
    path: '/dashboard',
    component: () => import('@/views/DashBoard.vue'),
    meta: { title: 'dashboard', icon: 'code' },
  },
  {
    path: '/#footfall',
    meta: { title: 'DataGlunt', icon: 'code' },
    children: [
      {
        path: '/dataglunt',
        component: () => import('@/views/DataGlunt.vue'),
        meta: { title: 'DataGlunt', icon: 'code' }
      },
      {
        path: '/recentdata',
        component: () => import('@/views/RecentData.vue'),
        meta: { title: 'DataGlunt', icon: 'fa-code' }
      },
      {
        path: '/trendanalysis',
        component: () => import('@/views/TrendAnalysis.vue'),
      },
      {
        path: '/advancedanalysis',
        component: () => import('@/views/AdvancedAnalysis.vue'),
      },
    ],
  },
  {
    path: '/#datacompare',
    meta: { title: 'DataGlunt', icon: 'code' },
    children: [
      {
        path: '/comparebytime',
        component: () => import('@/views/CompareByTime.vue'),
      },
      {
        path: '/comparebyplace',
        component: () => import('@/views/CompareByPlace.vue'),
      },
      {
        path: '/trafficdistribution',
        component: () => import('@/views/TrafficDistribution.vue'),
      },
      {
        path: '/comparebylabel',
        component: () => import('@/views/CompareByLabel.vue'),
      },
    ]
  },
  {
    path: '/heatmap',
    component: () => import('@/views/HeatMap.vue'),
  },
  {
    path: '/agegender',
    component: () => import('@/views/GenderAge.vue'),
  },
  {
    path: '/#report',
    meta: { title: 'DataGlunt', icon: 'code' },
    children: [
      {
        path: '/reportsummary',
        component: () => import('@/views/ReportSummary.vue'),
      },
      {
        path: '/reportstandard',
        component: () => import('@/views/ReportStandard.vue'),
      },
      {
        path: '/reportpremium',
        component: () => import('@/views/ReportPremium.vue'),
      },
      {
        path: '/reportexport',
        component: () => import('@/views/QueryDatabase.vue'),
      },
    ]
  },
  {
    path: '/sensors',
    component: () => import('@/views/ListSensors.vue'),
  },
  {
    path: '/sitemap',
    component: () => import('@/views/DeviceMap.vue'),
  }, 
  {
    path: '/about',
    component: () => import('@/views/AboutPage.vue'),
  }, 

  // Admin page
  {
    path: '/admin/devicetree',
    component: () => import('@/views/admin/DeviceTree.vue'),
  },
  {
    path: '/admin/counterlabel',
    component: () => import('@/views/admin/CounterLabel.vue'),
  },
  {
    path: '/admin/db:custom:table',
    component: () => import('@/views/admin/DataBase.vue'),
  },
  {
    path: '/admin/information',
    component: () => import('@/views/admin/Information.vue'),
  },
  {
    path: '/admin/language',
    component: () => import('@/views/admin/Language.vue'),
  },
  {
    path: '/admin/webconfigbasic',
    component: () => import('@/views/admin/WebConfigBasic.vue'),
  },
  {
    path: '/admin/webconfigmenus',
    component: () => import('@/views/admin/WebConfigMenus.vue'),
  },
  {
    path: '/admin/webconfigdashboard',
    component: () => import('@/views/admin/WebConfigDashboard.vue'),
  },
  {
    path: '/admin/webconfiganalysis',
    component: () => import('@/views/admin/WebConfigAnalysis.vue'),
  },
  {
    path: '/admin/webconfigreport',
    component: () => import('@/views/admin/WebConfigReport.vue'),
  },




  // system_page
  {
    path: '/system/software',
    component: () => import('@/views/system/Software.vue'),
  },
  {
    path: '/system/database',
    component: () => import('@/views/system/Database.vue'),
  },
  {
    path: '/system/license',
    component: () => import('@/views/system/License.vue'),
  },
  {
    path: '/system/tool',
    component: () => import('@/views/system/Tool.vue'),
  },
  


  // Account page
  {
    path: '/admin/',
    component: () => import('@/views/account/AccountUser.vue'),
  },  
  {
    path: '/admin/account',
    component: () => import('@/views/account/AccountUser.vue'),
  },
  {
    path: '/profile',
    component: () =>import('@/views/account/UserProfile.vue')
  },
  {
    path: '/admin/profile',
    component: () => import('@/views/account/UserProfile.vue'),
  }, 
  {
    path: '/login',
    component: () =>import('@/views/account/Login.vue')
  },
  {
    path: '/logout',
    component: () =>import('@/views/account/Logout.vue')
  },   
];
// const routes = [
//   {
//     path: '/',
//     redirect : '/dashboard'
//   },
//   {
//     path: '/dashboard',
//     component: () => import('@/views/DashBoard.vue'),
//   },
//   {
//     path: '/dataglunt',
//     component: () => import('@/views/DataGlunt.vue'),
//     meta: { title: 'DataGlunt', icon: 'code' }
//   },
//   {
//     path: '/recentdata',
//     component: () => import('@/views/RecentData.vue'),
//     meta: { title: 'DataGlunt', icon: 'fa-code' }
//   },
//   {
//     path: '/trendanalysis',
//     component: () => import('@/views/TrendAnalysis.vue'),
//   },
//   {
//     path: '/advancedanalysis',
//     component: () => import('@/views/AdvancedAnalysis.vue'),
//   },
//   {
//     path: '/comparebytime',
//     component: () => import('@/views/CompareByTime.vue'),
//   },
//   {
//     path: '/comparebyplace',
//     component: () => import('@/views/CompareByPlace.vue'),
//   },
//   {
//     path: '/trafficdistribution',
//     component: () => import('@/views/TrafficDistribution.vue'),
//   },
//   {
//     path: '/comparebylabel',
//     component: () => import('@/views/CompareByLabel.vue'),
//   },
//   {
//     path: '/heatmap',
//     component: () => import('@/views/HeatMap.vue'),
//   },
//   {
//     path: '/agegender',
//     component: () => import('@/views/GenderAge.vue'),
//   },
//   {
//     path: '/reportsummary',
//     component: () => import('@/views/ReportSummary.vue'),
//   },
//   {
//     path: '/reportstandard',
//     component: () => import('@/views/ReportStandard.vue'),
//   },
//   {
//     path: '/reportpremium',
//     component: () => import('@/views/ReportPremium.vue'),
//   },
//   {
//     path: '/reportexport',
//     component: () => import('@/views/QueryDatabase.vue'),
//   },
//   {
//     path: '/sensors',
//     component: () => import('@/views/ListSensors.vue'),
//   },
//   {
//     path: '/sitemap',
//     component: () => import('@/views/DeviceMap.vue'),
//   }, 
//   {
//     path: '/about',
//     component: () => import('@/views/AboutPage.vue'),
//   }, 

//   // Admin page

//   {
//     path: '/admin/devicetree',
//     component: () => import('@/views/admin/DeviceTree.vue'),
//   },
//   {
//     path: '/admin/counterlabel',
//     component: () => import('@/views/admin/CounterLabel.vue'),
//   },
//   {
//     path: '/admin/db:custom:table',
//     component: () => import('@/views/admin/DataBase.vue'),
//   },
//   {
//     path: '/admin/information',
//     component: () => import('@/views/admin/Information.vue'),
//   },
//   {
//     path: '/admin/language',
//     component: () => import('@/views/admin/Language.vue'),
//   },
//   {
//     path: '/admin/webconfigbasic',
//     component: () => import('@/views/admin/WebConfigBasic.vue'),
//   },
//   {
//     path: '/admin/webconfigmenus',
//     component: () => import('@/views/admin/WebConfigMenus.vue'),
//   },
//   {
//     path: '/admin/webconfigdashboard',
//     component: () => import('@/views/admin/WebConfigDashboard.vue'),
//   },
//   {
//     path: '/admin/webconfiganalysis',
//     component: () => import('@/views/admin/WebConfigAnalysis.vue'),
//   },
//   {
//     path: '/admin/webconfigreport',
//     component: () => import('@/views/admin/WebConfigReport.vue'),
//   },




//   // system_page
//   {
//     path: '/system/software',
//     component: () => import('@/views/system/Software.vue'),
//   },
//   {
//     path: '/system/database',
//     component: () => import('@/views/system/Database.vue'),
//   },
//   {
//     path: '/system/license',
//     component: () => import('@/views/system/License.vue'),
//   },
//   {
//     path: '/system/tool',
//     component: () => import('@/views/system/Tool.vue'),
//   },
  


//   // Account page
//   {
//     path: '/admin/',
//     component: () => import('@/views/account/AccountUser.vue'),
//   },  
//   {
//     path: '/admin/account',
//     component: () => import('@/views/account/AccountUser.vue'),
//   },
//   {
//     path: '/profile',
//     component: () =>import('@/views/account/UserProfile.vue')
//   },
//   {
//     path: '/admin/profile',
//     component: () => import('@/views/account/UserProfile.vue'),
//   }, 
//   {
//     path: '/login',
//     component: () =>import('@/views/account/Login.vue')
//   },
//   {
//     path: '/logout',
//     component: () =>import('@/views/account/Logout.vue')
//   },   
// ];

// const router = createRouter({
//     history: createWebHistory('/'),
//     routes,
// });

// export default (router);
export default (routes);
