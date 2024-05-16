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
import { AheatmapOption } from '@/components/chart_options.js';
import axios from 'axios';
import { _tz_offset, navStore, addDays, getDateString, Utc2Local } from '@/store/nav_store.js'
import { storeToRefs } from 'pinia'

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

dp.date_from = addDays(dp.date_to, -7);

let chart_heatmap = null;
const drawChart = () => {
  chart_heatmap = new ApexCharts(
    document.querySelector("#apexcharts-line"),
    AheatmapOption
  );
  chart_heatmap.render();
};

function redrawChart() {
  const date_from_t = getDateString(dp.date_from);
  const date_to_t   = getDateString(dp.date_to);

  axios({
    method: 'post',
    url: '/api/query',
    params:{
      data:'trafficdistribution',
    },
    data: {
      format: 'json',
      db_name: dp.db_name,
      sq: [dp.sq_code],
      st: [dp.st_code], 
      cam: 0,
      date_from: date_from_t,
      date_to: date_to_t,
      view_by: 'hourly',
      page: 'analysis:traffic_distribution'
    },
    header:{"Context-Type": "multipart/form-data"}
  }).then(result => {
    console.log(result.data);
    if (result.data.xaxis.categories) {
      result.data.xaxis.categories.forEach((item, idx)=>{
        result.data.xaxis.categories[idx] = Utc2Local(item, _tz_offset);
      });
    }

    // result.data.series.forEach((item)=>{
    //   item.name= t(item.name);
    //   let all_null = true;
    //   item.data.forEach((val) =>{
    //     if (val != null) {
    //       all_null = false;
    //     }
    //   });
    //   if (all_null) {
    //     item.data[0]= 0;
    //   }

    // });
    // console.log(chart_data);
    chart_heatmap.updateOptions(result.data);
  }).catch(error => {
      console.log(error);
  });


  // const url ='/api/query?data=count&fmt=json&sq='+dp.sq_code+'&st='+dp.st_code+'&cam=0&date_from='+date_from_t+'&date_to='+date_to_t+'&view_by='+dp.view_by+'&page=analysis:dataglunt:0';
  // // console.log(url);
  // axios.get(url)
  //   .then(result => {
  //     console.log(result.data);
  //   if (result.data.xaxis.categories && (view_by.value == 'tenmin' || view_by.value=='hourly')) {
  //     result.data.xaxis.categories.forEach((item, idx)=>{
  //       result.data.xaxis.categories[idx] = Utc2Local(item, _tz_offset);
  //     });
  //   }
  //   result.data.series.forEach((item)=>{
  //     // console.log(item);
  //     item.name= t(item.name);
  //   });
  //   // result.data.xaxis.type='datetime';
  //   chart_line.updateOptions(result.data);
  // //   // chart.updateSeries(result.data['series']);
  // })
  // .catch(error => {
  //     console.log(error);
  //     // window.location.href=("/login");

  // });
}

function redrawChartxx() {
  const date_from_t = getDateString(dp.date_from);
  const date_to_t = getDateString(dp.date_to)
  const url ='/api/query?data=trafficdistribution&fmt=json&sq='+dp.sq_code+'&st='+dp.st_code+'&cam=0&label=entrance,exit&date_from='+date_from_t+'&date_to='+date_to_t+'&view_by='+dp.view_by+'&page=analysis:trafficdistribution:0';
  console.log(url);
  axios.get(url)
  .then(result => {
    console.log(result.data);
    if (result.data.xaxis.categories && (view_by.value == 'tenmin' || view_by.value=='hourly')) {
      result.data.xaxis.categories.forEach((item, idx)=>{
        result.data.xaxis.categories[idx] = Utc2Local(item, _tz_offset);
      });
    }
    chart_heatmap.updateOptions(result.data);
  //   // chart.updateSeries(result.data['series']);
  })
  .catch(error => {
      console.log(error);
  });
}

onMounted(
    () => {
    drawChart();
    redrawChart();
  }
);
onBeforeUnmount(() => {
  chart_heatmap.destroy();

});

</script>

<style></style>