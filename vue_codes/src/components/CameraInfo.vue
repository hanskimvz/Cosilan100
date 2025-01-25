<template>
  <div class="card">
    <div class="card-header">
      <h3 id="modal_device_info"><b>{{ $t('camera_info') }}</b></h3>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-4">
          <label class="col-form-label">{{ $t('code') }}</label>
          <input type="text" v-model="camera_info.code" class="form-control" readonly>
        </div>
        <div class="col-md-4">
          <label class="col-form-label">{{ $t('name') }}</label>
          <input type="text" v-model="camera_info.name" class="form-control">
        </div>
        <div class="col-md-4">
          <label  class="col-form-label">{{ $t('store_group') }}</label>
          <select v-model="camera_info.store_code" class="form-control">
            <option v-for="store in camera_info.stores" :value="store.code">{{ store.name }}</option>
          </select>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <label class="col-form-label">{{ $t('comment') }}</label>
          <textarea v-model="camera_info.comment" class="form-control"></textarea>
        </div>
      </div>
    </div>
    <div v-for="device in camera_info.device_info" class="card-body">
      <CameraDetail :device_info="device" @update="update" />
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch, onMounted } from "vue";
import axios from 'axios';
import { useI18n } from "vue-i18n";
import { useCookies } from "vue3-cookies";


import CameraDetail from './CameraDetail.vue';

const props = defineProps(["camera_info"]);
const emit = defineEmits(["update"]);

const { t } = useI18n();
const { cookies } = useCookies();

const update = () =>{
  console.log('update', props.camera_info)

  if ((props.camera_info.name != props.camera_info.name_org) || (props.camera_info.store_code != props.camera_info.store_code_org)) {
    updateCameraParams();
  }

  if (props.camera_info.store_code != props.camera_info.store_code_org) {
    console.log('store_code changed', props.camera_info.store_code)
    // need to data update, count_tenmin, count_hour, count_day, count_week, count_month, count_year
  }
}

  

const updateCameraParams = () => {
  console.log('updateCameraParams', props.camera_info)
}

const getCameraParams = async (device_info) => {
  if (!device_info) {
    return 0;
  }
  console.log(device_info)
  // return 0;
  try {
    const res = await axios({
      method: 'post',
      url: '/api/query',
      params:{ data:'querydb' },
      data: {
        db_name: cookies.get('_db_name'),
        role: cookies.get('_role'),
        id: cookies.get('_login_id'),
        table: 'device_tree',
        filter: { device_info: device_info },
        fields: ['device_info', 'db_name','ip', 'port', 'device_family', 'flag', 'mac', 'brand', 'model', 'ip4mode', 'ip4address_dhcp', 'param', 'snapshot'],
        format : 'json'
      },
      header:{"Context-Type": "multipart/form-data"}
    });
    const data = await res.data;
    console.log(data);
    if (data.code == 403) {
      router.push({ path: '/login'});
      return 0;
    }
    // const z = document.getElementById("zone_id");
    // draw_zone(z,[], data.data[0].snapshot);

  }
  catch(error) {
    console.log(error);
  }
  finally {
    // is_loading.value = false;
  }
}  

onMounted (()=>{
  // getCameraParams(props.camera_info.device_info[0]);
})
</script>

<style scoped>
.card {
  margin-top: 60px;
  margin-left: 0px;
  margin-right: 20px;
}
</style>
