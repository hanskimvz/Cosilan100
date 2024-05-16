<template>
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
          <tr v-for="row in table_body" :key="row.pk" :id="'id_'+row.pk">
            <input type="hidden" name="act" value="modify" />
            <input type="hidden" name="pk" value="632" />
            <td>{{ row.pk }}</td>
            <td><input type="text" class="form-control" name="varstr" :value="row.varstr"></td>
            <td><input type="text" class="form-control" name="eng" :value="row.eng"></td>
            <td><input type="text" class="form-control" name="kor" :value="row.kor"></td>
            <td><input type="text" class="form-control" name="chi" :value="row.chi"></td>
            <td><input type="checkbox" class=" form-control" name="flag" :checked="row.flag=='y'"></td>
            <td><input type="text" class="form-control" name="page" :value="row.page"></td>
            <td>{{ row.regdate}}</td>
            <td>
              <button class="btn btn-warning btn-sm" @click="modifyLang(row.pk)">{{$t('modify')}}</button>
              <button class="btn btn-primary btn-sm ml-4" @click="deleteLang(row.pk)">{{$t('delete')}}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
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
  })
  .catch(error => {
      console.log(error);
  });
}

const addLnag=(()=>{

});

const modifyLang=((pk)=>{
  const tags_td = $($('#id_'+pk)).children('td');
  const tags_input = $(tags_td).children('input');
  let arr = {
    pk: pk,
    varstr:'',
    eng:'',
    kor:'',
    chi:'',
    page:'',
    flag:'',
    db_name: dp.db_name,
    format: 'json'
  };
  for (let i=0; i<tags_input.length; i++) {
    if (tags_input[i].type=='text') {
      arr[tags_input[i].name] =  tags_input[i].value;
    }
    else if (tags_input[i].type == 'checkbox'){
      arr[tags_input[i].name] =  tags_input[i].checked ? 'y': 'n';
    }
  }
  // console.log(arr)
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