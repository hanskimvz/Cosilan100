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

import { lineOption, lineOption_hourly, barOption } from '@/components/chart_options.js';
import { _tz_offset, getDateString, addDays, arraySum } from '@/assets/functions.js';

import selectSite  from '@/layout/SelectSite.vue';
import viewBy      from '@/layout/ViewBy.vue';
import selectDate  from '@/layout/SelectDate.vue';
import navLanguage from '@/layout/NavLanguage.vue';
import navDropdown from '@/layout/NavDropdown.vue';


const { t, locale } = useI18n();
const route = useRoute();
const router = useRouter();
const lineChart = ref(null);
const barChart = ref(null);

const query_data = reactive({
  format: 'json',
  db_name: 'cnt_demo',
  sq:  [],
  st:  [], 
  cam: [],
  date_from: getDateString(new Date()),
  date_to: getDateString( new Date()),
  view_by: 'hourly',
  page: 'analysis:trend_analysis'
})

let ts;
const updateData = ( (data)=> {
  console.log(data)
  let key = Object.keys(data)[0];
  if (key == 'place') {
    query_data.sq = [data[key][0]];
    query_data.st = [data[key][1]];
  }
  else if (key == 'view_by'){
    query_data.view_by = data[key];
  }
  else if (key == 'date_range'){
    query_data.date_from = data[key][0];
    query_data.date_to   = data[key][1];
  }
  console.log(key, isLoading.value);
  if (ts) {
    clearTimeout(ts);
  }
  ts =  setTimeout(() => {
    redrawChart();  
  }, 500);
});

const isLoading = ref(true);
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

const lineChartOptions = ref(lineOption);
const barChartSeries = ref([]);
const lineChartSeries = ref([]);

lineChartOptions.value.stroke.width=3;
// watch([query_data], (t)=> {
//   // console(t)
//   if (!isLoading.value) {
//   if (ts) {
//     clearTimeout(ts);
//   }
//   ts =  setTimeout(() => {
//     redrawChart();  
//   }, 500);
//   }
// });

let date_ref = [[],[],[]];
const relocDateRef = (()=>{
  date_ref[0][1] = getDateString(new Date(query_data.date_to));
  date_ref[1][1] = getDateString(addDays(new Date(query_data.date_to), -7));
  date_ref[2][1] = getDateString(addDays(new Date(query_data.date_to), -365));

  if (query_data.view_by == 'tenmin' || query_data.view_by == 'hourly'){ // one day
    date_ref[0][0] = date_ref[0][1];
    date_ref[1][0] = date_ref[1][1];
    date_ref[2][0] = date_ref[2][1];
  }
  else if (query_data.view_by == 'daily') {
    date_ref[0][0] = getDateString(addDays(new Date(query_data.date_to), -7));
    date_ref[1][0] = getDateString(addDays(new Date(query_data.date_to), -14));
    date_ref[2][0] = getDateString(addDays(new Date(query_data.date_to), -365-7));
  }
  else if (query_data.view_by == 'monthly') {
    date_ref[0][0] = getDateString(addDays(new Date(query_data.date_to), -7));
    date_ref[1][0] = getDateString(addDays(new Date(query_data.date_to), -14));
    date_ref[2][0] = getDateString(addDays(new Date(query_data.date_to), -365-7));
  }
});


async function  redrawChart () {
  let data = [];
  relocDateRef();
  lineChartSeries.value = [];
  barChartSeries.value = [];
  let lineSeries = [];
  // lineChartOptions.value = lineOption;
  for (let i=0; i<3; i++) {
    isLoading.value = true;
    query_data.date_from = date_ref[i][0];
    query_data.date_to   = date_ref[i][1];
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

      data[i] = await res.data;
      if (data[i].code == 403) {
        router.push({ path: '/login', query:{'redirect': route.path}});
        return 0;
      }
      data[i].series.forEach((item, idx)=> {
        data[i].series[idx].name = t(item.name)+'('+ query_data.date_from +')';
        barChartSeries.value.push({'name':item.name, data:[arraySum(item.data)]});
        lineSeries.push(item);
      })
      // lineChartOptions.value= data;
      console.log(lineChartOptions.value);
        // lineChartOptions.value= data[i];
      // console.log(lineChartSeries.value);
      // if (i==0) {
        lineChartOptions.value= data[i];
      // }
      // else {
      //   data[i].series.forEach(arr => {
      //     lineChartOptions.value.series.push(arr);
      //   })
      // }
      lineChartSeries.value = lineChartSeries.value.concat(data[i].series);
    } catch(error) {
      console.error('Failed to fetch data', error)
    } finally {
      isLoading.value = false;
    }
  }
  
  // lineChartOptions.value.series = lineSeries;

  console.log(data)
  console.log(lineChartOptions.value);
  // lineChartOptions.value= data[0];
  // lineChartSeries.value = [];
  // lineChartSeries.value= [].concat(data[0].series, data[1].series, data[2].series);
}

// function redrawChartXX() {
//   relocDateRef();

//   let chart_options_new = [];
//   for (let i=0; i<3; i++) {
//     axios({
//       method: 'post',
//       url: '/api/query',
//       params:{
//         data:'count',
//       },
//       data: {
//         format: 'json',
//         db_name: dp.db_name,
//         sq: [dp.sq_code],
//         st: [dp.st_code], 
//         cam: 0,
//         date_from: date_ref[i][0],
//         date_to: date_ref[i][1],
//         view_by: dp.view_by,
//         page: 'analysis:trend_analysis'
//       },
//       header:{"Context-Type": "multipart/form-data"}
//     }).then(result => {
//         // console.log(result.data);
//       if (result.data.code == 403) {
//         router.push({ path: '/login'});
//         return 0;
//       }        
//       if (result.data.xaxis.categories && (view_by.value == 'tenmin' || view_by.value=='hourly')) {
//         result.data.xaxis.categories.forEach((item, idx)=>{
//           result.data.xaxis.categories[idx] = Utc2Local(item, _tz_offset);
//         });
//       }

//       result.data.series.forEach((item)=>{
//         item.name = date_ref[i][0]+":"+t(item.name);
//         let all_null = true;
//         item.data.forEach((val) =>{
//           if (val != null) {
//             all_null = false;
//           }
//         });
//         if (all_null) {
//           item.data[0]= 0;
//         }
//         if (i==0){
//           chart_options_new = result.data;
//         }
//         else {        
//           chart_options_new.series.push({
//             "name": item.name,
//             "data": item.data
//           })
//         }
//       });

//       if (i==2) {
//         if (view_by.value == 'tenmin' || view_by.value=='hourly') {
//           chart_options_new.tooltip.x.format= "HH:mm";

//         }
//         else if (view_by.value == 'daily') {
//           chart_options_new.tooltip.y = {
//             title: {
//               formatter: (serName, data) => {
//                 let exSer =  serName.split(":");
//                 return getDateString(addDays(new Date(exSer[0]), data.dataPointIndex)) + ":" + exSer[1];
//               }
//             }
//           }
//         }
//         chart_line.updateOptions(chart_options_new);
//         // chart_line.updateSeries(chart_options_new.series);
//         let options = {series:[], xaxis: {labels: {show:false}, categories: [t('total')]},}
//         chart_options_new.series.forEach((item)=>{
//           options.series.push({'name':item.name, data:[arraySum(item.data)]})
//         });
//         chart_bar.updateOptions(options)
//       }
//     }).catch(error => {
//         console.log(error);
//     });

//   }
// }

onMounted(() => {
  // redrawChart();
});

onBeforeUnmount(()=>{
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