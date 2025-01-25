<template>
  <!-- <ul class="navbar-nav mb-2 me-2 px-4 align-end">
    <li class="nav-item dropdown"  @click="toggleDropdown">
      <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
        {{ user_name }}
      </a>
      <ul v-if="isOpen" class="dropdown-menu">
        <li><RouterLink class="dropdown-item" to="/profile">{{$t('profile')}}</RouterLink></li>
        <li><RouterLink class="dropdown-item" to="/account/user">{{$t('user')}}</RouterLink></li>
        <li><RouterLink class="dropdown-item" to="/admin/language">{{$t('language')}}</RouterLink></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="/help/" target="_blank">{{$t('help')}}</a></li>
        <li><a class="dropdown-item" href="/logout">{{$t('logout')}}</a></li>
      </ul>
    </li>
  </ul> -->
  <ul class="navbar-nav mb-2 me-2 px-4 align-end">
    <li class="nav-item dropdown">
      <div class="dropdown" @mouseover="isOpen = true" @mouseleave="isOpen = false">
        <span class="dropdown-toggle">{{ user_name }}</span>
        <ul v-if="isOpen" class="dropdown-menu">
          <li><RouterLink class="dropdown-item" to="/profile" >{{$t('profile')}}</RouterLink></li>
          <li><RouterLink class="dropdown-item" to="/admin/">{{$t('admin_page')}}</RouterLink></li>
          <li><RouterLink class="dropdown-item" to="/admin/language">{{$t('language')}}</RouterLink></li>
          <li><hr class="dropdown-divider"></li>
          <li><a class="dropdown-item" href="/help/" target="_blank">{{$t('help')}}</a></li>
          <li><a class="dropdown-item" href="/logout">{{$t('logout')}}</a></li>
        </ul>
      </div>
    </li>
  </ul>  
</template>

<script setup>
import { ref } from 'vue';
import { useCookies } from 'vue3-cookies';
const { cookies } = useCookies();

const user_name = cookies.get('_name');

const isOpen = ref(false);

</script>

<style scoped>
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-toggle {
  padding: 0px 5px 10px 10px;
  /* background-color: #007bff; */
  /* color: white; */
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0px;
  /* left: -100px; */
  z-index: 1000;
  display: block;
  min-width: 10rem;
  padding: 0.5rem 30;
  margin: 0.125rem 0 0;
  font-size: 1rem;
  color: #212529;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 0.25rem;
}

.dropdown-item {
  padding: 0.25rem 1rem;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #d2e1f0;
}
</style>