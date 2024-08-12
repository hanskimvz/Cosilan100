<template>
  <div class="row align-items-center">
    <div class="col-auto" v-if="props.view_by=='daily' || props.view_by=='monthly'">
      <div class="input-group">
        <span type="button" class="btn btn-default" @click="movDate('from', -1)"><i class="bi bi-chevron-left"></i></span>
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
          @closed="sendDataToParent"
        />
        <span type="button" class="btn btn-default" @click="movDate('from', 1)"><i class="bi bi-chevron-right"></i></span>
      </div>
    </div>
    <div class="col" v-if="props.view_by=='daily' || props.view_by=='monthly'">~</div>
    <div class="col-auto" > 
      <div class="input-group">
        <span type="button" class="btn btn-default" @click="movDate('to', -1)" width="10"><i class="bi bi-chevron-left"></i></span>
        <Datepicker 
          v-model="date_range[1]" 
          :locale="locale_t" 
          :weekStartsOn="0" 
          :inputFormat="dateFormat" 
          :size="8"
          :clearable="false" 
          :disabledDates="{ predicate: isTodayOver }"
          :class="'form-control date-input text-center align-middle '" 
          @closed="sendDataToParent"
          
        />
        <span type="button" class="btn btn-default" @click="movDate('to', 1)"><i class="bi bi-chevron-right"></i></span>
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

const date_range = ref([new Date(), new Date()]);

const props = defineProps({
  view_by: String,
  default: 'hourly',
},)

const emit = defineEmits(['dataEvent'])

const sendDataToParent = () => {
  if (props.view_by == 'tenmin' || props.view_by == 'hourly') {
    date_range.value[0] = date_range.value[1] ;
  }  
  else if (props.view_by=='daily'){
    const to   = date_range.value[1];
    const from = date_range.value[0];
    if ( (to.getTime() - from.getTime()) < 3600*24*4*1000) { // 4days} 
      date_range.value[0] =  addDays(to, -4);
    }
  }  
  emit('dataEvent', {'date_range': [getDateString(date_range.value[0]), getDateString(date_range.value[1])]} );
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

watch(() => props.view_by, (newValue, oldValue) => {
  // console.log(newValue)
  sendDataToParent();
}, { immediate: true });


const movDate = (flag, val) => {
  if (flag == 'from') {
    date_range.value[0] = addDays(date_range.value[0], val)
  }  
  else if (flag == 'to') {
    if (isTodayOver(addDays(date_range.value[1], val))) {
      return false;
    }
    date_range.value[1] = addDays(date_range.value[1], val)
  }
  sendDataToParent();
};

onMounted(()=>{
})

</script>

<style scoped>
div {
  text-align: center;
}

div.block {
  display: inline-flex;
}
.date-input {
  margin-left: 0px;
  margin-right: 0px;
  padding-left: 0px;
  padding-right: 0px;
}
</style>