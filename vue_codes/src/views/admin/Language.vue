<template>
    <div class="main">
      <main class="content">
        <div class="container-fluid mt-2">
  <div class="col-12 col-lg-12">
    <div class="table-responsive">
			<table class="table table-striped table-sm table-bordered table-hover" >
				<thead>
					<tr>
						<th>PK</th>
						<th>{{$t('varstr')}}</th>
						<th>{{$t('english')}}</th>
            <th>{{$t('korean')}}</th>
            <th>{{$t('chinese')}}</th>
            <th>{{$t('page')}}</th>
            <th>{{$t('use')}}</th>
            <th>{{$t('regdate')}}</th>
            <th></th>
          </tr>
				</thead>
        <tbody>
          <tr>
            <td>{{$t('add')}}</td>
            <td><input type="text" class="form-control" name="var" ></td>
            <td><input name="eng"  class="form-control"></td>
            <td><input name="kor"  class="form-control"></td>
            <td><input name="chi"  class="form-control"></td>
            <td><input type="checkbox" class="form-control" name="use"></td>
            <th></th>
            <th></th>
            <td><button class="btn btn-success btn-sm" @click="addLang()">{{$t('add')}}</button></td>
          </tr>
          <tr v-for="(row,i) in table_body" :key="row.pk">
            <input type="hidden" name="act" value="modify" />
            <td>{{ row.pk }}</td>
            <td><input type="text" class="form-control" v-model="table_body[i].varstr"></td>
            <td><input type="text" class="form-control" v-model="table_body[i].eng"></td>
            <td><input type="text" class="form-control" v-model="table_body[i].kor"></td>
            <td><input type="text" class="form-control" v-model="table_body[i].chi"></td>
            <td><input type="text" class="form-control" v-model="table_body[i].page"></td>
            <td><input type="checkbox" class="form-check" v-model="table_body[i].use"></td>
            
            <td>{{ row.regdate}}</td>
            <td>
              <button class="btn btn-warning btn-sm" @click="modifyLang(i)">{{$t('modify')}}</button>
              <button class="btn btn-primary btn-sm ml-4" @click="deleteLang(row.pk)">{{$t('delete')}}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div></div></main></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { navStore } from '@/store/nav_store.js'

const dp = navStore(); // piana

const table_body = ref({})
function getLanguage() {
  const url ='/api/query?data=language&fmt=json&action=list';
  console.log(url);
  axios.get(url)
  .then(result => {
    // console.log(result.data);
    table_body.value = result.data;
    table_body.value.forEach((item,i) => {
      table_body.value[i].use = item.flag == 'y' ? true :false;
    })
  })
  .catch(error => {
      console.log(error);
  });
}

const addLnag=(()=>{

});

const modifyLang=((i)=>{
  console.log(table_body.value[i]);
  // const tags_td = $($('#id_'+pk)).children('td');
  // const tags_input = $(tags_td).children('input');
  let arr = table_body.value[i];
  arr.flag = arr.use ? 'y' :'n';
  arr.db_name = 'cnt_demo';
  arr.format = 'json';

  console.log(arr);
  axios({
    method: 'post',
    url : '/api/update',
    params: {
      data: 'language'
    },
    data : arr,
    header:{"Context-Type": "multipart/form-data"}

  }).then((res) => {
    console.log(res);
  }).catch((error) => {
    console.error(error);
  });
});
const deleteLang=((pk)=>{

});

onMounted(()=>{
  getLanguage();
})
</script>

<style></style>