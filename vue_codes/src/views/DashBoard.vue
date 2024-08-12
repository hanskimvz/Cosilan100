<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="navbar-collapse ">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <selectSite @dataEvent="updateData"/>
          <selectDate :view_by="query_data.view_by" @dataEvent="updateData"/>        
        </ul>
        <navLanguage /><navDropdown />
      </div>
  </nav>
  
  <div class="dashboard">
    <!-- 카드 섹션 -->
    <div class="cards">
      <div v-for="(card, index) in cards" :key="index" class="card">
        <h3>{{ card.title }}</h3>
        <p class="value">{{ card.value }}</p>
        <p class="change" :class="{ positive: card.change > 0, negative: card.change < 0 }">
          {{ card.change > 0 ? '+' : '' }}{{ card.change }}%
        </p>
      </div>
    </div>

    <!-- 차트 섹션 -->
    <div class="charts">
      <div class="chart">
        <h3>Monthly Revenue</h3>
        <apexchart type="line" height="350" :options="lineOption" :series="lineChartSeries"></apexchart>
      </div>
      <div class="chart">
        <h3>Product Sales</h3>
        <apexchart type="bar" height="350" :options="barChartOptions" :series="barChartSeries"></apexchart>
      </div>
    </div>
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
import selectDate  from '@/layout/SelectDate.vue';
import navLanguage from '@/layout/NavLanguage.vue';
import navDropdown from '@/layout/NavDropdown.vue';


const query_data = reactive({
  format: 'json',
  db_name: 'cnt_demo',
  sq:  [],
  st:  [], 
  cam: [],
  date_from: getDateString(new Date()),
  date_to: getDateString( new Date()),
  view_by: 'hourly',
  page: 'analysis:data_glunt'
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


// 카드 데이터
const cards = ref([
  { title: 'Total Revenue', value: '$54,321', change: 8.4 },
  { title: 'Total Users', value: '12,345', change: 5.7 },
  { title: 'New Orders', value: '1,234', change: -2.3 },
  { title: 'Customer Satisfaction', value: '4.8/5', change: 1.2 },
]);

// 라인 차트 데이터
const lineChartOptions = ref({
  chart: { id: 'revenue-chart' },
  xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] },
  stroke: { curve: 'smooth' },
});

const lineChartSeries = ref([{
  name: 'Revenue',
  data: [30000, 40000, 35000, 50000, 49000, 60000, 70000, 91000, 85000, 94000, 80000, 100000],
}]);

// 바 차트 데이터
const barChartOptions = ref({
  chart: { id: 'sales-chart' },
  xaxis: { categories: ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'] },
  plotOptions: { bar: { horizontal: false, columnWidth: '55%', endingShape: 'rounded' } },
});

const barChartSeries = ref([{
  name: 'Sales',
  data: [400, 430, 448, 470, 540],
}]);

onMounted(() => {
  // 여기에서 필요한 경우 API로부터 실제 데이터를 가져올 수 있습니다.
});
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card h3 {
  margin: 0 0 10px;
  font-size: 16px;
  color: #333;
}

.card .value {
  font-size: 24px;
  font-weight: bold;
  margin: 0 0 5px;
}

.card .change {
  font-size: 14px;
}

.change.positive { color: green; }
.change.negative { color: red; }

.charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
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