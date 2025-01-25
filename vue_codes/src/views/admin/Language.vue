<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="navbar-collapse ">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
      </ul>
      <navLanguage /><navDropdown />
    </div>
  </nav>  
  <div class="main">
    <main class="content">
      <div class="container-fluid mt-2">
      <div class="col-12 col-lg-12">
        <div class="card">
          <!-- <div v-if="is_loading" class="loading-overlay">
            <div v-if="is_loading" class="loading-spinner"></div>
          </div> -->
          <div class="card-body">
            <table class="table table-striped table-sm table-bordered table-hover" >
              <thead>
              <tr>
                <th v-for="head in table_head"  class="text-center" >{{ t(head.title) }}</th>
              </tr>
              </thead>
              <tbody>
                <tr id="0">
                  <td class="text-center">{{ t('add') }}</td>
                  <td class="text-center"><input type="text" v-model="new_lang.varstr" class="form-control form-control-sm" /></td>
                  <td class="text-center"><input type="text" v-model="new_lang.eng" class="form-control form-control-sm" /></td>
                  <td class="text-center"><input type="text" v-model="new_lang.kor" class="form-control form-control-sm" /></td>
                  <td class="text-center"><input type="text" v-model="new_lang.chi" class="form-control form-control-sm" /></td>
                  <td class="text-center"><input type="text" v-model="new_lang.page" class="form-control form-control-sm" /></td>
                  <td class="text-center"><input type="checkbox" v-model="new_lang.flag" value="y" class="form-check-input" /></td>
                  <td class="text-center">
                    <button class="btn btn-sm btn-primary me-2" @click="addLang">{{ t('add') }}</button>
                  </td>
                </tr>
                <tr v-for="(row, index) in table_body" :key="index" :id="index+1">
                  <td class="text-center">{{ index+1 }}</td>
                  <td><input type="text" v-model="row.varstr" class="form-control form-control-sm" /></td>
                  <td><input type="text" v-model="row.eng" class="form-control form-control-sm" /></td>
                  <td><input type="text" v-model="row.kor" class="form-control form-control-sm" /></td>
                  <td><input type="text" v-model="row.chi" class="form-control form-control-sm" /></td>
                  <td><input type="text" v-model="row.page" class="form-control form-control-sm" /></td>
                  <td><input type="checkbox" v-model="row.flag" value="y" class="form-check-input" /></td>
                  <td><div v-if="is_loading" class="loading-spinner"></div>
                    <button class="btn btn-sm btn-primary me-2" @click="modifyLang(row._id)">{{ t('modify') }}</button>
                    <button class="btn btn-sm btn-danger" @click="deleteLang(row._id)">{{ t('delete') }}</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useCookies } from 'vue3-cookies';
import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();
const { cookies } = useCookies();

import navLanguage from '@/layout/NavLanguage.vue';
import navDropdown from '@/layout/NavDropdown.vue';

const table_head = [
  {title:'id',      width:100, data: '_id'},
  {title:'varstr',  width:100, data: 'varstr'},
  {title:'english', width:100, data: 'eng'},
  {title:'korean',  width:100, data: 'kor'},
  {title:'chinese', width:100, data: 'chi'},
  {title:'page',    width:100, data: 'page'},
  {title:'use',     width:100, data: 'flag'},
  {title:'action',  width:100}
];

const table_body = ref([]);
const new_lang = ref({});

const is_loading = ref(false);

const getCellClass=(cellKey, cell, row)=>{
  return 'text-center';
}

const getCellContent=(cellKey, cell, row)=>{
  return cell;
}

const getLanguage = async()=>{
  is_loading.value = true;
  try {
    // await new Promise(resolve => setTimeout(resolve, 100));
    const res = await axios({
      method: 'post',
      url: '/api/query',
      params:{ data:'querydb' },
      data: {
        db_name: cookies.get('_db_name'),
        table: 'language',
        filter: {},
        sort: { varstr: 1 },
        format : 'json'
      },
      header:{"Context-Type": "multipart/form-data"}
    });

    const data = await res.data;
    console.log(data);
    if (data.code == 403) {
      router.push({ path: '/login', query:{'redirect': route.path}});
      is_loading.value = false;
      return 0;
    }

    table_body.value = data.data.map(row => ({
      ...row,
      // flag: row.flag === 'y' ? true : false
    }));
    console.log(table_body.value);
  } 
  catch(error) {
    console.error('Failed to fetch data', error)
  } 
  finally {
    is_loading.value = false;
  }
}

const checkLang = (lang) => {
  if (!lang.varstr) {
    alert('varstr is required');
    return 0;
  }
  if (!lang.eng) {
    alert('eng is required');
    return 0;
  }
  if (!lang.kor) {
    alert('kor is required');
    return 0;
  }
  if (!lang.chi) {
    alert('chi is required');
    return 0;
  }
  return 1;
}

const addLang = async () => {
  console.log(new_lang.value);
  if (!checkLang(new_lang.value)) {
    return 0;
  }

  const post_data = {
    db_name: cookies.get('_db_name'),
    table: 'language',
    login_id: cookies.get('_login_id'),
    role: cookies.get('_role'),
    format: 'json',
    update: new_lang.value
  }
  try {
    const res = await axios({
      method: 'post',
      url: '/api/insert',
      params: { data: 'insertdb' },
      data: post_data,
      header:{"Context-Type": "multipart/form-data"}
    });
    console.log(res);
  }
  catch(error) {
    console.error('Failed to fetch data', error)
  }
  finally {
  }
};

const modifyLang = async (_id) => {
  const row = table_body.value.find(row => row._id === _id);
  if (!checkLang(row)) {
    return 0;
  }
  
  const filter = { _id: row._id };
  const update = {
    varstr: row.varstr,
    eng: row.eng,
    kor: row.kor,
    chi: row.chi,
    page: row.page,
    flag: row.flag
  };

  const post_data = {
    filter: filter,
    update: update,
    db_name: cookies.get('_db_name'),
    table: 'language',
    login_id: cookies.get('_login_id'),
    role: cookies.get('_role'),
    format: 'json'
  } 
  try {
    const res = await axios({
      method: 'post',
      url: '/api/update',
      params: { data: 'updatedb',},
      data: post_data,
      header:{"Context-Type": "multipart/form-data"}
    });
    console.log(res);
  }
  catch(error) {
    console.error('Failed to fetch data', error)
  }
  finally {
  }
}

const deleteLang = async (_id) => {
  const row = table_body.value.find(row => row._id === _id);
  if (!row) {
    alert('row is not found');
    return 0;
  }
  if (row._id) {
    const x = confirm(` varstr: ${row.varstr} \n english: ${row.eng} \n korean: ${row.kor} \n chinese: ${row.chi} \n ` + t('delete_confirm'));
    if (!x) {
      return 0;
    }
  }
  const filter = { _id: row._id };
  const post_data = {
      filter: filter,
      db_name: cookies.get('_db_name'),
      table: 'language',
      login_id: cookies.get('_login_id'),
      role: cookies.get('_role'),
      format: 'json'
  }
  try {
    const res = await axios({
      method: 'post',
      url: '/api/delete',
      params: { data: 'deletedb' },
      data: post_data,
      header:{"Context-Type": "multipart/form-data"}
    });
  }
  catch(error) {
    console.error('Failed to fetch data', error)
  }
  finally {
  }
}

onMounted(()=>{
  getLanguage();
})
</script>

<style scoped>
.loading-spinner {
  border: 4px solid #333;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f8f9fa;
}
.btn-sm {
  font-size: 0.8rem;
  margin: 0.1rem;
}
.form-check-input {
  width: 1.2rem;
  height: 1.2rem;
}
</style>