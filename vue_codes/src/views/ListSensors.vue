<template>
  <div class="row">
    <div v-for="cam in arr_camera" :key="cam.usn" class="col-12 col-md-6 col-lg-4">
      <div class="card">
        <div class="card-header">
          <span class="float-right">{{cam.last_access }}</span>
          <h3 class="card-title mb-0"><b>{{ cam.camera_name }}</b></h3>
        </div>
        <img class="card-img-top" :src="cam.snapshot.body" alt="Unsplash" ></img>
        <div class="card-body">
          <h5>{{$t('square_name')}}: {{ cam.square_name }}</h5>
          <h5>{{$t('store_name')}}:{{ cam.store_name }}</h5>
          <h5>{{$t('device_info')}}:{{ cam.device_info }}</h5>
          <button class="btn btn-primary btn-sm mb-0" data-toggle="modal" data-target="#detail_device"  @click="deviceDetail(cam.device_info)">{{$t('detail')}}</button >
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="detail_device" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-xl" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h3 id="modal_device_info">{{ camera.device_info }}</h3>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        </div>
        <div class="modal-body m-0">
            <table class="table table-striped table-sm table-boarded">
              <tr><td rowspan="13" colspan="5"><canvas id="zone_id"></canvas></td>
                    <th>{{$t('camera_code')}}</th><td>{{ camera.camera_code }}</td></tr>
                <tr><th>{{$t('camera_name')}}</th><td>{{ camera.camera_name }}</td></tr>
                <tr><th>{{$t('mac')}}</th><td>{{ camera.mac }}</td></tr>
                <tr><th>{{$t('brand')}}</th><td>{{ camera.brand }}</td></tr>
                <tr><th>{{$t('model')}}</th><td>{{ camera.model }}</td></tr>
                <tr><th>{{$t('usn')}}</th><td>{{ camera.usn }}</td></tr>
                <tr><th>{{$t('productid')}}</th><td>{{ camera.product_id }}</td></tr>
                <tr><th>{{$t('ip_address')}}</th><td>{{ camera.ip }}</td></tr>
                <tr><th>{{$t('square_name')}}</th><td>{{ camera.square_name }}</td></tr>
                <tr><th>{{$t('store_name')}}</th><td>{{ camera.store_name }}</td></tr>
                <tr><th>{{$t('installdate')}}</th><td>{{ camera.initial_access }}</td></tr>
                <tr><th>{{$t('lastaccess')}}</th><td>{{ camera.last_access }}</td></tr>
                <tr><th>{{$t('license')}}</th><td>{{ camera.license }}</td></tr>
                <tr><th>{{$t('function')}}</th>
                  <td><i id="cntrpt"></i>{{$t('count_db')}}</td>
                  <td><i id="heatmap"></i>{{$t('heatmap')}}</td>
                  <td><i id="face_det"></i>{{$t('face')}}</td>
                  <td><i id="macsniff"></i>{{$t('macsniff')}}</td>
                  <td></td>
                  <td></td>
                </tr>
                <tr><th>{{$t('feature')}}</th>
                  <td><i id="en_cntrpt"></i>{{$t('count')}} </td>
                  <td><i id="en_heatmap"></i>{{$t('heatmap')}} </td>
                  <td><i id="en_face_det"></i>{{$t('age_gender')}} </td>
                  <td><i id="en_macsniff"></i> {{$t('macsniff')}}</td>
                  <td></td>
                  <td></td>
                </tr>
            </table>              
          
        </div>
      </div>
    </div>
	</div>  
</template>

<script setup>
import { onMounted, onBeforeUnmount, watch, ref } from 'vue';
import axios from 'axios';
import { _tz_offset, navStore } from '@/store/nav_store.js';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const router = useRouter();

const dp = navStore(); // piana
let ts;
const {  sq_code, st_code } = storeToRefs(dp)
watch( [ sq_code, st_code ], (n,t)=> {
  // console.log(n,t)
  if (ts) {
    clearTimeout(ts);
  }
  ts =  setTimeout(() => {
    getListDevices();  
  }, 2000);
});

function draw_zone(id, zone, img_src) {
  // console.log(zone);
  const context = id.getContext("2d");
  const img = new Image();
  const width = 800; 
  const height = 470;

  id.width = width;
  id.height =  height;

  let p_xy;
  let P = new Array();
  let x = new Array();
  let y = new Array();
  

  img.src = img_src;
  context.clearRect(0, 0, width, height);
  context.drawImage(img, 0, 0, width, height);
  
  for (let i=0; i<zone.length; i++) {
    P = zone[i]['points'].split(',');
    if(zone[i]['style'] == 'polygon'){
      P.push(P[0]);
    }
    for (let j=0; j<P.length; j++) {
      p_xy = P[j].split(":");
      x[j] = Math.round((width*p_xy[0])/65535);
      y[j] = Math.round((height*p_xy[1])/65535);
    }
    context.beginPath(); 	
    context.moveTo(x[0], y[0]);
    for (let j=1; j<P.length; j++) {
      context.lineTo(x[j],y[j]);
    }
    if(zone[i]['style'] == 'polygon'){
      context.lineWidth = 0;
      context.fillStyle = 'rgba(' + zone[i]['color'] + ',0.3)';
      context.closePath();
      if(zone[i]['type'] == 'nondetection') {
        context.fillStyle = "rgba(100,100,100,0.6)";
      }
      context.fill();
    }
    else {
      context.lineWidth = 3;
      context.strokeStyle = 'rgba(' + zone[i]['color'] + ',0.5)';
      context.stroke();
    }
    context.font = "12pt Calibri";
    context.fillStyle = 'rgba(' + zone[i]['color'] + ',0.8)';
    context.fillText(zone[i]['name'], x[0], y[0]-10);
  }
}

let arr_camera = ref({});
let camera = ref({});

const deviceDetail = ( (dev_info)=>{
  // console.log(arr_camera.value)
  const z = document.getElementById("zone_id");
  const f_checked = 'align-middle fas fa-check-square mr-1';
  const f_uncheck = 'align-middle far fa-square mr-1';
  arr_camera.value.forEach( (item)=>{
    if (item.device_info == dev_info) {
      camera.value =  item;
      let ss = camera.value.device_info.split("&")
      camera.value.mac = ss[0].split("=")[1];
      camera.value.brand = ss[1].split("=")[1];
      camera.value.model = ss[2].split("=")[1];

      camera.value.functions.countrpt ? $('#cntrpt').attr('class', f_checked) : $('#cntrpt').attr('class', f_uncheck);
      camera.value.functions.face_det ? $('#face_det').attr('class', f_checked) : $('#face_det').attr('class', f_uncheck);
      camera.value.functions.heatmap  ? $('#heatmap').attr('class', f_checked) : $('#heatmap').attr('class', f_uncheck);
      camera.value.functions.macsniff ? $('#macsniff').attr('class', f_checked) : $('#macsniff').attr('class', f_uncheck);

      camera.value.features.enable_countingline ? $('#en_cntrpt').attr('class', f_checked) : $('#en_cntrpt').attr('class', f_uncheck);
      camera.value.features.enable_face_det ? $('#en_face_det').attr('class', f_checked) : $('#en_face_det').attr('class', f_uncheck);
      camera.value.features.enable_heatmap  ? $('#en_heatmap').attr('class', f_checked) : $('#en_heatmap').attr('class', f_uncheck);
      camera.value.features.enable_macsniff ? $('#en_macsniff').attr('class', f_checked) : $('#en_macsniff').attr('class', f_uncheck);
      draw_zone(z, camera.value.zone_info, camera.value.snapshot.body);
    }
  })
});

const changeImage = (()=>{
  camera.value.countrpt = false
});

function getListDevices() {
  // const url ='/api/query?data=listdevice&fmt=json&sq='+dp.sq_code+'&st='+dp.st_code+'&cam=0';
  // console.log(url);
  axios({
    method: 'post',
    url: '/api/query',
    params:{
      data:'listdevice',
    },
    data: {
      format: 'json',
      db_name: dp.db_name,
      sq: [dp.sq_code],
      st: [dp.st_code], 
      cam: 0,
    },
    header:{"Context-Type": "multipart/form-data"}
  }).then(result => {
    // console.log(result.data);
    if (result.data.code == 403) {
      router.push({ path: '/login'});
      return 0;
    }    
    arr_camera.value = result.data.device;
  })
  .catch(error => {
      console.log(error);
  });
}

onMounted(() => {
  getListDevices();
});
// onBeforeUnmount(() => {
//   chart_heatmap.destroy();

// });

</script>

<style></style>