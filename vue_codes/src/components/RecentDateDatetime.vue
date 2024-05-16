<template>
  <div v-if="$route.path == '/recentdata'" class="form-inline d-none d-sm-inline-block">
    <button class="btn mr-sm-1" :class="view_by == 'tenmin' ? 'btn btn-secondary ': ''" @click="changeDate('tenmin')">10분단위</button>
    <button class="btn mr-sm-1" :class="view_by == 'hourly' ? 'btn btn-secondary ': ''"@click="changeDate('hourly')">시간별</button>
    <button class="btn mr-sm-1" :class="view_by == 'daily' ? 'btn btn-secondary ': ''"@click="changeDate('daily')">날짜별</button>
    <button class="btn mr-sm-1" :class="view_by == 'monthly' ? 'btn btn-secondary ': ''"@click="changeDate('monthly')">월별</button>
  </div>
  <div v-if="$route.path == '/recentdata'" class="form-inline">
    <div v-if="view_date_from" class="date">
      <span type="button" class="form-control btn btn-default" @click="modDate('from', -1)"><i class="fa fa-chevron-left"></i></span>
      <Datepicker 
        v-model="date_from_ref" 
        :locale="locale" 
        :weekStartsOn="0"
        :inputFormat="dateFormat"
        :size="10"
        :clearable="false"
        :allowOutsideInterval="false"
        :disabledDates = "{ predicate:isTodayOver}"
      />
      <span type="button" class="form-control"  @click="modDate('from', 1)"><i class="fa fa-chevron-right"></i></span>      
    </div>
    <span v-if="view_date_from" class="ml-2 mr-2">~</span>
    <div class="date">
      <span type="button" class="form-control"  @click="modDate('to', -1)"><i class="fa fa-chevron-left"></i></span>
      <Datepicker 
        v-model="date_to_ref" 
        :locale="locale" 
        :weekStartsOn="0"
        :inputFormat="dateFormat"
        :size="10"
        :clearable="false"
        :disabledDates = "{ predicate:isTodayOver}"
      />
      <span type="button" class="form-control"  @click="modDate('to', 1)"><i class="fa fa-chevron-right"></i></span>
    </div>
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

  if (view_by.value == 'tenmin' || view_by.value =='hourly') {
    view_date_from.value = false;
    date_from.value = getDate(date_to_ref.value);
    date_to.value = getDate(date_to_ref.value);
  }
  else {
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