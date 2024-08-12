<template>
  <div class="justify-content-center" style="margin-left:10px; margin-right:10px;">
    <div class="row g-3 align-items-center mb-1" >
      <div class="col-auto">
        <select class="form-select me-2" v-model="sq_code[0]" @change="listStore(0)">
          <option value="0">{{ $t('all_square') }}</option>
          <option v-for="(item, i) in place_data" :key="i" :value="item.code"> {{ item.name }} </option>
        </select>
      </div>
      <div class="col-auto">
        <select class="form-select me-2" v-model="st_code[0]" @change="sendDataToParent">
          <option value="0">{{ $t('all_store') }}</option>
          <option v-for="(item, i) in stores" :key="i" :value="item.code"> {{ item.name }} </option>
        </select>
      </div>

      <div class="col-auto">
        <select class="form-select me-2" v-model="sq_code[1]" @change="listStore(1)">
          <option value="0">{{ $t('all_square') }}</option>
          <option v-for="(item, i) in place_data" :key="i" :value="item.code"> {{ item.name }} </option>
        </select>
      </div>
      <div class="col-auto">
        <select class="form-select me-2" v-model="st_code[1]" @change="sendDataToParent">
          <option value="0">{{ $t('all_store') }}</option>
          <option v-for="(item, i) in stores" :key="i" :value="item.code"> {{ item.name }} </option>
        </select>
      </div>

      <div class="col-auto">
        <select class="form-select me-2" v-model="sq_code[2]" @change="listStore(2)">
          <option value="0">{{ $t('all_square') }}</option>
          <option v-for="(item, i) in place_data" :key="i" :value="item.code"> {{ item.name }} </option>
        </select>
      </div>
      <div class="col-auto">
        <select class="form-select me-2" v-model="st_code[2]" @change="sendDataToParent">
          <option value="0">{{ $t('all_store') }}</option>
          <option v-for="(item, i) in stores" :key="i" :value="item.code"> {{ item.name }} </option>
        </select>
      </div>
    </div>    
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';
import axios from 'axios';

const sq_code = ref([0,0,0]);
const st_code = ref([0,0,0]);
const place_data = ref([]);
const stores = ref([]);

const emit = defineEmits(['dataEvent']);

const listStore = ( (p) =>{
  st_code.value[p] = 0;
  stores.value = [];
  if (sq_code.value[p] =='0') {
    sq_code.value[p] = 0;
  }
  if (sq_code.value[p]) {
    let ps  = place_data.value.filter( item  => {
      return item.code == sq_code.value[p];
    });
    // console.log(ps);
    stores.value = ps[0].store;
  }
  sendDataToParent();
});


const sendDataToParent = () => {
  // console.log([sq_code.value, st_code.value]);
  emit('dataEvent', {'place': [
    [sq_code.value[0], st_code.value[0]],
    [sq_code.value[1], st_code.value[1]],
    [sq_code.value[2], st_code.value[2]],
  ]});
}

onMounted(() => { 
    const url ='/api/query?data=place&fmt=json';
    axios.get(url)
    .then(result => {
      place_data.value = result.data;
      // console.log (place_data.value);
    })
    .catch(error => {
        console.log(error);
    });
  // }
});


</script>

<style scoped>
</style>