<script setup>
// import { defineComponent, onMounted, getCurrentInstance, computed } from "vue";
import sideBar from '@/layout/TheSideBar.vue'
import navBar from '@/layout/TheNavBar.vue'
import Footer from '@/layout/TheFooter.vue'

// import sideAdminBar from '@/layout/sideAdminBar.vue'
import navAdminBar from '@/layout/navAdminBar.vue'

</script>


<template>
  <header></header>
  <div  class="wrapper">
    <sideBar></sideBar>
    <div class="main">
      <navBar></navBar>
      <main class="content">
        <div class="container-fluid p-0">
          <RouterView></RouterView>
        </div>
        <Footer></Footer>
      </main>
    </div>
  </div> 
</template>
