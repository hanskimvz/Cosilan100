<!--
  현재까지 진도.
  update 함수 작성 안됨.
  카메라 카운터 불러와서 표로 작성하는 부분 아직 안됨.

-->

<template>
  <div class="modal-dialog modal-xl" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h3 id="modal_device_info"><b>{{ $t('camera_info') }}</b></h3>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body m-0">
        <div class="row mb-0">
          <div class="col-md-8">
            <canvas id="zone_id" width="700" height="350" class="text-center" ></canvas>
            
            <div class="row">
              <div class="form-group col-md-4">
                <label class="col-form-label">{{ $t('code') }}</label>
                <input type="text" v-model="camera_info.camera_code" class="form-control" readonly>
              </div>
              <div class="form-group col-md-4">
                <label class="col-form-label">{{ $t('name') }}</label>
                <input type="text" v-model="camera_info.camera_name" class="form-control">
              </div>
              <div class="form-group col-md-4">
                <label>{{ $t('store_group') }}</label>
                <select id="store_code" class="form-control">
                  <option value="ST1547978776435" selected>ST1547978776435: SDW</option>
                </select>
              </div>
              <div class="form-group col-md-12 mt-0">
                <label>{{ $t('feature') }}</label>
                <div class="form-group mb-0">
                    <label class="form-check-inline col-md-2">
                        <input class="form-check-input" type="checkbox" v-model="camera_info.enable_countingline" @change="display_counter_label = camera_info.enable_countingline? true: false" :disabled="!camera_info.countrpt">{{ $t('counting') }}
                    </label>
                    <label class="form-check-inline col-md-2">
                        <input class="form-check-input" type="checkbox"  v-model="camera_info.enable_heatmap" :disabled="!camera_info.heatmap">{{ $t('heatmap') }}
                    </label>
                    <label class="form-check-inline col-md-2">
                        <input class="form-check-input" type="checkbox" v-model="camera_info.enable_face_det" :disabled="!camera_info.face_det">{{ $t('age_gender') }}
                    </label>
                    <label class="form-check-inline col-md-2">
                        <input class="form-check-input" type="checkbox" v-model="camera_info.enable_macsniff" :disabled="!camera_info.macsniff">{{ $t('macsniff') }}
                    </label>
                    <label class="form-check-inline col-md-2">
                        <input class="form-check-input" type="checkbox" v-model="camera_info.flag">{{ $t('activate') }}
                    </label>
                </div>
            </div>
            <div v-show="display_counter_label" class="col-md-12">
              <table class="table table-striped table-sm table-bordered">
                <tr>
                  <th>{{ $t('counter_name') }}</th>
                  <th>{{ $t('counter_label') }}</th>
                </tr>
                <tr>
                  <td>in</td>
                  <td>
                    <select id="in" class="form-control">
                      <option value="none">None</option>
                      <option value="entrance" selected>Entrance</option>
                      <option value="exit">Exit</option>
                      <option value="outside">Outside</option>
                    </select>
                  </td>
                    </tr>
                    <tr>
                        <td>out</td>
                        <td>
                            <select id="out" class="form-control">
                                <option value="none">None</option>
                                <option value="entrance">Entrance</option>
                                <option value="exit" selected>Exit</option>
                                <option value="outside">Outside</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>Counter 0</td>
                        <td>
                            <select id="Counter 0" class="form-control">
                                <option value="none">None</option>
                                <option value="entrance" selected>Entrance</option>
                                <option value="exit">Exit</option>
                                <option value="outside">Outside</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>Counter 1</td>
                        <td>
                            <select id="Counter 1" class="form-control">
                                <option value="none">None</option>
                                <option value="entrance">Entrance</option>
                                <option value="exit" selected>Exit</option>
                                <option value="outside">Outside</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>Counter 3</td>
                        <td>
                            <select id="Counter 3" class="form-control">
                                <option value="none" selected>None</option>
                                <option value="entrance">Entrance</option>
                                <option value="exit">Exit</option>
                                <option value="outside">Outside</option>
                            </select>
                        </td>
                    </tr>
                </table>
            </div>
            <div class="form-group col-md-12">
              <label>{{ $t('comment') }}</label>
              <textarea id="comment" class="form-control"></textarea>
            </div>

            </div>
        </div>
        <div class="col-md-4">
          <div class="form-group">
              <label class="col-form-label">{{ $t('mac') }}</label>
              <input type="text" v-model="camera_info.mac" class="form-control form-control-sm" readonly>
          </div>
          <div class="form-group">
              <label class="col-form-label">{{ $t('brand') }}</label>
              <input type="text" v-model="camera_info.brand" class="form-control form-control-sm" readonly>
          </div>
          <div class="form-group">
              <label class="col-form-label">{{ $t('model') }}</label>
              <input type="text" v-model="camera_info.model" class="form-control form-control-sm" readonly>
          </div>
          <div class="form-group">
              <label class="col-form-label">{{ $t('usn') }}</label>
              <input type="text" v-model="camera_info.usn" class="form-control form-control-sm" readonly>
          </div>
          <div class="form-group">
              <label class="col-form-label">{{ $t('productid') }}</label>
              <input type="text" v-model="camera_info.product_id" class="form-control form-control-sm" readonly>
          </div>
          <div class="form-group">
              <label class="col-form-label">{{ $t('installdate') }}</label>
              <input type="text" v-model="camera_info.initial_access" class="form-control form-control-sm" readonly>
          </div>
          <div class="form-group">
              <label class="col-form-label">{{ $t('lastaccess') }}</label>
              <input type="text" v-model="camera_info.last_access" class="form-control form-control-sm" readonly>
          </div>
          <div class="form-group">
              <label class="col-form-label">{{ $t('license') }}</label>
              <input type="text" v-model="camera_info.license" class="form-control form-control-sm" readonly>
          </div>
          <div class="form-group">
            <label>{{ $t('function') }}</label> 
            <div class="form-group mb-0">
              <label class="form-check-inline ml-2"><span class="mr-2">{{ camera_info.countrpt ? '&#10003;':'&#10005' }}</span>{{ $t('count_db') }}</label><br />
              <label class="form-check-inline ml-2"><span class="mr-2">{{ camera_info.heatmap  ? '&#10003;':'&#10005' }}</span>{{ $t('heatmap') }}</label><br />
              <label class="form-check-inline ml-2"><span class="mr-2">{{ camera_info.face_det ? '&#10003;':'&#10005' }}</span>{{ $t('face') }}</label><br />
              <label class="form-check-inline ml-2"><span class="mr-2">{{ camera_info.macsniff ? '&#10003;':'&#10005' }}</span>{{ $t('macsniff') }}</label>
            </div>
          </div>
        </div>
      </div>

      <div class="float-right">
        <button class="btn btn-sm btn-warning" @click="document.getElementById('delete_pad').style.display='block';">{{ $t('delete') }}</button>
      </div>
      <div class="text-center">
        <button class="btn btn-primary" @click="update">{{ $t('save') }}</button>
      </div>
    </div>
  </div>
</div>

</template>

<script setup>
import { ref, defineProps, defineEmits, watch, onMounted } from "vue";

const props = defineProps(["camera_info", "counter_label_info"]);
const emit = defineEmits(["update"]);

const display_counter_label = ref(false);

const update = (() =>{
  emit("update")
})



watch([props],(o,n)=>{
  console.log(o,n)
  const z = document.getElementById("zone_id");
  display_counter_label.value = props.camera_info.enable_countingline;
  draw_zone(z, props.camera_info.zone_info, props.camera_info.snapshot.body);
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



onMounted (()=>{
})
</script>