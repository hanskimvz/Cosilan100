<template>
<div class="justify-content-center" style="margin-left:10px; margin-right:10px;">
  <button value='tenmin'  :class="['btn', {'btn-warning': view_by == 'tenmin'}]"  @click="sendDataToParent">{{ $t('tenmin') }}</button>
  <button value='hourly'  :class="['btn', {'btn-warning': view_by == 'hourly'}]"  @click="sendDataToParent">{{ $t('hourly') }}</button>
  <button value='daily'   :class="['btn', {'btn-warning': view_by == 'daily'}]"   @click="sendDataToParent">{{ $t('daily') }}</button>
  <button value='monthly' :class="['btn', {'btn-warning': view_by == 'monthly'}]" @click="sendDataToParent">{{ $t('monthly') }}</button>
</div>

</template>


<script setup>

import { ref } from 'vue'

const emit = defineEmits(['dataEvent'])
const view_by = ref('hourly');

const sendDataToParent = () => {
  view_by.value = event.target.value;
  emit('dataEvent', {'view_by':event.target.value})
}
</script>

