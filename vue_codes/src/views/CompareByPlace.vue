<template>
  <div class="row">
    <div class="col-12 col-lg-3 ">
      <div class="card card-body">
        <div id="apexcharts-bar"></div>
      </div>
    </div>				
    <div class="col-12 col-lg-9">
      <div class="card card-body">
        <div id="apexcharts-line"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, reactive, watch } from 'vue';
import { lineOption, barOption } from '@/components/chart_options.js';
import axios from 'axios';
import { _tz_offset, navStore,  getDateString, Utc2Local, addDays } from '@/store/nav_store.js';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const router = useRouter();
const { t, locale } = useI18n();

const dp = navStore(); // piana
let chart_series = [[],[],[]];
let ts;

const { date_from, date_to, view_by, sq_code, st_code, sq_code1, st_code1, sq_code2, st_code2 } = storeToRefs(dp)
watch( [date_from, date_to, view_by, sq_code, st_code, sq_code1, st_code1, sq_code2, st_code2], (o,n)=> {
  // console.log(o,n)
  let ch=0;
  if (ts) {
    clearTimeout(ts);
  }
  ts =  setTimeout(() => {
    for(let i=0; i<9; i++) {
      if (o[i] != n[i] ) {
        if (i==3 || i==4) { 
          redrawChart(0);
        }
        else if (i==5 || i==6) { 
          redrawChart(1);  
        }
        else if (i==7 || i==8) { 
          redrawChart(2);  
        }
        else {
          redrawChart(0);
          redrawChart(1);  
          redrawChart(2);  
        }
        break;
      }
    }
  }, 2000);
});

let chart_line = null;
let chart_bar = null;
const drawChart = () => {
  chart_line = new ApexCharts(
    document.querySelector("#apexcharts-line"),
    lineOption
  );
  chart_bar = new ApexCharts(
    document.querySelector("#apexcharts-bar"),
    barOption
  );
  chart_line.render();
  chart_bar.render();
  console.log("chart created")
};

const arraySum = ((arr) => {
	let sum = 0;
	arr.forEach(function(item){
		sum += Number(item);
	});
	return sum;
});



async function redrawChart(ch) {
  let date_from_t = getDateString(dp.date_from);
  const date_to_t = getDateString(dp.date_to)
  if (dp.view_by == 'tenmin' || dp.view_by == 'hourly'){
    date_from_t = getDateString(dp.date_to)
  }

  let place_ref = [[dp.sq_code, dp.st_code], [dp.sq_code1, dp.st_code1], [dp.sq_code2, dp.st_code2]];

  chart_series[ch] =[];
  if (place_ref[ch][0] == 0 || place_ref[ch][0] == '0') {

    let x_series = [].concat(...chart_series);
    if (x_series.length) {
      console.log(x_series)
      chart_line.updateSeries(x_series);
    }

    let options = {series:[], xaxis: {labels: {show:false}, categories: [t('total')]},}
    x_series.forEach((item)=>{
      options.series.push({'name':item.name, data:[arraySum(item.data)]})
    });
    chart_bar.updateOptions(options)

    return false;
  }
  await axios({
    method: 'post',
    url: '/api/query',
    params:{
      data:'count',
    },
    data: {
      format: 'json',
      db_name: dp.db_name,
      sq: [place_ref[ch][0]],
      st: [place_ref[ch][1]], 
      cam: 0,
      date_from: date_from_t,
      date_to: date_to_t,
      view_by: dp.view_by,
      page: 'analysis:compare_by_place'
    },
    header:{"Context-Type": "multipart/form-data"}
  }).then(result => {
    // console.log(result.data);
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
      item.name = ch + ":" + t(item.name);
      let all_null = true;
      item.data.forEach((val) =>{
        if (val != null) {
          all_null = false;
        }
      });
      if (all_null) {
        item.data[0]= 0;
      }
      chart_series[ch].push({
        "name": item.name,
        "data": item.data
      });
    });
    
    chart_line.updateOptions(result.data);
    let x_series = [].concat(...chart_series);
    chart_line.updateSeries(x_series);

    let options = {series:[], xaxis: {labels: {show:false}, categories: [t('total')]},}
    x_series.forEach((item)=>{
      options.series.push({'name':item.name, data:[arraySum(item.data)]})
    });
    chart_bar.updateOptions(options)


  }).catch(error => {
    console.log(error);
  });
}


onMounted(() => {
  drawChart();
  // redrawChart(0)
  // redrawChart(); // when loading dp.date_to1 and dp.date2 will be modified. ==>watch
});
onBeforeUnmount(() => {
  chart_line.destroy();
  chart_bar.destroy();
});
</script>
