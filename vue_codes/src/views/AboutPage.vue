<template>
  <h2>About page</h2>
  <p>{{ $route.path}}</p>
</template>

<script setup>
import { useRoute } from 'vue-router'
// import { ref, watch } from 'vue'
const route = useRoute();
console.log(route.path);
</script>

<style></style>