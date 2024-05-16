<template>
  <div class="modal-dialog modal-md" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h3 id="modal_device_info"><b>{{ $t('square_info') }}</b></h3>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body m-0">
        <div class="col-md-12">
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('code') }}</label>
              <input type="text" v-model="square_info.code" class="form-control" >
            </div>
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('name') }}</label>
              <input type="text" v-model="square_info.name" class="form-control">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('address') }}</label>
              <input type="text" v-model="square_info.address" class="form-control">
            </div>
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('address_city') }}</label>
              <input type="text" v-model="square_info.addr_city" class="form-control">
            </div>
          </div>
          <div class="form-group">
            <label class="col-form-label">{{ $t('address_detail') }}</label>
            <input type="text" v-model="square_info.addr_b" class="form-control">
          </div>
          <div class="form-group">
            <label class="col-form-label">{{ $t('comment') }}</label>
            <textarea v-model="square_info.comment" class="form-control"></textarea>
          </div>
        </div>
        <div class="float-right">
          <button class="btn btn-sm btn-warning"  @click="document.getElementById('delete_pad').style.display='';">{{ $t('delete') }}</button>
        </div>
        <div class="text-center">
          <button class="btn btn-primary" @click="update">{{ $t('save') }}</button>
        </div>
      </div>
    </div>
  </div>


</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps(["square_info"]);
const emit = defineEmits(["update"])

const update = (() =>{
  emit("update")
})



</script>
