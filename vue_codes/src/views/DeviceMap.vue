<template>
  <div class="row">
    <table class="table table-sm">
      <tr>
        <th>{{$t('square')}}</th>
        <th>{{$t('store')}}</th>
        <th>{{$t('camera')}}</th>
        <th>{{$t('image')}}</th>
        <th>{{$t('lastaccess')}}</th>
        <th>{{$t('counting')}}</th>
        <th>{{$t('heatmap')}}</th>
      </tr>
      <tr  v-for="(cam,i) in arr_devices" :key="i">
        <td :style="cam.sq_border">{{ cam.sq_name }}</td>
        <td :style="cam.st_border">{{ cam.st_name }}</td>
        <td>{{ cam.cam_name }}</td>
        <td><img :src="cam.snapshot" width="100"/></td>
        <td>{{ cam.regdate }}</td>
        <td><i :class="cam.enable_countingline"></i></td>
        <td><i :class="cam.enable_heatmap"></i></td>
      </tr>


    </table>
  </div>

</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue';
import axios from 'axios';
import { navStore } from '@/store/nav_store.js';
import { useRouter } from 'vue-router';

const router = useRouter();
const dp = navStore(); // piana

let arr_devices = ref({});

const drawDeviceTree= ((data)=>{
  let arr = new Array();
  const f_checked = 'align-middle fas fa-check mr-1';
  data.forEach((sq,i) => {
    sq.store.forEach((st,j)=>{
      st.camera.forEach((cam, k) => {
        arr.push({
          "sq_name": j == 0 && k == 0 ? sq.name :'',
          "st_name": k == 0 ? st.name : '',
          "cam_name": cam.code,
          "snapshot": cam.snapshot,
          "sq_border": j != 0 || k !=0 ? 'border: 0px solid black':'',
          "st_border":  k !=0 ? 'border: 0px solid black':'',
          "regdate": cam.last_access,
          "enable_countingline": cam.enable_countingline == 'y' ? f_checked : '',
          "enable_heatmap": cam.enable_countingline == 'y' ? f_checked : '',

          });
      });

    });
  })
  arr_devices.value = arr;
});

function getDeviceTree() {
  const url ='/api/query?data=sitemap&fmt=json';
  // console.log(url);
  axios({
    method: 'post',
    url: '/api/query',
    params:{
      data:'sitemap',
    },
    data: {
      format: 'json',
      db_name: dp.db_name,
    },
    header:{"Context-Type": "multipart/form-data"}
  }).then(result => {
    // console.log(result.data);
    if (result.data.code == 403) {
      router.push({ path: '/login'});
      return 0;
    }
    drawDeviceTree(result.data);
  })
  .catch(error => {
      console.log(error);
  });
}

onMounted(() => {
  getDeviceTree();
});
</script>

<style></style>