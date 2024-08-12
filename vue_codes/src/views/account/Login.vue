<template>
<div class="container p-0">
  <div class="container-fluid p-0">
    <div class="container position-absolute top-50 translate-middle-y">
      <div class="row justify-content-center  mt-5">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header" style="background: #304156;">
              <img src="/logo.png" height="40" class="rounded mx-auto d-block" />
            </div>
            <div class="card-body">
              <div class="mb-3" >
                <label for="ID" class="form-label">{{ $t('id_or_email') }}</label>
                <input type="text" class="form-control" v-model="post_data.id" required @click="clearmsg()">
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">{{ $t('password') }}</label>
                <input type="password" class="form-control"  v-model="post_data.password" required @click="clearmsg()">
              </div>
              <div class="mb-3">
                <label for="language" class="form-label">{{ $t('language') }}</label>
                <select class="form-select"  v-model="post_data.language" @change="changeLocale()">
                  <option value="eng">{{ $t('english') }}</option>
                  <option value="chi">{{ $t('chinese') }}</option>
									<option value="kor">{{ $t('korean') }}</option>
                </select>
              </div>
              <input v-model="rememberMe" type="checkbox" /><span class="px-2">{{ $t('remember_me')}}</span>
							<small class="px-2"><a href="/pagesResetPassword">{{ $t('forgot_password') }} </a></small>
              <div class="mb-3">
								<span id='rs' class="text-warning"></span>
              </div>
            </div>
            <div class="card-footer text-center">
              <button type="button" class="btn btn-primary w-50" @click="Login()">{{ $t('login_act') }}</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useCookies } from 'vue3-cookies';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();
const route = useRoute();
const router = useRouter();
const post_data = ref({id:'', password:'', language:''});
const rememberMe = ref(false);

const { cookies } = useCookies();

const changeLocale= (() =>{
  locale.value = post_data.value.language;
});


const Login=(()=>{
  if (!post_data.value.id) {
    message(t('enter_id_pw'));
    return false;
  }
  if (!(post_data.value.id.trim()) ) {
    message(t('enter_id_pw'));
    return false;
  }

  cookies.set("_selected_language", post_data.value.language);
  axios({
		method: "post",
		url:'/api/login',
		data: {
			format: 'json',
			id: post_data.value.id, 
			password: post_data.value.password
		},
		header: {
			"Context-Type": "multipart/form-data"
		}
	}).then(result => {
		console.log(result.data)
    if (result.data.code == 1000) {
      cookies.set('_login_id', result.data.description.ID);
      cookies.set('_db_name', result.data.description.db_name);
      cookies.set('_role', result.data.description.role);
      cookies.set('_name', result.data.description.name);
			cookies.set('_userseq', result.data.description.userseq);

			if(rememberMe.value){
				localStorage.setItem('id', post_data.value.id);
				localStorage.setItem('pw', post_data.value.password);
				localStorage.setItem('lang', post_data.value.language);
				localStorage.setItem('remember', rememberMe.value);
			}
			else {
				localStorage.removeItem('id');
				localStorage.removeItem('pw');
				localStorage.removeItem('lang');
				localStorage.removeItem('remember');
			}

			if(route.query.redirect){
				router.push({path: route.query.redirect}); // router.push has some problem.
			}
			else {
				router.push({path: '/'});
			}
    }
    else {
      message(t(result.data.message));
    }		
	}).catch(error =>{
		console.log(error)
	})
});
	

const message = (msg) => {
  document.getElementById('rs').innerHTML = msg;
  setTimeout(() => {
    document.getElementById('rs').innerHTML ="";
  }, 3000);
}


const clearmsg = ()=> {
    document.getElementById('rs').innerHTML = "";
};

// console.log('navigatr.language', navigator.language);

onMounted(() => {
  post_data.value.id = localStorage.getItem('id');
  post_data.value.password = localStorage.getItem('pw');
  post_data.value.language = localStorage.getItem('lang');
	console.log(post_data.value);
  if (!post_data.value.language) {
    if (navigator.language == 'ko') {
      locale.value = 'kor';
      post_data.value.language = 'kor';
    }

    else {
      locale.value = 'eng';
      post_data.value.language = 'eng';
    }
  }
  rememberMe.value = localStorage.getItem('remember');
});
	
// 	axios.post(url, {id:post_data.value.id, password: post_data.value.password})
//   .then(result => {
//     console.log(result.data);
//     if (result.data.code == 1000) {
//       cookies.set('_login_id', result.data.description.ID);
//       cookies.set('_db_name', result.data.description.db_name);
//       cookies.set('_role', result.data.description.role);
//       cookies.set('_name', result.data.description.name);
// 			cookies.set('_userseq', result.data.description.userseq);
//       message.value = 'login_ok';
//       $('#rs').attr('class', 'text-success');
//       window.location.href=("/");
//     }
//     else {
//       message.value = result.data.description;
//     }
//   })
//   .catch(error => {
//       console.log(error);
//   });
// });
</script>