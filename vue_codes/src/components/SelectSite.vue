<template>
  <div v-show="!($route.path == '/sitemap' || $route.path == '/about')" class="block">
    <div class="form-inline d-none d-sm-inline-block">
      <select class="form-control mr-sm-2" id="square" v-model="place.sq_code" @change="listStore('#store')">
        <option value=0>{{$t('all_square')}}</option>
      </select>
      <select class="form-control mr-sm-2" id="store" v-model="place.st_code">
        <option value=0>{{$t('all_store')}}</option>
      </select>
    </div>
    <div v-show="$route.path==='/comparebyplace'">
      <div class="form-inline d-none d-sm-inline-block " >
        <select class="form-control mr-sm-2" id="square1" v-model="place.sq_code1"  @change="listStore('#store1')">
          <option value=0>{{$t('all_square')}}</option>
        </select>
        <select class="form-control mr-sm-2" id="store1" v-model="place.st_code1">
          <option value=0>{{$t('all_store')}}</option>
        </select>
      </div>
      <div class="form-inline d-none d-sm-inline-block ">
        <select class="form-control mr-sm-2" id="square2" v-model="place.sq_code2" @change="listStore('#store2')">
          <option value=0>{{$t('all_square')}}</option>
        </select>
        <select class="form-control mr-sm-2" id="store2" v-model="place.st_code2">
          <option value=0>{{$t('all_store')}}</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { navStore } from '@/store/nav_store.js'
import axios from 'axios';
// import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const place =  navStore();
// const route =  useRoute()

// let disp = ref(true);
let place_data = [];

const listSquare= ((id)=>{
  $(id).empty().append($('<option>', {value: 0, text:t('all_square')}));
    place_data.forEach(function(item, index) {
    $(id).append($('<option>', {value: item.code, text:item.name}))
  });
});

const listStore = ( (store_id) =>{
  $(store_id).empty().append($('<option>', {value: 0, text:t('all_store')}));
  let sss;
  if (store_id == '#store'){
    sss = place.sq_code;
    place.st_code = 0;
  }
  else if (store_id == '#store1'){
    sss = place.sq_code1;
    place.st_code1 = 0;
  }
  else if (store_id == '#store2'){
    sss = place.sq_code2;
    place.st_code2 = 0;
  }
  
  place_data.forEach( function(item, index) {
    if (item.code == sss)  {
      item.store.forEach (function (it) {
        $(store_id).append($('<option>', {value: it.code, text:it.name}))
      })
    }
  });
});


onMounted(() => { 
  // console.log (place_data.length)
  if (!place.place_data.length) {
    const url ='/api/query?data=place&fmt=json';
    axios.get(url)
    .then(result => {
      place_data = result.data;
      // console.log (place_data)
      listSquare('#square');
      listSquare('#square1');
      listSquare('#square2');
    })
    .catch(error => {
        console.log(error);
    });
  }
});



// setTimeout(()=>{
//   listSquare('#square1');
//   listSquare('#square2');
//   console.log('timeout')
// }, 2000);

// onUpdated (()=> {
//   console.log(place_data);
//   // listSquare('#square');
//   listSquare('#square1');
//   listSquare('#square2');
// });

</script>

<style scoped>
div {
  text-align: center;
}

div.block {
  display: inline-flex;
}
</style>