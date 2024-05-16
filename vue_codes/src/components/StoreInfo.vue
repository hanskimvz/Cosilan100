<template>
  <div class="modal-dialog modal-md" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h3 id="modal_device_info"><b>{{ $t('store_info') }}</b></h3>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body m-0">
        <div class="col-md-12">
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('code') }}</label>
              <input type="text" v-model="store_info.code" class="form-control"  />
            </div>
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('name') }}</label>
              <input type="text" v-model="store_info.name" class="form-control">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('phone') }}</label>
              <input type="text" v-model="store_info.phone" class="form-control">
            </div>
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('fax') }}</label>
              <input type="text" v-model="store_info.fax" class="form-control">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('contact') }}</label>
              <input type="text" v-model="store_info.contact" class="form-control">
            </div>
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('telephone') }}</label>
              <input type="text" v-model="store_info.contact_tel" class="form-control">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('address') }}</label>
              <input type="text" v-model="store_info.address" class="form-control">
            </div>
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('address_city') }}</label>
              <input type="text"  v-model="store_info.addr_city" class="form-control">
            </div>
          </div>
          <div class="form-group">
            <label class="col-form-label">{{ $t('address_detail') }}</label>
            <input type="text" v-model="store_info.addr_b" class="form-control">
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label>{{ $t('open_hour') }} 
                <input class="form-check-input ml-4" type="checkbox" :checked="display_open_hour" @change="display_open_hour= !display_open_hour">
              </label>
              <div v-show="display_open_hour" class="form-group mb-0 form-inline">
                <select v-model="store_info.open_hour" class="form-control col-md-5">
                  <option value="0">12:00  {{ $t('am') }}</option>
                  <option v-for="i in 11" :key="i" :value="i">{{ ('0' + i + ':00').slice(-5) }} {{ $t('am') }}</option>
                  <option value="12">12:00  {{ $t('pm') }}</option>
                  <option v-for="i in 11" :key="i" :value="i+12">{{ ('0' + i + ':00').slice(-5) }} {{ $t('pm') }}</option>
                </select>
                <span class="col-md-1 text-center">~</span>
                <select v-model="store_info.close_hour" class="form-control col-md-5">
                  <option value="0" selected>12:00  {{ $t('am') }}</option>
                  <option v-for="i in 11" :key="i" :value="i">{{ ('0' + i + ':00').slice(-5) }} {{ $t('am') }}</option>
                  <option value="12">12:00  {{ $t('pm') }}</option>
                  <option v-for="i in 11" :key="i" :value="i+12">{{ ('0' + i + ':00').slice(-5) }} {{ $t('pm') }}</option>
                </select>
              </div>
            </div>
            <div class="form-group col-md-6">
              <label>{{ $t('square_group') }}</label>
              <select v-model="store_info.square_code" class="form-control">
                <option value="SQ1547972440547" selected>SQ1547972440547: Home</option>
                <option value="SQ1547972950349">SQ1547972950349: 深圳南山</option>
                <option value="SQ1548262680701">SQ1548262680701: 罗湖办公室</option>
                <option value="SQ1578462515001">SQ1578462515001: 上海test</option>
                <option value="SQ1585273475721">SQ1585273475721: 泰富test</option>
                <option value="SQ1586836391699">SQ1586836391699: 某某商业中心</option>
                <option value="SQ1607389666989">SQ1607389666989: 山西景区</option>
                <option value="SQ1651608403108">SQ1651608403108: Temp</option>
                <option value="SQ1671956532775">SQ1671956532775: 韩国金浦</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('area') }}({{ $t('sqmt') }})</label>
              <input v-model="store_info.area" class="form-control" />
            </div>
            <div class="form-group col-md-6">
              <label class="col-form-label">{{ $t('sniffing_mac') }}</label>
              <input type="text" v-model="store_info.sniffing_mac" class="form-control" />
            </div>
          </div>
          <div class="form-group">
            <label class="col-form-label">{{ $t('comment') }}</label>
            <textarea v-model="store_info.comment" class="form-control"></textarea>
          </div>
        </div>
        <div class="float-right">
            <button class="btn btn-sm btn-warning" @click="document.getElementById('delete_pad').style.display='';">{{ $t('delete') }}</button>
        </div>
        <div class="text-center">
            <button class="btn btn-primary" @click="update">{{ $t('save') }}</button>
        </div>
      </div>
    </div>
  </div>






</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";

const props = defineProps(["store_info"]);
const emit = defineEmits(["update"]);

const display_open_hour = ref(false);
const update = (() =>{
  emit("update")
})



</script>