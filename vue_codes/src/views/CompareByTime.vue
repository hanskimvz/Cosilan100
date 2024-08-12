<template>
<nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="navbar-collapse ">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <selectSite @dataEvent="updateData"/>
        <selectDate @dataEvent="updateData"/>
      </ul>
      <navLanguage /><navDropdown />
    </div>
  </nav>
  <div class="main">
    <main class="content">
      <div class="container-fluid mt-2">
        <div class="charts">
          <div class="chart">
            <h3>{{ $t('footfall') }}</h3>
            <div v-if="isLoading" class="loading-overlay">
              <div class="loading-spinner"></div>
            </div>
            <apexchart ref="barChart" type="bar" height="350" :options="barChartOptions" :series="barChartSeries"></apexchart>
          </div>
          <div class="chart">
            <h3>{{ $t('footfall') }}</h3>
            <div v-if="isLoading" class="loading-overlay">
              <div class="loading-spinner"></div>
            </div>
            <apexchart ref="lineChart" type="line" height="350" :options="lineChartOptions" :series="lineChartSeries"></apexchart>
          </div>          
        </div>

        <div class="row mb-3"></div>
          <div class="row">
            <div class="col-12">
            <div class="card">
              <div class="card-body">
                <table class="table table-striped table-bordered table-hover" >
                  <thead>
                    <tr><th> datetime </th>
                    <th v-for="(n, i) in lineChartSeries" :key="i">{{n.name}} </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(x, j) in lineChartOptions.xaxis.categories" :key="j">
                      <td> {{x}} </td>
                      <td v-for="(v, k) in lineChartSeries" > {{ v.data[j] }} </td>
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
import { onMounted, watch, ref, reactive, onBeforeUnmount } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import VueApexCharts from 'vue3-apexcharts';

import { lineOption_hourly, barOption } from '@/components/chart_options.js';
import { _tz_offset, getDateString, addDays, arraySum } from '@/assets/functions.js';

import selectSite  from '@/layout/SelectSite.vue';
import selectDate  from '@/layout/SelectDate3.vue';
import navLanguage from '@/layout/NavLanguage.vue';
import navDropdown from '@/layout/NavDropdown.vue';;

const { t, locale } = useI18n();
const route = useRoute();
const router = useRouter();
const lineChart = ref(null);
const barChart = ref(null);

let date_ref = [
  getDateString(new Date()),
  getDateString(addDays(new Date(), -7)),
  getDateString(addDays(new Date(),-14))
];

const query_data = reactive({
  format: 'json',
  db_name: 'cnt_demo',
  sq:  [],
  st:  [], 
  cam: [],
  date_from: getDateString(new Date()),
  date_to: getDateString( new Date()),
  view_by: 'hourly',
  page: 'analysis:compare_by_time'
})

let ts;
let lineSeries=[[],[],[]];
let barSeries=[[],[],[]];

const updateData = ( (data)=> {
  console.log(data)
  let key = Object.keys(data)[0];
  let chs = 0;
  if (key == 'place') {
    query_data.sq = [data[key][0]];
    query_data.st = [data[key][1]];
    chs = 7;
  }
  else if (key == 'view_by'){
    query_data.view_by = data[key];
  }
  else if (key == 'date_range'){
    date_ref = data['date_range'];
    chs  = 1 << data.channel;
  }
  if (ts) {
    clearTimeout(ts);
  }
  ts =  setTimeout(() => {
    console.log('chs', chs);
    redrawChart(chs);
  }, 500);
});

const isLoading = ref(false);
const barChartOptions  = ref({
  chart: {
    id: 'bar-chart',
    toolbar: { show : false}
  },
  series:[],
  legend:{
    show:true,
    position: 'top',
  },
  xaxis: {labels: {show:false}, 
  categories: [t('total')]},
  plotOptions: { bar: { horizontal: false, columnWidth: '80%', endingShape: 'rounded' } },
});


const lineChartOptions = ref(lineOption_hourly);
const barChartSeries = ref([]);
const lineChartSeries = ref([]);


async function  redrawChart (ch) {
  // let data = [];
  lineChartSeries.value = [];
  barChartSeries.value = [];

  // lineChartOptions.value = lineOption;
  for (let i=0; i<3; i++) {
    if (!(ch>>i&1)) {
      continue;
    }
    lineSeries[i] = [];
    barSeries[i]  = [];
    isLoading.value = true;
    query_data.date_from = date_ref[i];
    query_data.date_to   = date_ref[i];
    try {
    // await new Promise(resolve => setTimeout(resolve, 100));
      const res = await axios({
        method: 'post',
        url: '/api/query',
        params:{
          data:'count',
        },
        data: query_data,
        header:{"Context-Type": "multipart/form-data"}
      });

      const data = await res.data;
      if (data.code == 403) {
        router.push({ path: '/login', query:{'redirect': route.path}});
        return 0;
      }
      data.series.forEach((item, idx)=> {
        data.series[idx].name = t(item.name)+'('+ query_data.date_from +')';
        barSeries[i].push({'name':item.name, data:[arraySum(item.data)]});
        lineSeries[i].push(item);
      })
      // console.log(lineChartOptions.value);
      // lineChartSeries.value = lineChartSeries.value.concat(data[i].series);
    } catch(error) {
      console.error('Failed to fetch data', error)
    } finally {
      isLoading.value = false;
    }
  }
  // console.log(lineSeries);
  lineSeries.forEach(arr =>{
    // console.log(arr);
    arr.forEach(item => {
      lineChartSeries.value.push(item); 
    })
  });
  barSeries.forEach(arr =>{
    // console.log(arr);
    arr.forEach(item => {
      barChartSeries.value.push(item); 
    })
  });
  // barChartSeries.value = [].concat(barSeries);
  // lineChartSeries.value = [].concat(lineSeries);
}

onMounted(() => {
  redrawChart(7);
});
onBeforeUnmount(() => {
  lineChart.value.destroy();
  barChart.value.destroy();
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
  grid-template-columns: 1fr 4fr;
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