<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="navbar-collapse ">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <selectSite @dataEvent="updateData"/>
          <viewBy     @dataEvent="updateData" />
          <selectDate :view_by="query_data.view_by" @dataEvent="updateData"/>
        </ul>
        <navLanguage /><navDropdown />
      </div>
  </nav>
  <!-- <div style="margin:10px; margin-top:20px;" class="row justify-content-center ml-5"> -->
  <div class="main">
    <main class="content">
      <div class="container-fluid mt-2">

        <div class="charts">
          <div class="chart">
            <h3>{{ $t('footfall') }}</h3>
            <div v-if="isLoading" class="loading-overlay">
              <div class="loading-spinner"></div>
            </div>
            <apexchart ref="chart" type="line" height="350" :options="lineChartOptions" :series="lineChartSeries"></apexchart>
            
          </div>
        </div>
        <div class="row mb-3"></div>
          <div class="row">
            <div class="col-12">
            <div class="card">
              <div class="card-body">
                <table class="table table-striped table-bordered table-hover" >
                  <thead>
                    <tr>
                      <th> datetime </th>
                      <th v-for="(n, i) in lineChartSeries" :key="i" size="100">{{ n.name }} </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(x, j) in lineChartOptions.xaxis.categories" :key="j">
                      <td> {{ts_to_date(x, query_data.view_by) }} </td>
                      <td v-for="(v, k) in lineChartSeries" class="text-end" size="100"> {{v.data[j]}} </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      
      </div>
    </main>
  </div>
</template>

<script setup>
// import ApexCharts from 'apexcharts';
import { onMounted, watch, ref, reactive, onBeforeUnmount } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import { useCookies } from 'vue3-cookies';
import axios from 'axios';

import { lineOption } from '@/components/chart_options.js';
import { _tz_offset, getDateString, addDays, makeSeries, makeXaxis } from '@/assets/functions.js';

import selectSite  from '@/layout/SelectSite.vue';
import viewBy      from '@/layout/ViewBy.vue';
import selectDate  from '@/layout/SelectDate.vue';
import navLanguage from '@/layout/NavLanguage.vue';
import navDropdown from '@/layout/NavDropdown.vue';

const { t, locale } = useI18n();
const route = useRoute();
const router = useRouter();
const { cookies } = useCookies();
const chart = ref(null);

let db_tables = {
  'tenmin': 'count_tenmin',
  'hourly': 'count_hour',
  'daily' : 'count_day',
  'weekly': 'count_week',
  'monthly': 'count_month',
  'yearly': 'count_year',
}

const query_data = reactive({
  sq:  [],
  st:  [], 
  cam: [],
  date_from: getDateString(new Date()),
  date_to: getDateString( new Date()),
  view_by: 'hourly',
})

const post_data = reactive({
  db_name: cookies.get('_db_name'),
  table: 'count_hour',
  filter: {},
  fields: {},
  orderby: '',
  page_no: 1,
  page_max: 25,
  format : 'json'
})

const ts_to_date = (ts, view_by)=> {
  let locale_str = 'en-US';
  if (locale.value == 'kor') {
    locale_str = 'ko-KR';
  }
  else if (locale.value == 'en') {
    locale_str = 'en-US';
  }
  else if(locale.value == 'chi') {
    locale_str = 'zh-CN';
  }
  if (view_by == 'hourly' || view_by == 'tenmin') {
    return new Date(ts).toLocaleString(locale_str, { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'});
  }
  else if (view_by == 'daily') {
    return new Date(ts).toLocaleString(locale_str, { year: 'numeric', month: '2-digit', day: '2-digit' });
  }
  else if (view_by == 'weekly') {
    return new Date(ts).toLocaleString(locale_str, { year: 'numeric', month: '2-digit', day: '2-digit' });
  }
  else if (view_by == 'monthly') {
    return new Date(ts).toLocaleString(locale_str, { year: 'numeric', month: '2-digit' });
  }
}

const updateData = ( (data)=> {
  console.log('updateData', data);
  let key = Object.keys(data)[0];
  if (key == 'place') {
    query_data.sq  = [data[key][0]];
    query_data.st  = [data[key][1]];
    query_data.cam = [data[key][2]];
  }
  else if (key == 'view_by'){
    query_data.view_by = data[key];
    post_data.table = db_tables[query_data.view_by];
  }
  else if (key == 'date_range'){
    if(query_data.view_by == 'monthly'){
      let d_from = new Date(data[key][0]);
      d_from.setDate(1);
      d_from.setHours(0, 0, 0, 0);
      query_data.date_from = getDateString(d_from);

      let d_to = new Date(data[key][1]); 
      d_to.setDate(1);
      d_to.setHours(0, 0, 0, 0);
      d_to.setMonth(d_to.getMonth() + 1); // 다음달로 이동
      d_to.setDate(0); // 이전달의 마지막날로 설정
      query_data.date_to = getDateString(d_to);
    }
    else {
      query_data.date_from = data[key][0];
      query_data.date_to   = data[key][1];
    }
  }
  // console.log(query_data);
});

const isLoading = ref(false);
const lineChartOptions = ref(lineOption);
const lineChartSeries = ref([]);
// lineChartOptions.value.xaxis.type='datetime';
// lineChartOptions.value.xaxis.tickAmount = 10;

let ts = null;
watch( [query_data], (n, o)=> {
  if (ts) {
    clearTimeout(ts);
  }
  ts =  setTimeout(() => {
    redrawChart();  
  }, 500);
});
let counter_labels = ref(['entrance', 'exit']);


async function redrawChart () {
  isLoading.value = true;
  console.log('post_data', post_data);  
  post_data.filter = {
    $and: [
      query_data.sq[0] ?  {square_code:  query_data.sq[0]} : {},
      query_data.st[0] ?  {store_code:  query_data.st[0]} : {},
      query_data.cam[0] ? {camera_code: query_data.cam[0]} : {},
      {$or: counter_labels.value.map(x => ({ct_label: x}))},
      {timestamp: {$gte: (new Date(query_data.date_from).getTime())/1000}},
      {timestamp: {$lt: (new Date(query_data.date_to).getTime())/1000 + 3600*24}},
    ]
  }
  console.log('post_data.filter', post_data.filter);
  try {
    // await new Promise(resolve => setTimeout(resolve, 100));
    const res = await axios({
      method: 'post',
      url: '/api/query',
      params:{ data:'querydb' },
      data: post_data,
      header:{"Context-Type": "multipart/form-data"}
    });

    const data = await res.data;
    console.log(data);
    if (data.code == 403) {
      router.push({ path: '/login', query:{'redirect': route.path}});
      return 0;
    }

    let xaxis = makeXaxis(query_data.date_from, query_data.date_to, query_data.view_by);
    lineChartOptions.value.xaxis.categories = xaxis;
    lineChartSeries.value = makeSeries(data.data, xaxis, t);

    chart.value.updateOptions(lineChartOptions.value);

  } 
  catch(error) {
    console.error('Failed to fetch data', error)
  } 
  finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  redrawChart();
});

onBeforeUnmount(()=> {
  chart.value.destroy();
});

</script>

<style scoped>
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-spinner {
  border: 4px solid #333;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.charts {
  display: grid;
  gap: 20px;
}

.chart {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart h3 {
  margin: 0 0 20px;
  font-size: 18px;
  color: #333;
}
</style>
