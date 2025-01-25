<template>
  <div class="justify-content-center" style="margin-left:10px; margin-right:10px;">
    <div class="row g-3 align-items-center mb-1" >
      <div class="col-auto">
        <select class="form-select me-2" v-model="sq_code" @change="listStore()">
          <option value="0">{{ $t('all_square') }}</option>
          <option v-for="(item, i) in place_data" :key="i" :value="item.code"> {{ item.name }} </option>
        </select>
      </div>
      <div class="col-auto">
        <select class="form-select me-2" v-model="st_code" @change="listCamera()">
          <option value="0">{{ $t('all_store') }}</option>
          <option v-for="(item, i) in stores" :key="i" :value="item.code"> {{ item.name }} </option>
        </select>
      </div>
      <div class="col-auto">
        <select class="form-select me-2" v-model="cam_code" @change="sendDataToParent">
          <option value="0">{{ $t('all_camera') }}</option>
          <option v-for="(item, i) in cameras" :key="i" :value="item.code"> {{ item.name }} </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';
import { useCookies } from 'vue3-cookies';
import axios from 'axios';

const { cookies } = useCookies();
const sq_code = ref(0);
const st_code = ref(0);
const cam_code = ref(0);
const place_data = ref([]);
const stores = ref([]);
const cameras = ref([]);

const emit = defineEmits(['dataEvent']);


const listStore = ( () =>{
  st_code.value = 0;
  stores.value = [];
  if (sq_code.value =='0') {
    sq_code.value =0;
  }
  if (sq_code.value) {
    let ps  = place_data.value.filter( item  => {
      return item.code == sq_code.value;
    });
    // console.log(ps);
    stores.value = ps[0].store;
  }
  sendDataToParent();
});

const listCamera = ( () =>{
  console.log(stores.value);
  cam_code.value = 0;
  cameras.value = [];
  if (st_code.value =='0') {
    st_code.value = 0;
  }

  if (st_code.value) {
    let ps  = stores.value.filter( item  => {
      return item.code == st_code.value;
    });
    // console.log(ps);
    cameras.value = ps[0].camera;
  }
  sendDataToParent();
});



const sendDataToParent = () => {
  // console.log('sendDataToParent', sq_code.value, st_code.value, cam_code.value);
  emit('dataEvent', {'place': [sq_code.value, st_code.value, cam_code.value]});
}

const getDatabaseData = () => {
  const url ='/api/query?data=querydb';
  axios.post(url,   { 
      db_name: cookies.get('_db_name'),
      table: 'device_tree',
      filter: {},
      fields: {},
      orderby: '',
      page_no: 1,
      page_max: 25,
      format : 'json'
    }, 
    { header: {"Context-Type": "multipart/form-data",},}
  )
  .then((res) => {
    console.log(res.data);
    place_data.value = transformPlaceData(res.data.data);

    console.log(place_data.value);
   
  })
  .catch((error) => {
    console.error(error);
  });
}

onMounted(() => { 
  getDatabaseData();
});

function transformPlaceData(data) {
  const result = {};
  data.forEach(item => {
    const squareCode = item.square_code;
    const storeCode = item.store_code;
    const cameraCode = item.camera_code;

    if (!result[squareCode]) {
      result[squareCode] = {
        code: squareCode,
        name: item.square_name,
        store: {}
      };
    }
    if (!result[squareCode].store[storeCode]) {
      result[squareCode].store[storeCode] = {
        code: storeCode,
        name: item.store_name,
        camera: {}
      };
    }
        
    if (!result[squareCode].store[storeCode].camera[cameraCode]) {
      result[squareCode].store[storeCode].camera[cameraCode] = {
        name: item.camera_name,
        code: cameraCode,
        device_info: []
      };
    }
    const deviceInfo = item.device_info;
    if (!result[squareCode].store[storeCode].camera[cameraCode].device_info.includes(deviceInfo)) {
      result[squareCode].store[storeCode].camera[cameraCode].device_info.push(deviceInfo);
    }
  });
  
  return Object.values(result).map(square => ({
    ...square,
    store: Object.values(square.store).map(store => ({
      ...store,
      camera: Object.values(store.camera)
    }))
  }));
}

</script>

<style scoped>
</style>