<template>
  <div class="row">
    <div class="col-12">
      <div class="card card-body">
        <div id="apexcharts-line"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, watch } from 'vue';
import { lineOption } from '@/components/chart_options.js';
import axios from 'axios';
import { _tz_offset, navStore, getDateString, Utc2Local } from '@/store/nav_store.js'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const router = useRouter();

const { t, locale } = useI18n();
const dp = navStore(); // piana
let ts;
const { date_from, date_to, view_by, sq_code, st_code } = storeToRefs(dp)
watch( [date_from, date_to, view_by, sq_code, st_code], (t)=> {
  // console.log(t)
  if (ts) {
    clearTimeout(ts);
  }
  ts =  setTimeout(() => {
    redrawChart();  
  }, 500);
});

let chart_line = null;
const drawChart = () => {
  chart_line = new ApexCharts(
    document.querySelector("#apexcharts-line"),
    lineOption
  );
  chart_line.render();
};

function redrawChart() {
  let date_from_t = getDateString(dp.date_from);
  const date_to_t = getDateString(dp.date_to)
  if (dp.view_by == 'tenmin' || dp.view_by == 'hourly'){
    date_from_t = getDateString(dp.date_to)
  }
  axios({
    method: 'post',
    url: '/api/query',
    params:{
      data:'count',
    },
    data: {
      format: 'json',
      db_name: dp.db_name,
      sq: [dp.sq_code],
      st: [dp.st_code], 
      cam: 0,
      date_from: date_from_t,
      date_to: date_to_t,
      view_by: dp.view_by,
      page: 'analysis:compare_by_label'
    },
    header:{"Context-Type": "multipart/form-data"}
  }).then(result => {
    console.log(result.data);
    if (result.data.code == 403) {
      router.push({ path: '/login'});
      return 0;
    }    
    if (result.data.xaxis.categories && (view_by.value == 'tenmin' || view_by.value=='hourly')) {
      result.data.xaxis.categories.forEach((item, idx)=>{
        result.data.xaxis.categories[idx] = Utc2Local(item, _tz_offset);
      });
    }

    result.data.series.forEach((item)=>{
      item.name= t(item.name);
      let all_null = true;
      item.data.forEach((val) =>{
        if (val != null) {
          all_null = false;
        }
      });
      if (all_null) {
        item.data[0]= 0;
      }
    });

    chart_line.updateOptions(result.data);
  }).catch(error => {
      console.log(error);
  });


  // const url ='/api/query?data=count&fmt=json&sq='+dp.sq_code+'&st='+dp.st_code+'&cam=0&label=entrance,exit&date_from='+date_from_t+'&date_to='+date_to_t+'&view_by='+dp.view_by+'&page=analysis:comparebylabel:0';
  // console.log(url);
  // axios.get(url)
  // .then(result => {
  //   if (result.data.xaxis.categories && (view_by.value == 'tenmin' || view_by.value=='hourly')) {
  //     result.data.xaxis.categories.forEach((item, idx)=>{
  //       result.data.xaxis.categories[idx] = Utc2Local(item, _tz_offset);
  //     });
  //   }
  //   chart_line.updateOptions(result.data);
  // //   // chart.updateSeries(result.data['series']);
  // })
  // .catch(error => {
  //     console.log(error);
  // });
}

onMounted(
    () => {
    drawChart();
    redrawChart();
  }
);
onBeforeUnmount(() => {
  chart_line.destroy();

});

</script>

<style></style>