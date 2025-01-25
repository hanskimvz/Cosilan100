<template>
  <div class="card-header">
    <h5><b>{{ device_info }}</b></h5>
  </div>
  <div class="card-body">
    <div class="row">
      <canvas id="zone_id" width="700" height="350" class="text-center" ></canvas>
    </div>
    <div class="row">
      <div v-for="item in info_data" class="col-md-3">
        <div v-if="item.type == 'text' && item.key != 'comment'" class="form-group">
          <label class="col-form-label">{{ $t(item.key) }}</label>
          <input type="text" v-model="item.value" class="form-control form-control-sm" :readonly="item.readonly" disabled>
        </div>
        <div v-else-if="item.type == 'checkbox'" class="form-group">
          <label class="col-form-label d-flex">
            <input type="checkbox" v-model="item.value" class="form-check-input me-2" :checked="item.value" disabled>{{ $t(item.key) }}
          </label>
        </div>
        <div v-else-if="item.type == 'switch'" class="form-group">
          <label class="col-form-label d-flex">
            <input type="checkbox" v-model="item.value" class="form-check-input me-2" :checked="item.value">{{ $t(item.key) }}
          </label>
        </div>
      </div>
    </div>
    <div class="row">
      <div v-for="item in feature_data" class="col-md-3">
        <div v-if="item.type == 'checkbox'" class="form-group">
          <label class="col-form-label d-flex">
            <input type="checkbox" v-model="item.value" class="form-check-input me-2" :checked="item.value" disabled>{{ $t(item.key) }}
          </label>
        </div>
      </div>
    </div>
    <div class="row">
      <div v-for="item in function_data" class="col-md-3">
        <div v-if="item.type == 'switch'" class="form-group">
          <label class="col-form-label d-flex">
            <div class="form-check form-switch">
              <input class="form-check-input" type="checkbox" role="switch" v-model="item.value">
            </div>
            {{ $t(item.key) }}
          </label>
        </div>
      </div>
    </div>    
    <div class="row">
      <div  v-for="itemx in function_data" v-show="itemx.key == 'enable_countrpt' && itemx.value==true" class="col-md-12">
        <table class="table table-striped table-sm table-bordered">
          <tr>
            <th>{{ $t('counter_name') }}</th>
            <th>{{ $t('counter_label') }}</th>
          </tr>
          <tr  v-for="(item, i) in ctNames" :key="i">
            <td>{{ item.name }}</td>
            <td>
              <select class="form-control" v-model="item.label">
                <option v-for="label in ctLabels" :value="label">{{ t(label) }}</option>
              </select>
            </td>
          </tr>
        </table>
      </div>
    </div>
    <div class="card-footer d-flex justify-content-between">
      <div class="float-left">
        <button class="btn btn-sm btn-warning" @click="document.getElementById('delete_pad').style.display='block';">{{ $t('delete') }}</button>
      </div>
      <div class="float-right">
        <button class="btn btn-primary me-4" @click="update">{{ $t('save') }}</button>
        <button class="btn btn-secondary" @click="cancel">{{ $t('cancel') }}</button>
      </div>
    </div>
  </div>
  
  
  </template>
  
<script setup>
import { ref, reactive, defineProps, defineEmits, watch, onMounted } from "vue";
import axios from 'axios';
import { useI18n } from "vue-i18n";
import { useCookies } from "vue3-cookies";

const props = defineProps(["device_info"]);
const emit = defineEmits(["update"]);

const { t } = useI18n();
const { cookies } = useCookies();



const info_data = reactive([
  { key: 'mac',                 value: '', type:'text',     readonly: true },
  { key: 'brand',               value: '', type:'text',     readonly: true },
  { key: 'model',               value: '', type:'text',     readonly: true },
  { key: 'usn',                 value: '', type:'text',     readonly: true },
  { key: 'product_id',          value: '', type:'text',     readonly: true },
  { key: 'initial_access',      value: '', type:'text',     readonly: true },
  { key: 'last_access',         value: '', type:'text',     readonly: true },
  { key: 'license',             value: '', type:'text',     readonly: true },
  { key: 'comment',             value: '', type:'text',     readonly: true },
]);

const feature_data = reactive([
  { key: 'countrpt',            value: false, type:'checkbox',   readonly: true },
  { key: 'face_det',            value: false, type:'checkbox',   readonly: true },
  { key: 'heatmap',             value: false, type:'checkbox',   readonly: true },
  { key: 'macsniff',            value: false, type:'checkbox',   readonly: true },
]);

const function_data = reactive([
  { key: 'enable_countrpt',            value: false, type:'switch',   readonly: true },
  { key: 'enable_face_det',            value: false, type:'switch',   readonly: true },
  { key: 'enable_heatmap',             value: false, type:'switch',   readonly: true },
  { key: 'enable_macsniff',            value: false, type:'switch',   readonly: true },
]);
const ctNames = ref([]);
const ctLabels = ref(['entrance','exit','outside','none']);
const form_data = ref({});


watch([props,],(o,n)=>{
  // console.log(o,n)
  getCameraParams(props.device_info);
  // const z = document.getElementById("zone_id");
  // display_counter_label.value = props.camera_info.enable_countingline;
  // draw_zone(z, props.camera_info.zone_info, props.camera_info.snapshot.body);
})
  
  
function draw_zone(id, zone, img_src) {
  // console.log(zone);
  const context = id.getContext("2d");
  const img = new Image();
  const width = 600; 
  const height = 320;

  id.width = width;
  id.height =  height;

  let p_xy;
  let P = new Array();
  let x = new Array();
  let y = new Array();
  
  img.src = img_src;
  context.clearRect(0, 0, width, height);
  img.onload = () => {
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
  }}
}
      

const getZoneFromParams = (params) => {
  let zone = [];
  let i = 0;
  const lines = params.split('\n');
  
  lines.forEach(line => {
    if(line.match(/(VCA.Ch0.Zn)[0-9]/)) {
      const [key, val] = line.split('=');
      const ex_key = key.split('.');
      
      if(zone[i] && zone[i][ex_key[3]]) {
        i++;
      }
      
      if(!zone[i]) {
        zone[i] = {};
      }
      
      zone[i][ex_key[3]] = val.trim();
    }
  });
  
  return zone;
}
      

const getCountersFromParam = async (param) => {
  const ctName = [];
  const lines = param.split('\n');
  
  lines.forEach(line => {
    if(line.match(/(VCA.Ch0.Ct)[0-9](.name=)[a-zA-Z]+/)) {
      const [key, val] = line.split('=');
      const trimmedVal = val.trim();
      if(trimmedVal) {
        ctName.push({name:trimmedVal, label:'none'});
      }
    }
  });


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
        fields: ['device_info', 'counter_name', 'counter_label'],
        filter: {},
        format : 'json'
      },
      headers:{"Context-Type": "multipart/form-data"}
    })
    const data = await res.data;
    console.log('data', data);
    data.data.forEach(item => {
      if (item.device_info == props.device_info) {  
        ctName.forEach(ct => {
          if (ct.name == item.counter_name) {
            ct.label = item.counter_label;
            ct.label_org = item.counter_label;
          }
        })
      }
      if (item.counter_label && !ctLabels.value.includes(item.counter_label)) {
        ctLabels.value.push(item.counter_label);
      }      
    })
    // console.log('ctLabels', ctLabels.value);
    return ctName;
  }
  catch(error) {
    console.log(error);
  } 
  finally {
    // is_loading.value = false;
  }
  
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
        table: 'params',
        filter: { device_info: device_info },
        // fields: ['device_info', 'db_name','ip', 'port', 'device_family', 'flag', 'mac', 'brand', 'model', 'ip4mode', 'ip4address_dhcp', 'param', 'snapshot'],
        format : 'json'
      },
      headers:{"Context-Type": "multipart/form-data"}
    });
    const data = await res.data;
    console.log(data);
    if (data.code == 403) {
      router.push({ path: '/login'});
      return 0;
    }
    let snapshot = data.data[0]['snapshot'];
    let param = data.data[0]['param'];

    info_data.forEach( (item)=>{
      item.value = data.data[0][item.key];
      if (item.key == 'license') {
        let arr=[];
        if (data.data[0]['lic_pro'] == 'y') {
            data.data[0]['lic_pro'] = true;
        }
        if (data.data[0]['lic_pro'] == 'n') {
            data.data[0]['lic_pro'] = false;
        }
        if (data.data[0]['lic_count'] == 'y') {
            data.data[0]['lic_count'] = true;
        }
        if (data.data[0]['lic_count'] == 'n') {
            data.data[0]['lic_count'] = false;
        }
        if (data.data[0]['lic_surv'] == 'y') {
            data.data[0]['lic_surv'] = true;
        }
        if (data.data[0]['lic_surv'] == 'n') {
            data.data[0]['lic_surv'] = false;
        }
        if (data.data[0]['lic_pro']) {
          arr.push('PRO');
        }          
        if (data.data[0]['lic_count']) {
          arr.push('COUNT');
        }
        if (data.data[0]['lic_surv']) {
          arr.push('SURV');
        }
        item.value = arr.join(', ');
      }        
    })
    feature_data.forEach( (item)=>{
      item.value = data.data[0][item.key];
      if (item.value == 'y') {
        item.value = true;
      }
      if (item.value == 'n') {
        item.value = false;
      }        

    })
    function_data.forEach( (item)=>{
      item.value = data.data[0][item.key];
      if (item.value == 'y') {
        item.value = true;
      }
      if (item.value == 'n') {
        item.value = false;
      }        
    })

    const z = document.getElementById("zone_id");
    const zone = getZoneFromParams(param);
    // console.log(zone);
    draw_zone(z, zone, snapshot);
    ctNames.value = await getCountersFromParam(param);
    // console.log('ctNames', ctNames.value);
    }
    catch(error) {
      console.log(error);
    }
    finally {
      // is_loading.value = false;
    }
  }  



const update = () =>{
  console.log('device_info', props.device_info);
  console.log('info_data', info_data);
  console.log('function_data', function_data);
  console.log('ctNames', ctNames.value);
  let arr_ctNames = [];
  ctNames.value.forEach( (item)=>{
    if (item.label_org != item.label) {
      arr_ctNames.push(item);
    }
  })
  form_data.value = {
    filter: { device_info: props.device_info },
    update: {
      function_data: function_data,
      ctNames: arr_ctNames,
    },
    db_name: cookies.get('_db_name'),
    table: 'device_tree',
    id: cookies.get('_login_id'),
    role: cookies.get('_role'),
    format : 'json'
  }
  console.log('form_data', form_data.value);
  update_params();
  emit("update")
}  
  
const update_params = async ()=>{
  console.log('update_params');
}

const cancel = (()=>{
  getCameraParams(props.device_info);
})

  
  onMounted (()=>{
    getCameraParams(props.device_info);
  })
  </script>
  
  <style scoped>
  .card {
    margin-top: 60px;
    margin-left: 0px;
    margin-right: 20px;
  }
  </style>
  