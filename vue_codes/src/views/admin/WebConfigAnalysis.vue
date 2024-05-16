<template>
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-body">
          <table class="table table-striped table-sm table-bordered table-hover">
            <tbody>
              <tr>
                <th colspan="2">{{ $t('page') }}</th>
                <th>{{ $t('display') }}</th>
                <th>{{ $t('counter_label') }}</th>
              </tr>
              <tr v-for="(tb,i) in table_body" :key="i">
                <td>{{ $t(tb['page']) }}</td>
                <td>{{tb['page']}}</td>
                <td><input type="text" class="form-control" v-model="tb['display']"></td>
                <td>
                  <label v-for="(label, j) in tb['labels']" :key="j" class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" v-model="label['enable']" :checked="label['enable']">
                    <span  class="form-check-label">{{ $t(label['counter_label']) }}</span>
                  </label>
                </td>
              </tr>
              <tr>
                <td colspan="2">{{ $t('traffic_distribution_reset_hour') }}</td>
                <td colspan="2"><input type="text" class="form-control" v-model="traffic_reset_hour"></td>
              </tr>
              <tr>
                <td colspan="2">{{ $t('age_group') }}</td>
                <td colspan="2"><input type="text" class="form-control" v-model="age_group"></td>
              </tr>
            </tbody>
          </table>
          <button class="btn btn-primary" @click="changeOption()">{{ $t('save') }}</button>
          <span id="analysis_result"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { navStore } from '@/store/nav_store.js'
import { useI18n } from 'vue-i18n';

const { t, locale } = useI18n();
const dp = navStore(); // piana

const table_body = ref([]);
const traffic_reset_hour = ref();
const age_group = ref();


watch([locale], ()=>{
  table_body.value.forEach(item=>{
    item.display = t('_' + item.page + '_title');
  })
});

const changeOption=(()=>{
  // console.log(table_body.value);
  let arr_rs = [];
  table_body.value.forEach(item=>{
    let arr = {
      page: item.page,
      labels: item.labels.filter((ct)=>{
        return (ct['enable'] == true)
      }).map((ct)=>{
        return (ct['counter_label'])
      })
    }
    if (item.page == 'traffic_distribution'){
      arr['traffic_reset_hour'] = traffic_reset_hour.value;
    }
    arr_rs.push(arr);
  });
  arr_rs.push({
    page : 'age_group',
    labels: [age_group.value.split(",").map((item=>{
      return Number(item);
    }))]
  });
  console.log(arr_rs);
  axios({
    method: 'post',
    url : '/api/update',
    params: {
      db_name: dp.db_name,
      data: 'webconfig',
      page: 'analysis',
      fmt: 'json'
    },
    data: {data:arr_rs},
    header:{"Context-Type": "multipart/form-data"}

  }).then((res) => {
    console.log(res);
  }).catch((error) => {
    console.error(error);
  });




  
});


onMounted(() => {
  let url ='/api/query?data=querydb';
  let arr_label =[];

  axios.post(url, 
    { 
      db: dp.db_name,
      table: 'counter_label',
      fields: ['counter_label'],
      groupby: 'counter_label',
      format : 'json'
    }, 
    { header: {"Context-Type": "multipart/form-data",},}
  ).then(result => {
    // console.log(result.data);
    result.data.data.forEach((item) =>{
      arr_label.push(item['counter_label'])  ;
    })

  }).catch(error => {
    console.log(error);
  });

  url = '/api/query?data=webconfig&fmt=json&page=analysis';
  // console.log(url);
  axios.get(url)
    .then(result => {
      console.log(result.data.body);
      table_body.value = [];
      result.data.body.forEach((item) => {
        if (item.page == 'age_group') {
          age_group.value = item.labels.join(", ");
        }
        else {
          let arr = {
            page: item.page,
            display: t('_' + item.page + '_title'),
            labels:[]
          };
          arr_label.forEach((lb, j) => {
            arr['labels'].push({counter_label:lb, enable: item.labels.includes(lb)}) 
          });
          table_body.value.push(arr);
          if (item.page=='traffic_distribution') {
            traffic_reset_hour.value = item.traffic_reset_hour;
          }
        }
      });

        // table_body.value = result.data.body;
        // console.log(table_body.value);
      
    })
    .catch(error => {
      console.log(error);
    });

});

</script>

<style></style>