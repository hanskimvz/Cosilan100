<template>
  <div>
    <canvas id="barChart"></canvas>
  </div>
</template>

<script setup>
import Chart from 'chart.js/auto';
import { onMounted } from 'vue';

function drawChart() {
  const ctx = document.getElementById("barChart").getContext("2d");  
  const barChart = new Chart(ctx, {
    type: 'bar',
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

<style></style>