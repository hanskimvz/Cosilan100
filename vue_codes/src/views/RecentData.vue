<script setup>
// import Chart from 'chart.js/auto';
import { onMounted } from 'vue';


function drawChart() {
  const ctx = document.getElementById("myChart").getContext("2d");  
  const barChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderColor: '#36A2EB',
        // backgroundColor: '#9BD0F5',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        },
      }
    }
  });
}
onMounted(() => drawChart())

</script>
<template>
  <h2>Recent Data</h2>
  <div class="row">
    <!-- <barChart /> -->
    <div><canvas id="myChart"></canvas></div>
  </div>
</template>
<style></style>