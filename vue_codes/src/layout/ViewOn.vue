<template>
<div class="justify-content-center" style="margin-left:10px; margin-right:10px;">
  <button value="7days"   :class="['btn', {'btn-warning': view_on == '7days'}]"   @click="sendDataToParent">{{$t('T7days')}}</button>
  <button value="4weeks"  :class="['btn', {'btn-warning': view_on == '4weeks'}]"  @click="sendDataToParent">{{$t('T4weeks')}}</button>
  <button value="12weeks" :class="['btn', {'btn-warning': view_on == '12weeks'}]" @click="sendDataToParent">{{$t('T12weeks')}}</button>
</div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['dataEvent'])
const view_on = ref('7days');

const sendDataToParent = () => {
  view_on.value = event.target.value;
  emit('dataEvent', {'view_on':event.target.value})
}
</script>

