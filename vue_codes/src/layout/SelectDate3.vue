<template>
<div class="row align-items-center">
    <div class="col-auto">
      <div class="input-group">
        <span type="button" class="btn btn-default" @click="movDate(0, -1)"><i class="bi bi-chevron-left"></i></span>
          <Datepicker 
          v-model="date_range[0]" 
          :locale="locale_t" 
          :weekStartsOn="0" 
          :inputFormat="dateFormat" 
          :size="8"
          :clearable="false" 
          :allowOutsideInterval="false" 
          :disabledDates="{ predicate: isTodayOver }" 
          :class="'form-control text-center align-middle'"
          @closed="sendDataToParent(0)"
        />
        <span type="button" class="btn btn-default" @click="movDate(0, 1)"><i class="bi bi-chevron-right"></i></span>
      </div>
    </div>
    <div class="col-auto" > 
      <div class="input-group">
        <span type="button" class="btn btn-default" @click="movDate(1, -1)" width="10"><i class="bi bi-chevron-left"></i></span>
        <Datepicker 
          v-model="date_range[1]" 
          :locale="locale_t" 
          :weekStartsOn="0" 
          :inputFormat="dateFormat" 
          :size="8"
          :clearable="false" 
          :disabledDates="{ predicate: isTodayOver }"
          :class="'form-control date-input text-center align-middle '" 
          @closed="sendDataToParent(1)"
        />
        <span type="button" class="btn btn-default" @click="movDate(1, 1)"><i class="bi bi-chevron-right"></i></span>
      </div>
    </div>
    <div class="col-auto" > 
      <div class="input-group">
        <span type="button" class="btn btn-default" @click="movDate(2, -1)" width="10"><i class="bi bi-chevron-left"></i></span>
        <Datepicker 
          v-model="date_range[2]" 
          :locale="locale_t" 
          :weekStartsOn="0" 
          :inputFormat="dateFormat" 
          :size="8"
          :clearable="false" 
          :disabledDates="{ predicate: isTodayOver }"
          :class="'form-control date-input text-center align-middle '" 
          @closed="sendDataToParent(2)"
        />
        <span type="button" class="btn btn-default" @click="movDate(2, 1)"><i class="bi bi-chevron-right"></i></span>
      </div>
    </div>    
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router'
import Datepicker from 'vue3-datepicker';
import { ko, enUS, zhCN } from 'date-fns/locale'
import { useI18n } from 'vue-i18n';

import { _tz_offset, getDateString, addDays } from '@/assets/functions.js';

const { locale } = useI18n();
const locale_t = ref(ko);
const dateFormat = ref('yyyy-MM-dd');

const date_range = ref([new Date(), addDays(new Date(), -7), addDays(new Date(),-14)]);

const emit = defineEmits(['dataEvent'])

const sendDataToParent = (ch) => {
  emit('dataEvent', {
    'date_range': [getDateString(date_range.value[0]), getDateString(date_range.value[1]), getDateString(date_range.value[2])],
    'channel': ch
  });
}

const locale_s = {
  'kor': ko,
  'eng': enUS,
  'chi': zhCN
}

locale_t.value = locale_s[locale.value];

const isTodayOver = (date) => {
  return date > new Date();
};

const route = useRoute();
watch([locale], (n,o)=> {
//  console.log(o, n);
  locale_t.value = locale_s[locale.value];
});


const movDate = (flag, val) => {
  if (isTodayOver(addDays(date_range.value[flag], val))) {
    return false;
  }
  date_range.value[flag] = addDays(date_range.value[flag], val)
  sendDataToParent(flag);
};

onMounted(()=>{
})




// import { ref, reactive, watch, onMounted } from 'vue';
// import { navStore } from '@/store/nav_store.js'
// import { useRoute } from 'vue-router'
// import Datepicker from 'vue3-datepicker';
// import { ko, enUS, zhCN } from 'date-fns/locale'
// import { useI18n } from 'vue-i18n';
// const { locale } = useI18n();
// const locale_t = ref(ko);
// if (locale.value == 'kor') {
//   locale_t.value = ko;
// }
// else if (locale.value == 'eng') {
//   locale_t.value = enUS;
// }
// else if (locale.value == 'chi') {
//   locale_t.value = zhCN;
// }
// const dateFormat = ref('yyyy-MM-dd');

// let dr = navStore();

// const isTodayOver = (date) => {
//   return date > new Date();
// };

// const route = useRoute();
// watch([route, locale], (o,n)=> {
//   // console.log(route.path)
//   validateDisplay(route.path);
//   if (locale.value == 'kor') {
//     locale_t.value = ko;
//   }
//   else if (locale.value == 'eng') {
//     locale_t.value = enUS;
//   }
//   else if (locale.value == 'chi') {
//     locale_t.value = zhCN;
//   }  
// });

// const disp = ref({
//   view_by: false,
//   view_on: false,
//   date_from: false,
//   date_to: false,
//   date_to1: false,
//   date_to2: false
// });

// const validateDisplay = ((path)=>{
//   if (['/dataglunt', '/trendanalysis', '/advancedanalysis','/comparebylabel', '/comparebyplace'].includes(path)) {
//     disp.value.view_by = true;
//     disp.value.view_on = false;
//     disp.value.date_from = ['daily', 'monthly'].includes(dr.view_by) ? true : false;
//     disp.value.date_to = true;
//     disp.value.date_to1 = false;
//     disp.value.date_to2 = false;
//   }
//   else if (path == '/recentdata') {
//     disp.value.view_by = false;
//     disp.value.view_on = true;
//     disp.value.date_from = false;
//     disp.value.date_to = true;
//     disp.value.date_to1 = false;
//     disp.value.date_to2 = false;
//   }  
//   else if (path == '/comparebytime') {
//     disp.value.view_by = false;
//     disp.value.view_on = false;
//     disp.value.date_from = false;
//     disp.value.date_to = true;
//     disp.value.date_to1 = true;
//     disp.value.date_to2 = true;
//   }
//   else if (path == '/trafficdistribution') {
//     disp.value.view_by = false;
//     disp.value.view_on = false;
//     disp.value.date_from = true;
//     disp.value.date_to = true;
//     disp.value.date_to1 = false;
//     disp.value.date_to2 = false;
//   }        
//   else {
//     disp.value.view_by = false;
//     disp.value.view_on = false;
//     disp.value.date_from = false;
//     disp.value.date_to = false;
//     disp.value.date_to1 = false;
//     disp.value.date_to2 = false;
//   }
// });
// // validateDisplay(route.path);
// //  || $route.path=='/trendanalysis' || $route.path=='/advancedanalysis' || $route.path=='/comparebylabel'))



// function addDays(date, days) {
//   const clone = new Date(date);
//   clone.setDate(date.getDate() + days)
//   return clone;
// }

// const movDate = (flag, val) => {
//   if (flag == 'from') {
//     dr.date_from = addDays(dr.date_from, val)
//   }  
//   else if (flag == 'to') {
//     dr.date_to = addDays(dr.date_to, val)
//   }
//   else if (flag == 'to1') {
//     dr.date_to1 = addDays(dr.date_to1, val)
//   }
//   else if (flag == 'to2') {
//     dr.date_to2 = addDays(dr.date_to2, val)
//   }  
// };

// const changeViewBy = ((v) => {
//   dr.view_by = v;
//   validateDisplay(route.path);
//   if (dr.view_by == 'daily' && dr.date_from >= dr.date_to) {
//     dr.date_from = addDays(dr.date_to, -7)
//   }
//   else if (dr.view_by == 'monthly' && dr.date_from >= dr.date_to){
//     dr.date_from = addDays(dr.date_to, -7*30)
//   }

// });

// onMounted(()=>{
//   validateDisplay(route.path);
// })

</script>

<style scoped>
div {
  text-align: center;
}

div.block {
  display: inline-flex;
}
</style>