import {createRouter, createWebHistory} from 'vue-router';
import Dashboard from '@/views/DashBoard.vue';

const routes = [
  {
    path: '/',
    component: Dashboard,
  },
  {
    path: '/dataglunt',
    component: () => import('@/views/DataGlunt.vue'),
    meta: { title: 'DataGlunt', icon: 'dashboard' }
  },
  {
    path: '/recentdata',
    component: () => import('@/views/RecentData.vue'),
  },
  {
    path: '/trendanalysis',
    component: () => import('@/views/TrendAnalysis.vue'),
  },
  {
    path: '/advancedanalysis',
    component: () => import('@/views/AdvancedAnalysis.vue'),
  },
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
  {
    path: '/heatmap',
    component: () => import('@/views/HeatMap.vue'),
  },
  {
    path: '/agegender',
    component: () => import('@/views/GenderAge.vue'),
  },
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
    path: '/admin/account',
    component: () => import('@/views/admin/AccountUser.vue'),
  },
  {
    path: '/admin/profile',
    component: () => import('@/views/admin/UserProfile.vue'),
  }, 
  {
    path: '/admin/devicetree',
    component: () => import('@/views/admin/UserProfile.vue'),
  },   
];

const router = createRouter({
    history: createWebHistory('/'),
    routes,
});

export default router;
