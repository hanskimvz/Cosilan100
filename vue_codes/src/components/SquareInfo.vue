<template>
  <div class="card" >

    <div class="card-header">
      <h3 class="mt-2"><b>{{ $t('square_info') }}</b></h3>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-6">
          <label class="col-form-label">{{ $t('code') }}</label>
          <input type="text" v-model="square_info.code" class="form-control" readonly>
        </div>
        <div class="col-md-6">
          <label class="col-form-label">{{ $t('name') }}</label>
          <input type="text" v-model="square_info.name" class="form-control">
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <label class="col-form-label">{{ $t('address') }}</label>
          <input type="text" v-model="square_info.address" class="form-control">
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <label class="col-form-label">{{ $t('comment') }}</label>
          <input type="text" v-model="square_info.comment" class="form-control">
        </div>
      </div>
    </div>
  
    <div  v-if="!delete_pad" class="card-footer d-flex justify-content-between">
      <div class="float-left">
        <button v-if="props.square_info.code != 'new'" class="btn btn-sm btn-warning"  @click="delete_pad=true">{{ $t('delete') }}</button>
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
          <button class="btn btn-sm btn-warning px-3 me-2"  @click="delete_square">{{ $t('delete') }}</button>
          <button class="btn btn-secondary" @click="delete_pad=false">{{ $t('cancel') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from "vue";
import axios from "axios";
import { useI18n } from "vue-i18n";
import { useCookies } from "vue3-cookies";
import TheNavBar from "@/layout/TheNavBar.vue";

const { t } = useI18n();
const { cookies } = useCookies();

const props = defineProps({
  square_info: Object,
});

const config = ref({});

const getConfig = async () => {
  try {
    const res = await axios({
      method: 'get',
      url: '/ext/COSILAN/cosilan100/bin/config/config.json'
    });
    config.value = res.data;
    console.log(config.value);
  } catch (error) {
    console.log('config 파일을 읽는 중 오류가 발생했습니다:', error);
  }
}

getConfig();



const emit = defineEmits(['update']);

const delete_pad = ref(false);
const admin_password = ref('');
const form_data = ref({});



const update = (() =>{
  if (props.square_info.code == '') {
    return;
  }
  if (props.square_info.name == '') {
    alert(t('new_square_alert'));
    return;
  }
 
  if (props.square_info.code == 'new') {
    props.square_info.code = 'SQ'+ (new Date().getTime());
    console.log(props.square_info);
    form_data.value = {
      update: {
        square_code: props.square_info.code,
        square_name: props.square_info.name,
        square_address: props.square_info.address ? props.square_info.address : '',
        square_comment: props.square_info.comment ? props.square_info.comment : '',
      },
      db_name: cookies.get('_db_name'),
      table: 'device_tree',
      id: cookies.get('_login_id'),
      role: cookies.get('_role'),
      format : 'json'
    }
    console.log(form_data.value);
    insert_square();
    // emit("update", form_data.value);
    return;
  }

  form_data.value = {
    filter: { square_code: props.square_info.code },
    update: {
      square_name: props.square_info.name,
      square_address: props.square_info.address ? props.square_info.address : '',
      square_comment: props.square_info.comment ? props.square_info.comment : '',
    },
    db_name: cookies.get('_db_name'),
    table: 'device_tree',
    id: cookies.get('_login_id'),
    role: cookies.get('_role'),
    format : 'json'
  }
  console.log(form_data.value);
  update_square();
  // emit("update", form_data.value);
})

const delete_square = (() =>{
  console.log(admin_password.value);
})

const cancel = (() =>{
  emit("update", 'cancel');
})

const insert_square = async () =>{
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

const update_square = async () =>{
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
}

</script>

<style scoped>
.card {
  margin-left: 0px;
  margin-right: 20px;
}
</style>
