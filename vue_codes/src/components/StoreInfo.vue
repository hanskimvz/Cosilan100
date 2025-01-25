<template>
  <div class="card">
    <div class="card-header">
      <h3 class="mt-2" id="modal_device_info"><b>{{ $t('store_info') }}</b></h3>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-6">
          <label class="col-form-label">{{ $t('code') }}</label>
          <input type="text" v-model="store_info.code" class="form-control" readonly />
        </div>
        <div class="col-md-6">
          <label class="col-form-label">{{ $t('name') }}</label>
          <input type="text" v-model="store_info.name" class="form-control" />
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <label class="col-form-label">{{ $t('contact') }}</label>
          <input type="text" v-model="store_info.contact" class="form-control">
        </div>
        <div class="col-md-6">
          <label class="col-form-label">{{ $t('telephone') }}</label>
          <input type="text" v-model="store_info.contact_tel" class="form-control">
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
              <label class="col-form-label">{{ $t('address') }}</label>
              <input type="text" v-model="store_info.address" class="form-control">
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <label class="col-form-label d-flex align-items-center">{{ $t('open_hour') }} 
            <div class="form-check form-switch ms-2">
              <input class="form-check-input" type="checkbox" role="switch" :checked="display_open_hour" @change="display_open_hour= !display_open_hour">
            </div>
          </label>
          <div v-show="display_open_hour" class="form-group mb-0">
            <div class="col-md-5 d-flex">
              <select v-model="store_info.open_hour" class="form-control col-md-4">
                <option v-for="i in 12" :key="i-1" :value="i-1">{{ ('0' + (i-1) + ':00').slice(-5) }} {{ $t('am') }}</option>
                <option v-for="i in 12" :key="i+11" :value="i+11">{{ ('0' + (i-1 === 0 ? 12 : i-1) + ':00').slice(-5) }} {{ $t('pm') }}</option>
              </select>
              <span class="col-md-1 m-2 text-center">~</span>
              <select v-model="store_info.close_hour" class="form-control col-md-1">
                <option v-for="i in 12" :key="i-1" :value="i-1">{{ ('0' + (i-1) + ':00').slice(-5) }} {{ $t('am') }}</option>
                <option v-for="i in 12" :key="i+11" :value="i+11">{{ ('0' + (i-1 === 0 ? 12 : i-1) + ':00').slice(-5) }} {{ $t('pm') }}</option>
              </select>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <label class="col-form-label">{{ $t('square_group') }}</label>
          <select v-model="store_info.square_code" class="form-control" :disabled="cookies.get('_role') != 'admin'">
            <option v-for="square in store_info.squares" :key="square.code" :value="square.code">{{ square.code }}: {{ square.name }}</option>
          </select>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6">
          <label class="col-form-label">{{ $t('area') }}({{ $t('sqmt') }})</label>
          <input v-model="store_info.area" class="form-control" />
        </div>
        <div class="col-md-6">
          <label class="col-form-label">{{ $t('sniffing_mac') }}</label>
          <input type="text" v-model="store_info.sniffing_mac" class="form-control" />
        </div>
      </div>

      <div class="row">
        <div class="col-md-12">
          <label class="col-form-label">{{ $t('comment') }}</label>
          <input type="text" v-model="store_info.comment" class="form-control" />
        </div>
      </div>

    </div>
    <div v-if="!delete_pad" class="card-footer d-flex justify-content-between">
      <div class="float-left">
        <button class="btn btn-sm btn-warning"  @click="delete_pad=true">{{ $t('delete') }}</button>
      </div>
      <div class="text-right">
        <button class="btn btn-primary me-2" @click="update">{{ $t('save') }}</button>
        <button class="btn btn-secondary" @click="cancel">{{ $t('cancel') }}</button>
      </div>
    </div>      
    <div v-if="delete_pad" class="card-footer" >
      <div class="d-flex justify-content-between">
        <div class="d-flex">
          <label class="col-form-label me-2">{{ $t('admin_password') }}</label> 
          <input type="password" v-model="admin_password" class="form-control form-control-sm">
        </div>
        <div class="d-flex">
          <button class="btn btn-sm btn-warning px-3 me-2"  @click="delete_store">{{ $t('delete') }}</button>
          <button class="btn btn-secondary" @click="delete_pad=false">{{ $t('cancel') }}</button>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import axios from 'axios';
import { useI18n } from "vue-i18n";
import { useCookies } from "vue3-cookies";

const props = defineProps(["store_info"]);
const emit = defineEmits(["update"]);

const display_open_hour = ref(false);

const { t } = useI18n();
const { cookies } = useCookies();

const form_data = ref({});

const update = (() =>{
  console.log(props.store_info);
  if (props.store_info.code == '') {
    return;
  }
  if (props.store_info.name == '') {
    alert(t('new_store_alert'));
    return;
  }
 
  if (props.store_info.code == 'new') {
    props.store_info.code = 'ST'+ (new Date().getTime());
    console.log(props.store_info);
    form_data.value = {
      update: {
        store_code: props.store_info.code,
        store_name: props.store_info.name,
        store_contact: props.store_info.contact ? props.store_info.contact : '',
        store_tel: props.store_info.tel ? props.store_info.tel : '',
        store_open_hour: props.store_info.open_hour ? props.store_info.open_hour : 0,
        store_close_hour: props.store_info.close_hour ? props.store_info.close_hour : 0,
        store_area: props.store_info.area ? props.store_info.area : 0,
        store_sniffing_mac: props.store_info.sniffing_mac ? props.store_info.sniffing_mac : '',
        store_address: props.store_info.address ? props.store_info.address : '',
        store_comment: props.store_info.comment ? props.store_info.comment : '',
      },
      db_name: cookies.get('_db_name'),
      table: 'device_tree',
      id: cookies.get('_login_id'),
      role: cookies.get('_role'),
      format : 'json'
    }
    console.log(form_data.value);
    insert_store();
    // emit("update", form_data.value);
    return;
  }

  form_data.value = {
    filter: { store_code: props.store_info.code },
    update: {
      store_name: props.store_info.name,
      store_contact: props.store_info.contact ? props.store_info.contact : '',
      store_tel: props.store_info.tel ? props.store_info.tel : '',
      store_open_hour: props.store_info.open_hour ? props.store_info.open_hour : 0,
      store_close_hour: props.store_info.close_hour ? props.store_info.close_hour : 0,
      store_area: props.store_info.area ? props.store_info.area : 0,
      store_sniffing_mac: props.store_info.sniffing_mac ? props.store_info.sniffing_mac : '',
      store_address: props.store_info.address ? props.store_info.address : '',
      store_comment: props.store_info.comment ? props.store_info.comment : '',
    },
    db_name: cookies.get('_db_name'),
    table: 'device_tree',
    id: cookies.get('_login_id'),
    role: cookies.get('_role'),
    format : 'json'
  }
  if (props.store_info.square_code_org != props.store_info.square_code) {
    console.log('square_code_changed')
    form_data.value.update.square_code = props.store_info.square_code;
    form_data.value.update.square_name = props.store_info.squares.find(square => square.code == props.store_info.square_code).name;
  }
  console.log(form_data.value);
  update_store();
  // emit("update", form_data.value);
})

const delete_pad = ref(false);
const admin_password = ref('');

const delete_store = (() =>{
  console.log(admin_password.value);
})

const cancel = (() =>{
  console.log('cancel');
  emit("update", 'cancel');
})


const insert_store = async () =>{
  console.log(form_data.value);
  try {
    const res = await axios({
      method: 'post',
      url: '/api/insert',
      params:{ data:'insertdb' },
      data: { ...form_data.value },
      headers:{"Context-Type": "multipart/form-data"}
    });
    const data = await res.data;
    console.log(data);
  } catch (error) {
    console.log(error);
  }
}

const update_store = async () =>{
  try {
    const res = await axios({
      method: 'post',
      url: '/api/update',
      params:{ data:'updatedb' },
      data: { ...form_data.value },
      headers:{"Context-Type": "multipart/form-data"}
    });
    const data = await res.data;
    console.log(data);
  } catch (error) {
    console.log(error);
  }
  finally {
    emit("update", 'updated');
  }
}

</script>

<style scoped>
.card {
  margin-left: 0px;
  margin-right: 20px;
}
</style>
