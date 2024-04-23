<script setup>
import sideBar from '@/layout/TheSideBar.vue'
import navBar from '@/layout/TheNavBar.vue'
import viewBody from '@/layout/TheView.vue'
import Footer from '@/layout/TheFooter.vue'
</script>

<template>
  <header>
  </header>
  <div class="wrapper">
    <sideBar></sideBar>
    <div class="main">
      <navBar></navBar>
      <main>
        <viewBody></viewBody>
        <Footer></Footer>
      </main>
    </div>
  </div>
</template>

<style></style>
