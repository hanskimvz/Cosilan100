<template>
 
	<div class="container h-100">
		<div class="row h-100">
			<div class="col-sm-10 col-md-8 col-lg-6 mx-auto d-table h-100">
				<div class="d-table-cell align-middle">
					<div class="text-center mt-4">
						<h1 class="h2">{{ $t('welcome') }}</h1>
						<p class="lead">{{ $t('welcome_message') }}</p>
					</div>
					<div class="card">
						<div class="card-body">
							<form>
								<div class="m-sm-4">
									<div class="text-center">
										<span><i class="align-middle me-2 fas fa-fw fa-hashtag" style="width:60px; height:60px; color:#f000f0"></i></span>
									</div>
									<div class="form-group">
										<label>{{ $t('id_or_email') }}</label>
										<input class="form-control form-control-lg" type="text" placeholder="Enter Email or ID" v-model="post_data.id"/>
									</div>
									<div class="form-group">
										<label>{{ $t('password') }}</label>
										<input class="form-control form-control-lg" type="password" placeholder="Enter your password" v-model="post_data.password"/>
                    <small><a href="/pagesResetPassword">{{ $t('forgot_password') }} </a></small>
									</div>
									<div class="form-row">
										<div class="form-group col-md-6">
											<label>{{ $t('language') }}</label>
											<select class="form-control pull-right" v-model="post_data.language" @change="changeLocale()">
												<option value="eng">{{ $t('english') }}</option>
												<option value="kor">{{ $t('korean') }}</option>
                        <option value="chi">{{ $t('chinese') }}</option>
											</select>
										</div>
									</div>
									<div class="text-center mt-3">
										<button type="button" class="btn btn-lg btn-primary" @click="Login()">{{ $t('login_act') }}</button>
									</div>
									<div  class="mt-4"><span id="rs" class="text-danger">{{ $t(message) }}</span></div>
								</div>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import axios from 'axios';
import { useCookies } from 'vue3-cookies';
import { useI18n } from 'vue-i18n';
const { locale } = useI18n();

const post_data = ref({});
post_data.value.language = 'kor';
const message = ref(" ");

const { cookies } = useCookies();

const changeLocale= (() =>{
  // console.log(post_data.value.language);
  locale.value = post_data.value.language;
});

if (navigator.language == 'en-US') {
    locale.value = 'eng';
		post_data.value.language = 'eng';
}

const Login=(()=>{
  cookies.set("_selected_language", post_data.value.language);
  axios({
		method: "post",
		url:'/api/login',
		data: {
			format: 'json',
			id:post_data.value.id, 
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
      message.value = 'login_ok';
      $('#rs').attr('class', 'text-success');
			// cookies.remove('_login_id');
      window.location.href=("/");
    }
    else {
      message.value = result.data.description;
    }		
	}).catch(error =>{
		console.log(error)
	})
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