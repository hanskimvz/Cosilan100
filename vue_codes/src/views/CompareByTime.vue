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
import { _tz_offset, navStore, getDateString, Utc2Local, addDays } from '@/store/nav_store.js'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const router = useRouter();

const { t, locale } = useI18n();
const dp = navStore(); // piana
let ts;
const { date_to, date_to1, date_to2, sq_code, st_code } = storeToRefs(dp)
watch( [date_to, date_to1, date_to2, sq_code, st_code], (t)=> {
  console.log(t)
  if (ts) {
    clearTimeout(ts);
  }
  ts =  setTimeout(() => {
    redrawChart();  
  }, 500);
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


dp.date_to1 = addDays(dp.date_to, -7)
dp.date_to2 = addDays(dp.date_to, -14)

let date_ref = [];
const relocDateRef = (()=>{
  date_ref[0] = getDateString(dp.date_to);
  date_ref[1] = getDateString(dp.date_to1);
  date_ref[2] = getDateString(dp.date_to2);
});

function redrawChart() {
  relocDateRef();

  let chart_options_new = [];
  for (let i=0; i<3; i++) {
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
        date_from: date_ref[i],
        date_to: date_ref[i],
        view_by: 'hourly',
        page: 'analysis:compare_by_time'
      },
      header:{"Context-Type": "multipart/form-data"}
    }).then(result => {
    // console.log(result.data);
    if (result.data.code == 403) {
      router.push({ path: '/login'});
      return 0;
    }      
      result.data.xaxis.categories.forEach((item, idx)=>{
        result.data.xaxis.categories[idx] = Utc2Local(item, _tz_offset);
      });

      result.data.series.forEach((item)=>{
        item.name = date_ref[i]+":"+t(item.name);
        let all_null = true;
        item.data.forEach((val) =>{
          if (val != null) {
            all_null = false;
          }
        });
        if (all_null) {
          item.data[0]= 0;
        }
        if (i==0){
          chart_options_new = result.data;
        }
        else {        
          chart_options_new.series.push({
            "name": item.name,
            "data": item.data
          })
        }
      });

      if (i==2) {
        chart_options_new.tooltip.x.format= "HH:mm";
        chart_line.updateOptions(chart_options_new);

        let options = {series:[], xaxis: {labels: {show:false}, categories: [t('total')]},}
        chart_options_new.series.forEach((item)=>{
          options.series.push({'name':item.name, data:[arraySum(item.data)]})
        });
        chart_bar.updateOptions(options)
      }
    }).catch(error => {
        console.log(error);
    });

  }
}

onMounted(() => {
  drawChart();
  // redrawChart(); // when loading dp.date_to1 and dp.date2 will be modified. ==>watch
});
onBeforeUnmount(() => {
  chart_line.destroy();
  chart_bar.destroy();
});
</script>

<style></style>