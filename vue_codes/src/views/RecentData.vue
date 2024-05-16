<template>
  <div class="col-12">
    <div class="card card-body">
      <div id="apexcharts-line"></div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, onBeforeUnmount, watch } from 'vue';
import { lineOption } from '@/components/chart_options.js';
import axios from 'axios';
import { navStore, getDateString, addDays } from '@/store/nav_store.js';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';


const router = useRouter();
const { t, locale } = useI18n();


const dp = navStore(); // piana
let ts;
const { date_to, view_on, sq_code, st_code } = storeToRefs(dp)
watch([date_to, view_on, sq_code, st_code], (t)=> {
  // console(t)
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



const viewOn2Days = {
  '7days': -7, 
  '4weeks': -7*4,
  '12weeks': -7*12
};

function redrawChart() {
  const date_from_t = getDateString(addDays(dp.date_to, viewOn2Days[dp.view_on]));
  const date_to_t = getDateString(dp.date_to)
  // const url ='/api/query?data=count&fmt=json&sq='+dp.sq_code+'&st='+dp.st_code+'&cam=0&date_from='+date_from+'&date_to='+date_to+'&view_by=daily&page=analysis:latestflow';
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
      view_by: 'daily',
      page: 'analysis:recent_data'
    },
    header:{"Context-Type": "multipart/form-data"}
  }).then(result => {
    // console.log(result.data);
    if (result.data.code == 403) {
      router.push({ path: '/login'});
      return 0;
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
    // console.log(all_null)
    chart_line.updateOptions(result.data);
  }).catch(error => {
      console.log(error);
  });


  // console.log(url);
  // axios.get(url)
  // .then(result => {
  //   result.data.series.forEach((item)=>{
  //     // console.log(item);
  //     item.name= t(item.name);
  //   });    
  //   chart_line.updateOptions(result.data);
  //   // chart.updateSeries(result.data['series']);
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

onBeforeUnmount(()=>{
  chart_line.destroy();
})
</script>

<style></style>