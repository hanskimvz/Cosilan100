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
        <div class="row">
          <div class="col-12">
            <div class="card">
              <div class="card-body">
                <table ref="dataTableRef" class="display cell-border compact stripe hover">
                  <thead>
                    <tr>
                      <th v-for="column in columns" :key="column.data">
                        {{ column.title }}
                      </th>
                    </tr>
                  </thead>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="row">
              <div class="col-12">
                <div class="modal-header">
                  <strong>{{ t('profile') }}</strong>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <div class="row">
                    <div class="col-3">
                      <label for="id" class="me-2"> {{ t('id') }}</label>
                      <input type="text" class="form-control form-control-sm" style="width: 160px" id="id" v-model="form_data.id" readonly>
                    </div>
                    <div class="col-3">
                      <label for="name" class="me-2"> {{ t('name') }}</label>
                      <input type="text" class="form-control form-control-sm" style="width: 160px" id="name" v-model="form_data.name" >
                    </div>
                    <div class="col-5">
                      <label for="email" class="me-2"> {{ t('email') }}</label>
                      <input type="text" class="form-control form-control-sm" style="width: 300px" id="email" v-model="form_data.email" >
                    </div>
                    <div class="col-1">
                      <label for="flag" class="me-2"> {{ t('use') }} </label>
                      <div class="form-check form-switch bigger-switch">
                        <input class="form-check-input" type="checkbox" role="switch" id="flag" v-model="form_data.flag" />
                      </div>
                    </div>                      
                  </div>
                  <div class="row mt-3">
                    <div class="col-3">
                      <label for="role" class="me-2"> {{ t('role') }}</label>
                      <select class="form-control form-control-sm" id="role" style="width: 160px" v-model="form_data.role">
                        <option value="user"> {{ t('user') }}</option>
                        <option value="operator"> {{ t('operator') }}</option>
                        <option value="power_user"> {{ t('power_user') }}</option>
                        <option value="admin"> {{ t('admin') }}</option>
                      </select>
                    </div>
                    <div class="col-3">
                      <label for="name_eng" class="me-2"> {{ t('name_eng') }}</label>
                      <input type="text" class="form-control form-control-sm" id="name_eng" style="width: 200px" v-model="form_data.name_eng">
                    </div>
                    <div class="col-3">
                      <label for="date_in" class="me-2"> {{ t('date_in') }}</label>
                      <input type="date" class="form-control form-control-sm" id="date_in" style="width: 200px" v-model="form_data.date_in">
                    </div>  
                    <div class="col-3">
                      <label for="date_out" class="me-2"> {{ t('date_out') }}</label>
                      <input type="date" class="form-control form-control-sm" id="date_out" style="width: 200px" v-model="form_data.date_out">
                    </div>                                              
                  </div>
                  <div class="row mt-3">
                    <div class="col-9">
                        <label for="address" class="me-2"> {{ t('address') }}</label>
                        <input type="text" class="form-control form-control-sm" id="address"  v-model="form_data.address">
                    </div>
                    <div class="col-3">
                        <label for="telephone" class="me-2"> {{ t('telephone') }}</label>
                        <input type="text" class="form-control form-control-sm" id="telephone"  v-model="form_data.telephone">
                    </div>                    
                  </div>
                </div>
                <div class="modal-footer d-flex justify-content-between"> 
                  <button type="button" class="btn btn-warning" @click="passwordModal()">{{ t('change_password') }}</button>
                  <div class="d-flex justify-content-end">
                    <button type="button" class="btn btn-primary me-2" @click="updateUser()">{{ t('save') }}</button>
                    <button type="button" class="btn btn-secondary" @click="closeModal()">{{ t('close') }}</button>
                  </div>
                </div>
              </div>                  
            </div>
          </div>
        </div>
      </div>

      <div class="modal fade" id="myModalPassword" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <strong>{{ t('change_password') }}</strong>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="row">
                <div class="col-12 d-flex justify-content-start mb-2">
                  <label for="current_pw" class="col-2 me-2"> {{ t('current_password') }}</label>
                  <input type="password" class="form-control form-control-sm" style="width: 260px" id="current_pw" v-model="form_password.current" >
                </div>
                <div class="col-12 d-flex justify-content-start mb-2">
                  <label for="new_pw" class="col-2 me-2"> {{ t('new_password') }}</label>
                  <input type="password" class="form-control form-control-sm" style="width: 260px" id="new_pw" v-model="form_password.new" >
                </div>
                <div class="col-12 d-flex justify-content-start mb-2">
                  <label for="confirm_pw" class="col-2 me-2"> {{ t('confirm_password') }}</label>
                  <input type="password" class="form-control form-control-sm" style="width: 260px" id="confirm_pw" v-model="form_password.confirm" >
                </div>                
              </div>
              <div class="row mt-4">
                <div class="col-12 d-flex justify-content-start">
                  <span class="text-danger">{{ t('password_desc') }}</span>
                </div>
              </div>
            </div>
            <div class="modal-footer d-flex justify-content-between"> 
              <button type="button" class="btn btn-primary px-3 me-2" @click="changePassword()">{{ t('change_password') }}</button>
              <button type="button" class="btn btn-secondary px-3" @click="closePasswordModal()">{{ t('close') }}</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>


<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import axios from 'axios'
import { Modal } from 'bootstrap';
// Bootstrap 전체 import로 변경
// import * as bootstrap from 'bootstrap'
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import { useCookies } from 'vue3-cookies';


const { t, locale } = useI18n();
const { cookies } = useCookies();

const route = useRoute();
const router = useRouter();

import navLanguage from '@/layout/NavLanguage.vue';
import navDropdown from '@/layout/NavDropdown.vue';

import DataTablesCore from 'datatables.net-bs5';
import 'datatables.net-buttons';
import 'datatables.net-buttons/js/buttons.html5.js';
import 'datatables.net-dt/js/dataTables.dataTables';
import 'datatables.net-select';
// import 'datatables.net-select-bs5';

import { getDataTableOptions } from '@/components/datatable_option';

const form_data = ref({});
const form_password = ref({});

const dataTableRef = ref(null);
let dataTableInstance = null;

const table_head = ['id', 'name', 'email', 'role_t', 'use'];
const columns = ref([]);

// Function to initialize DataTable
const initializeDataTable = (columns, data) => {
  if (dataTableRef.value) {
    const options = getDataTableOptions(t);
    options.select = true;
    dataTableInstance = new DataTablesCore(dataTableRef.value, {
      ...options,
      data,
      columns,
      select: {
        style: 'single',
        info: false
      },
      pagingType: 'simple_numbers',
      autoFill: true,
    });

    dataTableInstance.on('select', function (e, dt, type, indexes) {
      if (type === 'row') {
        const rowData = dataTableInstance.rows(indexes).data().toArray()[0];
        handleRowSelect(rowData);
      }
    });

    dataTableInstance.on('deselect', function (e, dt, type, indexes) {
      if (type === 'row') {
        handleRowDeselect();
      }
    });
  }
};

const handleRowSelect = (rowData) => {
  console.log('선택된 행:', rowData);
  form_data.value = rowData;
  showModal();
  // 여기에 선택된 행 데이터 처리 로직 추가
};

const handleRowDeselect = () => {
  console.log('선택 해제됨');
  // 여기에 선택 해제 처리 로직 추가
};

const showModal = () => {
  const myModal = new Modal(document.getElementById('myModal'));
  myModal.show();
};

const closeModal = () => {
  const myModal = Modal.getInstance(document.getElementById('myModal'));
  myModal.hide();
};

const passwordModal = () => {
  const myModal = Modal.getInstance(document.getElementById('myModal'));
  myModal.hide();  
  const myModalPassword = new Modal(document.getElementById('myModalPassword'));
  myModalPassword.show();
};

const closePasswordModal = () => {
  const myModal = Modal.getInstance(document.getElementById('myModal'));
  myModal.hide();
  const myModalPassword = Modal.getInstance(document.getElementById('myModalPassword'));
  myModalPassword.hide();
};

async function getUserList (){
  try{
    const res = await axios({
      method: 'post', 
      url: '/api/query',
      params: {
        data: 'getUserList',
      },
      data: {
        db_name: cookies.get('_db_name'),
        id: cookies.get('_login_id'),
        role: cookies.get('_role'),
        format: 'json',
      },
      header:{"Context-Type": "multipart/form-data"}
    });
    const data = await res.data;
    console.log(data);
    const columns = table_head.map((item) => ({
      data: item,
      title: t(item),
      className: 'text-center',
    }));

    const table_body = data.data.map((row) => {
      // row.uptime = formatElapsedTime(row.uptime);
      row.use = (row.flag === true || row.flag === 'y') ? '<i class="bi bi-check-circle-fill"></i>' : ''
      row.flag = (row.flag === true || row.flag === 'y') ? true : false;
      row.role_t = t(row.role);

      return row;
    });
    
    if (dataTableInstance) {
      dataTableInstance.destroy();
    }
    console.log(columns, table_body);
    initializeDataTable(columns, table_body);
  }
  catch(error){
    console.log(error);
  }

}

const updateUser = async () => {
  console.log(form_data.value);
  const filter = {_id: form_data.value._id};
  const update = form_data.value;
  delete update._id;
  delete update.role_t;
  delete update.use;
  try{
    const res = await axios({
      method: 'post', 
      url: '/api/update',
      params: {
        data: 'updateUser',
      },
      data: {
        filter: filter, 
        update: update,
        db_name: cookies.get('_db_name'),
        id: cookies.get('_login_id'),
        role: cookies.get('_role'),
        format: 'json',
      },
      header:{"Context-Type": "multipart/form-data"}
    });
    const data = await res.data;
    console.log(data);
    if (data.code == 1000){
      closeModal();
      // getUserList();
    }
  }
  catch(error){
    console.log(error);
  }
}

const changePassword = async () => {
  console.log(form_password.value);
  if (!form_password.value.current || !form_password.value.new || !form_password.value.confirm){
    alert(t('enter_password'));
    return;
  }
  if (form_password.value.new != form_password.value.confirm){
    alert(t('passwords_not_match'));
    return;
  }
  if (form_password.value.new.length < 8){
    alert(t('password_desc'));
    return;
  }
  const update = {
    _id: form_data.value._id,
    id: form_data.value.id,
    ...form_password.value
  }

  console.log(update);
  try{
    const res = await axios({
      method: 'post', 
      url: '/api/update',
      params: {
        data: 'changePassword',
      },
      data: {
        update: update,
        db_name: cookies.get('_db_name'),
        id: cookies.get('_login_id'),
        role: cookies.get('_role'),
        format: 'json',
      },
      header:{"Context-Type": "multipart/form-data"}
    });
    const data = await res.data;
    console.log(data);
    if (data.code == 1000){
      closePasswordModal();
    }
    else{
      alert(t(data.description));
    }
  }
  catch(error){
    console.log(error);
  }
}

onMounted(() => {
  getUserList();
});

onUnmounted(() => {
  if (dataTableInstance) {
    dataTableInstance.destroy();
  }
});

</script>


<style>
@import 'datatables.net-dt';
@import 'datatables.net-buttons-dt/css/buttons.dataTables.css';

.p-button-sm {
  font-size: 0.875rem;
  padding: 0.4rem 0.8rem;
}

.modal-dialog {
  max-width: 860px; 
  width: 860px;
  margin: 1.75rem auto;
}

.modal-content {
  min-height: 40vh; 
}

/* 반응형 크기 설정 */
/* @media (min-width: 992px) {
  .modal-dialog {
    max-width: 80%;
    width: 80%;
  }
} */

/* 모달이 잘 보이도록 z-index 설정 */
.modal {
  z-index: 1050;
}

.modal-backdrop {
  z-index: 1040;
}
</style>
