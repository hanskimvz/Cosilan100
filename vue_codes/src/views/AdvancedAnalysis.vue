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
                    <tr><th>datetime </th>
                      <th v-for="(n, i) in lineChartOptions.series" :key="i" size="200">{{n.name}} </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(x, j) in lineChartOptions.xaxis.categories" :key="j">
                      <td> {{x}} </td>
                      <td v-for="(v, k) in lineChartOptions.series" class="text-end"> {{v.data[j]}} </td>
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

import { lineOption } from '@/components/chart_options.js';
import { _tz_offset, getDateString, addDays } from '@/assets/functions.js';

import selectSite  from '@/layout/SelectSite.vue';
import viewBy      from '@/layout/ViewBy.vue';
import selectDate  from '@/layout/SelectDate.vue';
import navLanguage from '@/layout/NavLanguage.vue';
import navDropdown from '@/layout/NavDropdown.vue';

const { t, locale } = useI18n();
const route = useRoute();
const router = useRouter();
const chart = ref(null);

const query_data = reactive({
  format: 'json',
  db_name: 'cnt_demo',
  sq:  [],
  st:  [], 
  cam: [],
  date_from: getDateString(new Date()),
  date_to: getDateString( new Date()),
  view_by: 'hourly',
  page: 'analysis:advanced_analysis'
})

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
  // console.log(query_data);
});

const isLoading = ref(true);
const lineChartOptions = ref(lineOption);
const lineChartSeries = ref([]);

let ts = null;
watch( [query_data], (n, o)=> {
  if (ts) {
    clearTimeout(ts);
  }
  ts =  setTimeout(() => {
    redrawChart();  
  }, 500);
});
async function  redrawChart () {
  isLoading.value = true;
  console.log('query_data', query_data);
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
    console.log(data);
    if (data.code == 403) {
      router.push({ path: '/login', query:{'redirect': route.path}});
      return 0;
    }    
    data.series.forEach((item, idx)=> {
      data.series[idx].name = t(item.name);
    })
    lineChartOptions.value= data;
    // console.log(lineChartOptions.value);
    // console.log(lineChartSeries.value);
  } catch(error) {
    console.error('Failed to fetch data', error)
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  redrawChart();
});






  // const url ='/api/query?data=count&fmt=json&sq='+dp.sq_code+'&st='+dp.st_code+'&cam=0&date_from='+date_from_t+'&date_to='+date_to_t+'&view_by='+dp.view_by+'&page=analysis:advancedanalysis:0';
  // console.log(url);
  // // axios({
  // //   url:
  // // }

  // // )
  // axios.get(url)
  // .then(result => {
  //   if (result.data.xaxis.categories && (view_by.value == 'tenmin' || view_by.value=='hourly')) {
  //     result.data.xaxis.categories.forEach((item, idx)=>{
  //       result.data.xaxis.categories[idx] = Utc2Local(item, _tz_offset);
  //     });
  //   }
  //   result.data.series.forEach((item)=>{
  //     item.name= t(item.name);
  //   });    
  //   chart.updateOptions(result.data);
  // //   // chart.updateSeries(result.data['series']);
  // })
  // .catch(error => {
  //     console.log(error);
  //     // router.push("/login")
  // });
// }


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