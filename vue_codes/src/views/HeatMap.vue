<template>
  <h3>Heatmap</h3>
  <div class="card card-body">
		<div id="heatmapContainer">
		</div>
	</div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, watch } from 'vue';
import h337 from 'heatmap.js'
let hm_option = {
  config: {
    radius: 45,
    maxOpacity: .7
  },
  image:{
    src :"",
    width: 800,
    height:450,
  },
  data: {
    max:0,
    data:[{x:0,y:0,value:0}],
  },
  tooltip:{
    id:"tooltipInstance",
  },
  style:{
    background:0,
    backgroundSize:0,
    height:0,
    width:0
  }
}
	
// create configuration object
var config = {
  container: document.getElementById('heatmapContainer'),
  radius: 10,
  maxOpacity: .5,
  minOpacity: 0,
  blur: .75
};
// create heatmap with configuration
console.log(h337);

var dataPoint = [{
  x: 5, // x coordinate of the datapoint, a number
  y: 5, // y coordinate of the datapoint, a number
  value: 100 // the value at datapoint(x, y)
}];
// heatmapInstance.addData(dataPoint);

onMounted( ()=> {
  var heatmap = h337.create({
  container: document.getElementById('heatmapContainer'),
  maxOpacity: .5,
  radius: 10,
  blur: .75,
});
// heatmap.setData(dataPoint);
});


</script>