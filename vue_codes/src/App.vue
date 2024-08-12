<script setup>
// import { defineComponent, onMounted, getCurrentInstance, computed } from "vue";
import sideBar from '@/layout/TheSideBar.vue'
import navBar from '@/layout/TheNavBar.vue'
import Footer from '@/layout/TheFooter.vue'

import { useCookies } from 'vue3-cookies';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

const { t,locale } = useI18n();
const {  cookies } = useCookies();
const router = useRouter();

// Login check
if (!cookies.get('_login_id') || !cookies.get('_userseq') ) {
  cookies.set("_temp", "123456")
  router.push({ path: '/login'});
}

if (cookies.get('_selected_language')) {
  locale.value = cookies.get('_selected_language')
}
document.title = t('_webpage_title');
</script>

<template>
<div class="wrapper">

    <!-- Sidebar -->
    <sideBar v-if="$route.meta.page == 'main' || $route.meta.page =='admin'"></sideBar>
    
    <!-- Page Content -->
    <div id="content">
      <!-- <navBar v-if="$route.meta.page == 'main' || $route.meta.page !='account'"></navBar> -->
      <!-- <div class="container p-0">
        <div class="container-fluid p-0"> -->
          <RouterView></RouterView>
        <!-- </div>
      </div> -->
      <Footer v-if="$route.meta.page == 'main' || $route.meta.page == 'admin'"></Footer>
    </div>
  </div>
  <!-- <div class="wrapper">
    <sideBar v-if="$route.meta.page == 'main' || $route.meta.page == 'admin'"></sideBar>
    <div class="main">
      <navBar v-show="$route.meta.page == 'main' || $route.meta.page == 'admin'"></navBar>
      <main class="content">
        <div class="container-fluid p-0">
          <RouterView></RouterView>
        </div>
        <Footer v-if="$route.meta.page == 'main' || $route.meta.page == 'admin'"></Footer>
      </main>{{ $route.meta.page }}
    </div>
  </div>  -->
</template>

<!-- v-show: render and hidden
    v-if: not render
-->
<!-- <template>
  <header></header>
  <div v-if="$route.path=='/login' || $route.path=='/logout' || $route.path=='/register' || $route.path=='/pagesResetPassword'" class="main align-middle">
    <div class="main">
      <main class="content">
        <div class="container-fluid mt-5">
          <RouterView></RouterView>
        </div>
      </main>
    </div>
  </div>-->

<!-- <template>
  <div class="wrapper">
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
</template>  -->

<style scoped>
.wrapper {
  display: flex;
  width: 100%;
  align-items: stretch;
}

#content {
  width: 100%;
  padding: 0px;
  min-height: 100vh;
  transition: all 0.3s;
}

</style>