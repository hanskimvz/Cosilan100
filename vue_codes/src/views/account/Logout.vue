<template>
  <main class="main h-100 w-100">
    <div class="container h-100">
      <div class="row h-100">
        <div class="col-sm-10 col-md-8 col-lg-6 mx-auto d-table h-100">
          <div class="d-table-cell align-middle">
            <div class="text-center">
              <h1>{{ $t('thanks_using') }}</h1>
              <p>{{ $t('let_me_know') }}</p>
              <p>{{ $t('helpful') }}</p>
              <br />
              <div class="horizontal-links">
                <a href="/login" class="m-2">{{ $t('relogin') }}</a> | 
                <a href="/about.php"  class="m-2">{{ $t('about_us') }}</a> | 
                <a href="/mailto.php"  class="m-2">{{ $t('contact_us')}}</a> | 
                <a href="/faq.php"  class="m-2">{{ $t('faq') }}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useCookies } from 'vue3-cookies';
const {cookies} = useCookies();

cookies.remove('_login_id');
cookies.remove('_db_name');
cookies.remove('_role');
cookies.remove('_selected_language');
cookies.remove('_name');
cookies.remove('_userseq');

</script>