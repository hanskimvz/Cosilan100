import '@/assets/app.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';
import { createI18n } from 'vue-i18n';
import { useCookies } from 'vue3-cookies';
import axios from 'axios';

import App from './App.vue';
import router from '@/components/routes.js';
// import routes from '@/components/routes.js';

const pinia = createPinia();
const app = createApp(App);

const { cookies } = useCookies();

let messages = {};
async function setI18n () {
  const url ='/api/query?data=language&fmt=json';
  // console.log(url);
  messages = (await axios.get(url)).data;

  const i18n = createI18n({
    legacy: false, // you must set `false`, to use Composition API
    locale: 'kor',
    fallbackLocale: 'eng',
    messages
  });
  return i18n;
}

app.use(pinia)
app.use(router)

setI18n().then((i18n)=>{
  app.use(i18n);
  app.mount('#app');
});












// createApp(App).use(router).mount('#app');
// app.use(pinia)
// app.use(router)
// app.use(i18n);
// app.mount('#app');

import '@/assets/app.js';
