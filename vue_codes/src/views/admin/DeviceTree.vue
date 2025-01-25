<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="navbar-collapse ">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
      </ul>
      <navLanguage /><navDropdown />
    </div>
  </nav>
  <div class="main">
    <main class="content">
      <div class="container-fluid mt-2">
        <div class="row">
          <div class="col-md-5">
            <TreeView :data="tree_data" @click="handleClick" />
          </div>
          <div class="col-md-7 pos-panel">
            <squareInfo v-if="view_info.square" :square_info="square_info" @update="updateSquare"></squareInfo>
            <storeInfo v-else-if="view_info.store" :store_info="store_info" @update="updateStore"></storeInfo>
            <cameraInfo v-else-if="view_info.camera" :camera_info="camera_info" @update="updateCamera"></cameraInfo>
          </div>
        </div>
      </div>
    </main>
  </div>
  <div v-if="alert.show" :class="`alert alert-${alert.type} alert-dismissible fade show m-3`" role="alert">
      {{ alert.message }}
      <button type="button" class="btn-close" @click="alert.show = false"></button>
  </div>

</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useCookies } from 'vue3-cookies';

import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();

import TreeView from    '@/components/TreeView.vue';
import navLanguage from '@/layout/NavLanguage.vue';
import navDropdown from '@/layout/NavDropdown.vue';
  
import squareInfo from '@/components/SquareInfo.vue';
import storeInfo from  '@/components/StoreInfo.vue';
import cameraInfo from '@/components/CameraInfo.vue';
  
const router = useRouter();
const { cookies } = useCookies();

const alert = ref({
  show: false,
  type: 'warning',  // success, danger, warning, info 등
  message: ''
});


  
const tree_data   = ref([]);
const view_info   = ref({});
const square_info = ref({});
const store_info  = ref({});
const camera_info = ref({});

const active_code = ref('');


const handleClick = (square_code, store_code, camera_code) => {
  view_info.value = {};
  // tree_data.value = JSON.parse(JSON.stringify(tree_data_org));

  // console.log('handleClick', square_code, store_code, camera_code);
  if (square_code && !store_code && !camera_code) {
    showSquareInfo(square_code);
  }
  else if (square_code && store_code && !camera_code) {
    showStoreInfo(square_code, store_code);
  }
  else if (square_code && store_code && camera_code) {
    showCameraInfo(square_code, store_code, camera_code);
  }
}

const updateTree = () => {
  // console.log('updateTree');
  tree_data.value.forEach(item => {
    item.name = item.name_org;
    item.store.forEach(store => {
      store.name = store.name_org;
      store.camera.forEach(camera => {
        camera.name = camera.name_org;
      });
    });
  });
}

const showSquareInfo = (square_code) => {
  view_info.value.square = true;
  if (active_code.value != square_code) {
    updateTree();
  }
  active_code.value = square_code;
  
  square_info.value = tree_data.value.find(item => item.code === square_code);
  square_info.value.isExpanded = true;
  
  if (square_info.value.code == 'new') {
    square_info.value.name = '';
  }
}



const showStoreInfo = (square_code, store_code) => {
  view_info.value.store = true;
  if (active_code.value != store_code) {
    updateTree();
  }
  active_code.value = store_code;

  square_info.value = tree_data.value.find(item => item.code === square_code);
  store_info.value  = square_info.value.store.find(item => item.code === store_code);
  store_info.value.squares = tree_data.value.map(item => ({code: item.code, name: item.name}));
  // store_info.value.square_code = square_code;
  if (store_info.value.code == 'new') {
    store_info.value.name = '';
  }
}

const showCameraInfo = (square_code, store_code, camera_code) => {
  view_info.value.camera = true;
  if (active_code.value != camera_code) {
    updateTree();
  }
  active_code.value = camera_code;

  camera_info.value = tree_data.value.find(item => item.code === square_code).store.find(item => item.code === store_code).camera.find(item => item.code === camera_code);
  camera_info.value.stores = tree_data.value.find(item => item.code === square_code).store.map(item => ({code: item.code, name: item.name}));
  camera_info.value.store_code_org = store_code;
  camera_info.value.square_code_org = square_code;
}

const updateSquare = (data) => {
  // console.log('updateSquare', data);
  if (data == 'cancel') {
    square_info.value.name = square_info.value.name_org;
    view_info.value = {};
    if (square_info.value.code == 'new') {
      square_info.value.name = t('new_square');
    }
    return;
  }
  // console.log(data);
}

const updateStore = (data) => {
  // console.log('updateStore', data);
  if (data == 'cancel') {
    store_info.value.square_code = store_info.value.square_code_org;
    store_info.value.name = store_info.value.name_org;
    view_info.value = {};
    if (store_info.value.code == 'new') {
      store_info.value.name = t('new_store');
    }
    return;
  }
  
  // console.log(data);
}

const updateCamera = () => {
  console.log('updateCamera');
}


function transformPlaceData(data) {
  const result = {};
  data.forEach(item => {
    const squareCode = item.square_code;
    const storeCode  = item.store_code;
    const cameraCode = item.camera_code;

    if (!result[squareCode]) {
      result[squareCode] = {
        code: squareCode,
        name: item.square_name,
        name_org: item.square_name,
        address: item.square_address ? item.square_address : '',
        comment: item.square_comment ? item.square_comment : '',
        store: {},
        isExpanded: false
      };
    }
    if(storeCode){
      if (!result[squareCode].store[storeCode]) {
        result[squareCode].store[storeCode] = {
          code: storeCode,
          name: item.store_name,
          name_org: item.store_name,
          contact: item.store_contact,
          tel: item.store_tel,
          address: item.store_address ? item.store_address : '',
          open_hour: item.store_open_hour ? item.store_open_hour : 0,
          close_hour: item.store_close_hour ? item.store_close_hour : 0,
          comment: item.store_comment ? item.store_comment : '',
          area: item.store_area ? item.store_area : 0,
          sniffing_mac: item.store_sniffing_mac ? item.store_sniffing_mac : '',
          camera: {},
          square_code: squareCode,
          square_code_org: item.square_code,
        };
      }
  
      if(cameraCode){
        if (!result[squareCode].store[storeCode].camera[cameraCode]) {
          result[squareCode].store[storeCode].camera[cameraCode] = {
            code: cameraCode,
            name: item.camera_name,
            name_org: item.camera_name,
            device_info: [],
            square_code: squareCode,
            square_code_org: item.square_code,
            store_code: storeCode,
            store_code_org: item.store_code,
            comment: item.camera_comment ? item.camera_comment : '',
          };
        }

        const deviceInfo = item.device_info;
        if (!result[squareCode].store[storeCode].camera[cameraCode].device_info.includes(deviceInfo)) {
          result[squareCode].store[storeCode].camera[cameraCode].device_info.push(deviceInfo);
        }
      }
    }   
  });
    
  const tree_temp = Object.values(result).map(square => ({
    ...square,
    store: Object.values(square.store).map(store => ({
      ...store,
      camera: Object.values(store.camera)
    }))
  }));

  tree_temp.forEach(item => {
    item.store.forEach(store => {
      store.camera.push({ 
        code: 'new', 
        name: t('new_camera'), 
        name_org: t('new_camera'), 
        device_info: [],
        square_code: item.code,
        square_code_org: item.code,
        store_code: store.code,
        store_code_org: store.code,
        device_info: []
      });
    });
    item.store.push({ 
      code: 'new', 
      name: t('new_store'), 
      name_org: t('new_store'), 
      square_code: item.code, 
      square_code_org: item.code, 
      camera: [] 
    });
  });
  tree_temp.push({ code: 'new', name: t('new_square'), name_org: t('new_square'), store: [] });

  return tree_temp;
}
  
const  getDeviceTree = async() => {
  try {
    const res = await axios({
      method: 'post',
      url: '/api/query',
      params:{ data:'querydb' },
      data: {
        db_name: cookies.get('_db_name'),
        table: 'device_tree',
        filter: {},
        sort: { sq_name: 1 },
        format : 'json'
      },
      header:{"Context-Type": "multipart/form-data"}
    });
    const data = await res.data;
    console.log(data);
    // tree_data.value=data.data;
    if (data.code == 403) {
      router.push({ path: '/login'});
      return 0;
    }
    tree_data.value = transformPlaceData(data.data);
    // console.log(tree_data.value);

  }
  catch(error) {
    console.log(error);
  }
  finally {
    // is_loading.value = false;
  }
}

onMounted(() => {
  getDeviceTree();
});




</script>

<style scoped>
.pos-panel {
  position: fixed;
  right: 0px;
  top: 50%;
  width: 50%;
  transform: translateY(-50%);
  max-height: 90vh;
  overflow-y: auto;
}
</style>
