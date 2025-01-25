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
            <div class="card border col-md-12" style="background-color:#fff;">
              <div class="card-header">
              <div class="card-actions float-right dropdown show mr-2">
                <a href="#" data-toggle="dropdown" data-display="static"><span class="mt-0">&#9661;</span></a>
                <div class="dropdown-menu dropdown-menu-right">
                  <span type="button" data-toggle="modal" data-target="#square_detail" class="dropdown-item" style="padding-bottom:0px; padding-top:0px;"  @click="viewSquareInfo(0)">Add Square</span>
                </div>
              </div>
              <h5 class="card-title mb-0"><b>{{$t('device_tree') }}hello</b></h5>
            </div> 
          </div>
  
  
  
  
      <div v-for="(square, i) in tree_data" :key="i" class="col-md-4 easy-tree">     
        <div class="card" style="background-color:#fff;">
          <div class="card-header alert-success">
            <div class="card-actions float-right dropdown show">
              <a href="#" data-toggle="dropdown" data-display="static">&#8803;</a>
              <div class="dropdown-menu dropdown-menu-right">
                <span type="button" data-toggle="modal" data-target="#store_detail" class="dropdown-item" @click="viewStoreInfo(0)">Add  Store</span>
              </div>
            </div>
            <h5 class="card-title mb-1 mt-0">
              <span type="button" data-toggle="modal" data-target="#square_detail" @click="viewSquareInfo(square.code)"><span class="mr-2">&#127972;</span><b>{{ square.name }}</b></span>
            </h5>
          </div>
          <ul>
            <li v-for="(store, j) in square.store" :key="j">
              <div class="card-header glyphicon mb-0 mt-0 col-md-12" style="background-color:#fdd; padding-bottom:0px;">
                <div class="card-actions float-right dropdown show mr-0 mt-0">
                  <a href="#" data-toggle="dropdown" data-display="static">&#8803;</a>
                  <div class="dropdown-menu dropdown-menu-right">
                    <span type="button" data-toggle="modal" data-target="#detail_device" class="dropdown-item" @click="viewStoreInfo(store.code)">Add device</span>
                  </div>
                </div>
                <h5 class="card-title ml-1 mb-1 mt-0">
                  <span type="button" data-toggle="modal" data-target="#store_detail" @click="viewStoreInfo(store.code)"><span class="mr-2">&#127968;</span><b>{{ store.name }}</b></span>
                </h5>
              </div>
              
                        <ul>
                          <li v-for="(camera, k) in store.camera" :key="k">
                            <div class=" card card-header glyphicon mb-0 mt-0 col-md-10 " style="background-color:#adf; padding-bottom:0px;">
                              <h5 class="card-title ml-1 mb-1 mt-0">
                                <span type="button" data-toggle="modal" data-target="#detail_device" @click="viewCameraInfo(camera.code)">
                                  <i class="fas fa-fw fa-camera"></i><b class="ml-2">{{ camera.name }}</b>
                                </span>
                              </h5>
                            </div>
                          </li>
                        </ul>
  
                      </li>
                    </ul>
      
  
  
        </div>
      </div>
    </div>
  </div></main></div>
  
  
  <!-- square info -->
  <div class="modal fade" id="square_detail" tabindex="-1" role="dialog" aria-hidden="true">
    <squareInfo :square_info="square_info" @update="modifySquare"></squareInfo>
  </div>
  
  <!-- store info -->
  <div class="modal fade" id="store_detail" tabindex="-1" role="dialog" aria-hidden="true">
    <storeInfo  :store_info="store_info" @update="modifyStore"></storeInfo>
  </div>
  
  <!-- device info -->
  <div class="modal fade" id="detail_device" tabindex="-1" role="dialog" aria-hidden="true">
    <cameraInfo :camera_info="camera_info" :counter_label_info="counter_label_info" @update="modifyCamera"></cameraInfo>
  </div> 
  </template>
  
  <script setup>
  import { onMounted, onBeforeUnmount, ref } from 'vue';
  import axios from 'axios';
  // import { navStore } from '@/store/nav_store.js';
  import { useRouter } from 'vue-router';
  import { useCookies } from 'vue3-cookies';
  
  import navLanguage from '@/layout/NavLanguage.vue';
  import navDropdown from '@/layout/NavDropdown.vue';
  
  import squareInfo from '@/components/SquareInfo.vue';
  import storeInfo from '@/components/StoreInfo.vue';
  import cameraInfo from '@/components/CameraInfo.vue';
  
  const router = useRouter();
  const { cookies } = useCookies();
  
  // const dp = navStore(); // piana
  
  const tree_data = ref({});
  
  
  
  const  square_info = ref({
    name: 'square tmep',
    code : '1223432424',
    body: 'sadfasjdfldfjsdl'
  });
  const  store_info = ref({
    name: 'store tmep',
    code : '1223432424',
    body: 'sadfasjdfldfjsdl'
  });
  const  camera_info = ref({});
  const counter_label_info =ref({});
  
  
  const viewSquareInfo = ((sq_code)=>{
    console.log(sq_code);
  
  });
  
  const viewStoreInfo = ((st_code)=>{
    console.log(st_code)
  })
  
  
  const viewCameraInfo = ( (cam_code) =>{
    console.log(cam_code)
    axios({
      method: 'post',
      url: '/api/query',
      params:{
        data:'listdevice',
      },
      data: {
        format: 'json',
        db_name: dp.db_name,
        sq: 0,
        st: 0, 
        cam: [cam_code],
      },
      header:{"Context-Type": "multipart/form-data"}
    }).then(result => {
      // console.log(result.data);
      camera_info.value = result.data.device[0];
      const ex_dev = camera_info.value.device_info.split("&");
      camera_info.value.mac = ex_dev[0].split("=")[1];
      camera_info.value.brand = ex_dev[1].split("=").length >1 ? ex_dev[1].split("=")[1]: '';
      camera_info.value.model = ex_dev[2].split("=").length >1 ? ex_dev[2].split("=")[1]: '';
  
      camera_info.value.enable_countingline = camera_info.value.features.enable_countingline;
      camera_info.value.enable_face_det     = camera_info.value.features.enable_face_det;
      camera_info.value.enable_heatmap      = camera_info.value.features.enable_heatmap;
      camera_info.value.enable_macsniff     = camera_info.value.features.enable_macsniff;
  
      camera_info.value.countrpt = camera_info.value.functions.countrpt;
      camera_info.value.face_det = camera_info.value.functions.face_det;
      camera_info.value.heatmap  = camera_info.value.functions.heatmap;
      camera_info.value.macsniff = camera_info.value.functions.macsniff;
  
      console.log(camera_info.value);
    })
    .catch(error => {
        console.log(error);
    });
  
    axios({
      method: 'post',
      url: '/api/query',
      params:{
        data:'querydb',
      },
      data: {
        db: dp.db_name,
        table: 'counter_label',
        fields: ['counter_name', 'counter_label'],
        search: 'camera_code="' + cam_code + '"',
        page_no: 0,
        page_max: 1000,
        format : 'json'
      },
      header:{"Context-Type": "multipart/form-data"}
    }).then(result => {
      console.log(result.data);
    }).catch(error => {
        console.log(error);
    });
  
  })
  
  
  const modifySquare= (()=>{
    console.log(square_info.value);
  })
  const modifyStore= (()=>{
    console.log(store_info.value);
  })
  
  const modifyCamera= (()=>{
    console.log(camera_info.value);
  })
  
  
  
  let arr_devices = ref({});
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
  
  const drawDeviceTreeX= ((data)=>{
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
  
  
  function transformPlaceData(data) {
    const result = {};
    data.data.forEach(item => {
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
  
  const  getDeviceTree = async() => {
    // const url ='/api/query?data=sitemap&fmt=json';
    // console.log(url);
    try {
      const res = await axios({
        method: 'post',
        url: '/api/query',
        params:{ data:'querydb' },
        data: {
          format: 'json',
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
      tree_data.value = transformPlaceData(data);
      console.log(tree_data.value);
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
  .easy-tree{ min-height:20px; margin-bottom:20px; color:#000;border:0; border-top:0; padding-bottom:15px }
  .easy-tree>ul{ padding-left:10px;  }
  .easy-tree li{ list-style-type:none; margin:0; padding:10px 20px 0;	position:relative}
  .easy-tree li::after,.easy-tree li::before{	content:'';	left:-30px;	position:absolute;	right:auto }
  .easy-tree li::before{ border-left:1px solid #888; bottom:10px; height:100%; top:0;	width:1px }
  .easy-tree li::after{ border-top:1px solid #888; height:3px; top:25px; width:50px; }
  .easy-tree li>span, .easy-tree li>div { -moz-border-radius:5px; -webkit-border-radius:5px; border:1px solid #add; border-radius:5px; display:inline-block; padding:5px 8px;min-width:200px; min-height:10px; text-decoration:none; background-color:#add;}
  .easy-tree li.parent_li>div{ cursor:pointer	}
  .easy-tree>ul>li::after,.easy-tree>ul>li::before{ border:0 }
  .easy-tree li:last-child::before{ height:26px }
  .easy-tree li>span>a{ color:#111; text-decoration:none}
  </style>