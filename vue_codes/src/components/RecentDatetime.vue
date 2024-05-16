<template>
  <div class="form-inline d-none d-sm-inline-block">
    <button class="btn mr-sm-1" :class="view_by == '7days' ? 'btn btn-secondary ': ''" @click="changeDate('tenmin')">최근7일</button>
    <button class="btn mr-sm-1" :class="view_by == '4weeks' ? 'btn btn-secondary ': ''"@click="changeDate('hourly')">최근4주</button>
    <button class="btn mr-sm-1" :class="view_by == '12weeks' ? 'btn btn-secondary ': ''"@click="changeDate('daily')">최근12주</button>
  </div>
  
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import {date_from, date_to, load_time, view_by} from '@/components/global.js';
import Datepicker from 'vue3-datepicker';

// import { defineRefs } from './utils/helper.js';
import axios from 'axios';

import { ko, enUS, zhCN } from 'date-fns/locale'
const locale = reactive(ko);
const dateFormat = ref('yyyy-MM-dd');

const isTodayOver = (date) => {
  return date > new Date();
};


const view_date_from = ref(false);
const date_from_ref = ref(new Date())
const date_to_ref = ref(new Date())



function addDays(date, days) {
  const clone = new Date(date);
  clone.setDate(date.getDate() + days)
  return clone;
}

const getDate = ( (date)=> {
  let y = date.getFullYear();
  let m = date.getMonth() + 1;
  if (m<10) {
    m = '0'+ m
  }
  let d = date.getDate();
  if (d<10) {
    d = '0'+ d
  }  
  return (y+"-"+m+"-"+d)
});

const modDate = (flag, val) =>{
  if (flag == 'from') {
    date_from_ref.value = addDays(date_from_ref.value, val)
  }
  else if (flag=='to'){
    date_to_ref.value = addDays(date_to_ref.value, val)
  }
  // console.log(date_from_ref)
};


watch([date_from_ref, date_to_ref], (newVal, prevVal) => {
  // console.log(newVal, prevVal);
  changeDate();
});


function changeDate(v=0) {
  if (v) {
    view_by.value = v;
  }

  if (view_by.value == '7days') {
    view_date_from.value = false;
    date_from.value = getDate(date_to_ref.value);
    date_to.value = getDate(date_to_ref.value);
  }
  else if (view_by.value == 'daily' || view_by.value =='monthly') {
    view_date_from.value = true;
    if (date_from_ref.value > date_to_ref.value){
      date_from_ref.value = addDays(date_to_ref.value, -7);
    }
    date_from.value = getDate(date_from_ref.value);
    date_to.value = getDate(date_to_ref.value);
  }

  console.log('view', view_by.value, ':', date_from.value, '~', date_to.value)
  load_time.value = Date.now();
}

changeDate();
</script>

<style scoped>
div {
  text-align: center;
}
div.date {
  display: inline-flex;
}
</style>