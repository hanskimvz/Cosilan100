<template>
  <h2>system Tool</h2>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';



const getDBData=(()=>{

  const url ='/api/query?data=test&fmt=json';
  axios.get(url)
  .then((res) => {
    console.log(res);
  })
  .catch((error) => {
    console.error(error);
  });
});


onMounted(()=>{
  getDBData();
})

</script>