<template>
  <div class="row">
    
    <div class="col-6">
      <div class="card">
        <div class="card-header mb-0">
          <button class="btn btn-sm  btn-primary float-right" @click="updateMenus('main')">{{$t('apply')}}</button>
          <h5 class="card-title mb-0">Main</h5></div>
        <div class="card-body">
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <div class="form-inline">
                <span>use</span>
                <span class="col-md-3 mr-3">Page</span>
                <span class="col-md-2 mr-2">i18n_t</span>
                <span class="col-md-2 mr-2">icon</span>
                <span class="col-md-2">to</span>
              </div>
            </li>
            <li v-for="(m,i) in main_menus" :key="i"  class="list-group-item">
              <div class="form-inline">
                <input class="ml-2 mr-2" type="checkbox"  v-model="m.use">
                <span class="col-md-3 mr-3" v-if="m.page=='split_line'">{{ m.page }}</span>
                <span class="col-md-3 mr-3" v-else>{{ $t(m.i18n_t) }}</span>
                <input class="form-control form-control-sm col-md-2 mr-2"                             type="text" v-model="m.i18n_t" />
                <input v-if="m.page!='split_line' "class="form-control form-control-sm col-md-2 mr-2" type="text" v-model="m.icon" />
                <input v-if="m.page!='split_line' "class="form-control form-control-sm col-md-3"      type="text" v-model="m.to" />
              </div>
              <ul v-if="m.children"  class="list-group list-group-flush">
                <li v-for="(mx, j) in m.children" :key="j"  class="list-group-item">
                  <div class="form-inline">
                    <span>-</span><input class="ml-2 mr-2" type="checkbox" v-model="mx.use">
                    <span class="col-md-3">{{ $t(mx.i18n_t) }}</span>
                    <input class="form-control form-control-sm col-md-2 mr-3" type="text"  v-model="mx.i18n_t" />
                    <input class="form-control form-control-sm col-md-2 mr-3" type="text"  v-model="mx.icon" disabled/>
                    <input class="form-control form-control-sm col-md-3"      type="text"  v-model="mx.to" />
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="col-6">
      <div class="card">
        <div class="card-header" >
          <button class="btn btn-sm  btn-primary float-right" @click="updateMenus('admin')">{{$t('apply')}}</button>
          <h5 class="card-title mb-0">Admin</h5></div>
        <div class="card-body">
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <div class="form-inline">
                <span>use</span>
                <span class="col-md-3 mr-3">Page</span>
                <span class="col-md-2 mr-2">i18n_t</span>
                <span class="col-md-2 mr-2">icon</span>
                <span class="col-md-2">to</span>
              </div>
            </li>
            <li v-for="(m,i) in admin_menus" :key="i"  class="list-group-item">
              <div class="form-inline">
                <input class="ml-2 mr-2" type="checkbox" name="use" v-model="m.use" :disabled="m.page=='webpageconfig'">
                <span class="col-md-3 mr-3" v-if="m.page=='split_line'">{{ m.page }}</span>
                <span class="col-md-3 mr-3" v-else>{{ $t(m.i18n_t) }}</span>
                <input class="form-control form-control-sm col-md-2 mr-2" type="text" v-model="m.i18n_t" />
                <input v-if="m.page!='split_line' "class="form-control form-control-sm col-md-2 mr-2" type="text" v-model="m.icon" />
                <input v-if="m.page!='split_line' "class="form-control form-control-sm col-md-3" type="text" v-model="m.to" />
              </div>
              <ul v-if="m.children"  class="list-group list-group-flush">
                <li v-for="(mx,j) in m.children" :key="j"  class="list-group-item">
                  <div class="form-inline">
                    <span>-</span><input class="ml-2 mr-2" type="checkbox" name="use" v-model="mx.use" :disabled="m.page=='webpageconfig'">
                    <span class="col-md-3">{{ $t(mx.i18n_t) }}</span>
                    <input class="form-control form-control-sm col-md-2 mr-3" type="text" v-model="mx.i18n_t" />
                    <input class="form-control form-control-sm col-md-2 mr-3" type="text" v-model="mx.icon" disabled/>
                    <input class="form-control form-control-sm col-md-3"      type="text" v-model="mx.to" />                    
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </div>    

  </div>
	
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const main_menus = ref({});
const admin_menus = ref({});


function updateMenus(page) {
  const url ='/api/update?data=webconfig&fmt=json&page=' + page;
  let data = main_menus.value
  if (page=='admin') {
    data = admin_menus.value
  }
  axios.post(url, 
    { data: data }, 
    { header: {"Context-Type": "multipart/form-data",},}
  )
  .then((res) => {
    console.log(res);
  })
  .catch((error) => {
    console.error(error);
  });
}



function loadMenus() {
  const url ='/api/query?data=webconfig&fmt=json&page=main';
  console.log(url);
  axios.get(url)
  .then(result => {
    // console.log(result.data);
    main_menus.value = result.data.body;
  })
  .catch(error => {
      console.log(error);
  });
}

function loadAdminMenus() {
  const url ='/api/query?data=webconfig&fmt=json&page=admin';
  console.log(url);
  axios.get(url)
  .then(result => {
    console.log(result.data);
    admin_menus.value = result.data.body;
  })
  .catch(error => {
      console.log(error);
  });
}

onMounted( () => {
  loadMenus();
  loadAdminMenus();
});


</script>

<style></style>