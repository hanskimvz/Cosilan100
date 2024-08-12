<template>
  <div class="form-inline d-none d-sm-inline-block block">
    <!-- <div v-if="($route.path=='/dataglunt' || $route.path=='/trendanalysis' || $route.path=='/advancedanalysis' || $route.path=='/comparebylabel')"> -->
    <!-- <div v-if="(['/dataglunt', '/trendanalysis', '/advancedanalysis','/comparebylabel', '/comparebyplace'].includes($route.path))"> -->
    <div v-if="disp.view_by">
      <button class="btn mr-sm-1" :class="dr.view_by == 'tenmin'  ? 'btn btn-secondary ' : ''"  @click="changeViewBy('tenmin')">{{$t('tenmin')}}</button>
      <button class="btn mr-sm-1" :class="dr.view_by == 'hourly'  ? 'btn btn-secondary ' : ''"  @click="changeViewBy('hourly')">{{$t('hourly')}}</button>
      <button class="btn mr-sm-1" :class="dr.view_by == 'daily'   ? 'btn btn-secondary ' : ''"  @click="changeViewBy('daily')">{{$t('daily')}}</button>
      <button class="btn mr-sm-1" :class="dr.view_by == 'monthly' ? 'btn btn-secondary ' : ''"  @click="changeViewBy('monthly')">{{$t('monthly')}}</button>
    </div>
    <!-- <div v-else-if="$route.path == '/recentdata'"> -->
    <div v-else-if="disp.view_on">
      <button class="btn mr-sm-1" :class="dr.view_on == '7days'   ? 'btn btn-secondary ' : ''"  @click="dr.view_on='7days'">{{$t('T7days')}}</button>
      <button class="btn mr-sm-1" :class="dr.view_on == '4weeks'  ? 'btn btn-secondary ' : ''"  @click="dr.view_on='4weeks'">{{$t('T4weeks')}}</button>
      <button class="btn mr-sm-1" :class="dr.view_on == '12weeks' ? 'btn btn-secondary ' : ''"  @click="dr.view_on='12weeks'">{{$t('T12weeks')}}</button>
    </div>
  </div>
  <!-- <div class="form-inline"> -->
    <div v-if="disp.date_from" class="block">
    <!-- <div v-if="((['/dataglunt', '/advancedanalysis','/comparebylabel'].includes($route.path)) && (['daily', 'monthly'].includes(dr.view_by)))||$route.path=='/trafficdistribution'" class="block"> -->
      <span type="button" class="btn btn-default" @click="movDate('from', -1)"><i class="fa fa-chevron-left"></i></span>
      <Datepicker 
        v-model="dr.date_from" 
        :locale="locale_t" 
        :weekStartsOn="0" 
        :inputFormat="dateFormat" 
        :size="10"
        :clearable="false" 
        :allowOutsideInterval="false" 
        :disabledDates="{ predicate: isTodayOver }" 
        :class="'form-control text-center align-middle'"
        />
      <span type="button" class="btn btn-default" @click="movDate('from', 1)"><i class="fa fa-chevron-right"></i></span>
    </div>
    <span v-if="disp.date_from">~</span>
    <div v-if="disp.date_to" class="block">
      <span type="button" class="btn btn-default" @click="movDate('to', -1)" width="10"><i class="fa fa-chevron-left"></i></span>
      <Datepicker 
      v-model="dr.date_to" 
      :locale="locale_t" 
      :weekStartsOn="0" 
      :inputFormat="dateFormat" 
      :size="10"
      :clearable="false" 
      :disabledDates="{ predicate: isTodayOver }"
      :class="'form-control text-center align-middle'" 
      />
      <span type="button" class="btn btn-default" @click="movDate('to', 1)"><i class="fa fa-chevron-right"></i></span>
    </div>
  <!-- </div> -->

    <div v-if="disp.date_to1" class="block ml-2 mr-2">
      <span type="button" class="btn btn-default" @click="movDate('to1', -1)"><i class="fa fa-chevron-left"></i></span>
      <Datepicker 
      v-model="dr.date_to1" 
      :locale="locale_t" 
      :weekStartsOn="0" 
      :inputFormat="dateFormat" 
      :size="10"
      :clearable="false" 
      :disabledDates="{ predicate: isTodayOver }"
      :class="'form-control text-center align-middle'" 
      />
      <span type="button" class="btn btn-default" @click="movDate('to1', 1)"><i class="fa fa-chevron-right"></i></span>
    </div>
    <div v-if="disp.date_to2" class="block">
      <span type="button" class="btn btn-default" @click="movDate('to2', -1)"><i class="fa fa-chevron-left"></i></span>
      <Datepicker 
      v-model="dr.date_to2" 
      :locale="locale_t" 
      :weekStartsOn="0" 
      :inputFormat="dateFormat" 
      :size="10"
      :clearable="false" 
      :disabledDates="{ predicate: isTodayOver }"
      :class="'form-control text-center align-middle '" 
      />
      <span type="button" class="btn btn-default" @click="movDate('to2', 1)"><i class="fa fa-chevron-right"></i></span>
    </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue';
import { navStore } from '@/store/nav_store.js'
import { useRoute } from 'vue-router'
import Datepicker from 'vue3-datepicker';
import { ko, enUS, zhCN } from 'date-fns/locale'
import { useI18n } from 'vue-i18n';
const { locale } = useI18n();
const locale_t = ref(ko);
if (locale.value == 'kor') {
  locale_t.value = ko;
}
else if (locale.value == 'eng') {
  locale_t.value = enUS;
}
else if (locale.value == 'chi') {
  locale_t.value = zhCN;
}
const dateFormat = ref('yyyy-MM-dd');

let dr = navStore();

const isTodayOver = (date) => {
  return date > new Date();
};

const route = useRoute();
watch([route, locale], (o,n)=> {
  // console.log(route.path)
  validateDisplay(route.path);
  if (locale.value == 'kor') {
    locale_t.value = ko;
  }
  else if (locale.value == 'eng') {
    locale_t.value = enUS;
  }
  else if (locale.value == 'chi') {
    locale_t.value = zhCN;
  }  
});

const disp = ref({
  view_by: false,
  view_on: false,
  date_from: false,
  date_to: false,
  date_to1: false,
  date_to2: false
});

const validateDisplay = ((path)=>{
  if (['/dataglunt', '/trendanalysis', '/advancedanalysis','/comparebylabel', '/comparebyplace'].includes(path)) {
    disp.value.view_by = true;
    disp.value.view_on = false;
    disp.value.date_from = ['daily', 'monthly'].includes(dr.view_by) ? true : false;
    disp.value.date_to = true;
    disp.value.date_to1 = false;
    disp.value.date_to2 = false;
  }
  else if (path == '/recentdata') {
    disp.value.view_by = false;
    disp.value.view_on = true;
    disp.value.date_from = false;
    disp.value.date_to = true;
    disp.value.date_to1 = false;
    disp.value.date_to2 = false;
  }  
  else if (path == '/comparebytime') {
    disp.value.view_by = false;
    disp.value.view_on = false;
    disp.value.date_from = false;
    disp.value.date_to = true;
    disp.value.date_to1 = true;
    disp.value.date_to2 = true;
  }
  else if (path == '/trafficdistribution') {
    disp.value.view_by = false;
    disp.value.view_on = false;
    disp.value.date_from = true;
    disp.value.date_to = true;
    disp.value.date_to1 = false;
    disp.value.date_to2 = false;
  }        
  else {
    disp.value.view_by = false;
    disp.value.view_on = false;
    disp.value.date_from = false;
    disp.value.date_to = false;
    disp.value.date_to1 = false;
    disp.value.date_to2 = false;
  }
});
// validateDisplay(route.path);
//  || $route.path=='/trendanalysis' || $route.path=='/advancedanalysis' || $route.path=='/comparebylabel'))



function addDays(date, days) {
  const clone = new Date(date);
  clone.setDate(date.getDate() + days)
  return clone;
}

const movDate = (flag, val) => {
  if (flag == 'from') {
    dr.date_from = addDays(dr.date_from, val)
  }  
  else if (flag == 'to') {
    dr.date_to = addDays(dr.date_to, val)
  }
  else if (flag == 'to1') {
    dr.date_to1 = addDays(dr.date_to1, val)
  }
  else if (flag == 'to2') {
    dr.date_to2 = addDays(dr.date_to2, val)
  }  
};

const changeViewBy = ((v) => {
  dr.view_by = v;
  validateDisplay(route.path);
  if (dr.view_by == 'daily' && dr.date_from >= dr.date_to) {
    dr.date_from = addDays(dr.date_to, -7)
  }
  else if (dr.view_by == 'monthly' && dr.date_from >= dr.date_to){
    dr.date_from = addDays(dr.date_to, -7*30)
  }

});

onMounted(()=>{
  validateDisplay(route.path);
})

</script>

<style scoped>
div {
  text-align: center;
}

div.block {
  display: inline-flex;
}
</style>