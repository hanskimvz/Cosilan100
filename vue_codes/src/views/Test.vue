<template>
  <div>
    <apexchart
      width="100%"
      height="400"
      type="line"
      :options="chartOptions"
      :series="series"
    ></apexchart>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VueApexCharts from 'vue3-apexcharts'

const chartOptions = ref({
  chart: {
    type: 'line',
    stacked: false,
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    width: [0, 4,5]  // Changed order: first is bar (0), second is line (4)
  },
  title: {
    text: 'XYZ - Stock Analysis',
    align: 'left',
  },
  xaxis: {
    categories: [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016],
  },
  yaxis: [
    {
      axisTicks: { show: true },
      axisBorder: { show: true, color: '#00E396' },
      labels: { style: { colors: '#00E396' } },
      title: {
        text: "Bar Series",
        style: { color: '#00E396' },
      },
    },
    {
      opposite: true,
      axisTicks: { show: true },
      axisBorder: { show: true, color: '#008FFB' },
      labels: { style: { colors: '#008FFB' } },
      title: {
        text: "Line Series",
        style: { color: '#008FFB' },
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
    y: {
      formatter: function (y) {
        if(typeof y !== "undefined") {
          return  y.toFixed(0) + " points";
        }
        return y;
      }
    }
  },
  legend: {
    horizontalAlign: 'left',
    offsetX: 40
  }
})

const series = ref([
  {
    name: 'Bar Series',
    type: 'column',
    data: [13, 23, 20, 8, 13, 27, 33, 12]
  },
  {
    name: 'Line Series',
    type: 'line',
    data: [20, 29, 37, 36, 44, 45, 50, 58]
  },
    {
    name: 'Line Series2',
    type: 'line',
    data: [29, 37, 36, 44, 45, 50, 58,30]
  }
])
</script>