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
        <select class="form-select me-2" v-model="st_code" @change="sendDataToParent">
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

const sq_code = ref(0);
const st_code = ref(0);
const place_data = ref([]);
const stores = ref([]);

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


const sendDataToParent = () => {
  emit('dataEvent', {'place': [sq_code.value, st_code.value]});
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