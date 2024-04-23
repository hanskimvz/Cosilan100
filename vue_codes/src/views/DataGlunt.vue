<template>
  <div class="col-12">
    <div id="apexcharts-line"></div>
  </div>
  <div><button class="btn btn-primary" @click="changeData">Data</button></div>
</template>

<script setup>
// import Chart from 'chart.js/auto';
import { onMounted, reactive } from 'vue';
import { lineOption } from '@/components/chart_options.js';
import axios from 'axios';
import settings from '@/assets/config.json';


//data
// const response = {
//   "series": [
//     {
//       "name": "12weeks",
//       "data": [17318, 17533, 17011, 14286, 16300, 14629, 15242, 15303, 14481, 13325, 13201, 10547, 10932, 10742, 10182, 10906, 11091, 11639, 12111, 12796, 15229, 15593, 15707, 15118, 15651, 17159, 16572, 15224, 16816, 16655, 16288, 15774, 17089, 15928, 16205, 16125, 12199, 12779, 17427, 19313, 16492, 15135, 16891, 17236, 18272, 17782, 18858, 17643, 17626, 17551, 17663, 18580, 18538, 18906, 18080, 18427, 18297, 18320, 18707, 18576, 18660, 18368, 17126, 17754, 18000, 19165, 18128, 15556, 14425, 16549, 17326, 17455, 18078, 18287, 19064, 18414, 18270, 18319, 18484, 18521, 17802, 17433, 15871, 15358]
//     }
//   ],
//   "xaxis":{
//     "type":"datetime",
//     "categories": ["2024-01-29","2024-01-30","2024-01-31","2024-02-01","2024-02-02","2024-02-03","2024-02-04","2024-02-05","2024-02-06","2024-02-07","2024-02-08","2024-02-09","2024-02-10","2024-02-11","2024-02-12","2024-02-13","2024-02-14","2024-02-15","2024-02-16","2024-02-17","2024-02-18","2024-02-19","2024-02-20","2024-02-21","2024-02-22","2024-02-23","2024-02-24","2024-02-25","2024-02-26","2024-02-27","2024-02-28","2024-02-29","2024-03-01","2024-03-02","2024-03-03","2024-03-04","2024-03-05","2024-03-06","2024-03-07","2024-03-08","2024-03-09","2024-03-10","2024-03-11","2024-03-12","2024-03-13","2024-03-14","2024-03-15","2024-03-16","2024-03-17","2024-03-18","2024-03-19","2024-03-20","2024-03-21","2024-03-22","2024-03-23","2024-03-24","2024-03-25","2024-03-26","2024-03-27","2024-03-28","2024-03-29","2024-03-30","2024-03-31","2024-04-01","2024-04-02","2024-04-03","2024-04-04","2024-04-05","2024-04-06","2024-04-07","2024-04-08","2024-04-09","2024-04-10","2024-04-11","2024-04-12","2024-04-13","2024-04-14","2024-04-15","2024-04-16","2024-04-17","2024-04-18","2024-04-19","2024-04-20","2024-04-21"],
//   }
// }


let chart = null;
const drawChart = () => {
  chart = new ApexCharts(
    document.querySelector("#apexcharts-line"),
    lineOption
  );
  chart.render();
};


function changeOptions(response) {
  // chart.updateSeries(response['series']);
  // chart.updateOptions({ xaxis: {type: 'datetime', categories : response['category'],} });
  chart.updateOptions(response);
};

function changeData(dataset) {
  chart.updateSeries(dataset);
};

// const host = window.location.host.split(":")[0];
// const url ='http://'+ host +':9999/api/query.do?fr=dashBoard&page=footfall&fm=json&sq=0&st=0&time_ref=04/21/2024';
// console.log(settings)
// const url ='http://'+settings.DataBase.serverAddress+':'+settings.DataBase.serverPort+'/api/query.do?fr=dashBoard&page=footfall&fm=json&sq=0&st=0&time_ref=04/21/2024';

onMounted(
    () => {
    drawChart();
    const url ='/api/query.do?fr=dashBoard&page=footfall&fm=json&sq=0&st=0&time_ref=04/21/2024#hanskim';
    console.log(url);
    axios.get(url)
    .then(result => {
      // 파라미터에 담긴 데이터를 콘솔로 찍어서 확인도 하고..
      console.log(result.data);
      changeOptions(result.data);
    })
    .catch(error => {
        console.log(error);
    });
  }
);

</script>

<style></style>