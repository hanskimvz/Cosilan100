<template>
  <ul class="navbar-nav mb-2 me-2 px-4 align-end">
    <li class="nav-item dropdown">
      <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
        {{ cookies.get('_name') }}
      </a>
      <ul class="dropdown-menu dropdown-menu-end" >
        <li><RouterLink class="dropdown-item" to="/profile">{{$t('profile')}}</RouterLink></li>
        <li><a class="dropdown-item" href="/admin/" target="admin_page">{{$t('admin_page')}}</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="/help/">{{ $t('help') }}</a></li>
        <li><a class="dropdown-item" href="/logout">{{ $t('logout') }}</a></li>
      </ul>
    </li>
  </ul>
</template>

<script setup>
import { useCookies } from 'vue3-cookies';
const { cookies } = useCookies();


</script>