<template>
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">{{$t('basic_information') }}</h5>
        </div>
        <div class="card-body">
          <div class="form-group"><label>{{ $t('host_title') }}</label>
            <input class="form-control"  v-model="host_title">
          </div>
          <div class="form-group"><label>{{ $t('webpage_title') }}</label>
            <input class="form-control"  v-model="webpage_title"  >
          </div>
          <div class="form-group"><label>{{$t('logo')}}</label>
            <input type="file" id="upload_image" @change="getFileName($event.target.files)" accept=".gif, .jpg, .png" hidden /><br />
            <label for="upload_image">
              <img id="preview" :src="logo_src" />
            </label>
          </div>
          <div class="form-group"><label>{{ $t('developer') }}</label>
            <input class="form-control" type="text"  value="Hans Kim" readonly>
          </div>
          <button type="button" class="btn btn-primary"  @click="changeOption(this)">{{$t('save') }}</button>
          <span id="basic_result"></span>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useI18n } from 'vue-i18n';
import { navStore } from '@/store/nav_store.js'
const dp = navStore(); // piana

const { t, locale } = useI18n();
const webpage_title = ref(document.title);
const host_title = ref(document.getElementById('__host_title').innerHTML);
const logo_src = ref();

watch([locale], ()=>{
  webpage_title.value = document.title;
  host_title.value = document.getElementById('__host_title').innerHTML;
})



// let id = document.getElementById('logo_title');
// console.log(id.innerHTML)


function base64(file) {
  // 비동기적으로 동작하기 위하여 promise를 return 해준다.
  return new Promise(resolve => {
    // 업로드된 파일을 읽기 위한 FileReader() 객체 생성
    let a = new FileReader()
    // 읽기 동작이 성공적으로 완료됐을 때 발생
    a.onload = e => {
      resolve(e.target.result)
			// 썸네일을 보여주고자 하는 <img>에 id값을 가져와 src에 결과값을 넣어준다.
      const previewImage = document.getElementById('preview')
      previewImage.src = e.target.result
      console.log(previewImage.width, previewImage.height)
      // console.log(previewImage.src)
    }
		// file 데이터를 base64로 인코딩한 문자열. 이 문자열을 브라우저가 인식하여 원래 데이터로 만들어준다.
    a.readAsDataURL(file)
  })
}

async function getFileName(files) {
  console.log(files[0].name,  files[0].size)
  this.fileName = files[0]
  await this.base64(this.fileName)
}


const changeOption = (()=>{
  const previewImage = document.getElementById('preview')
  console.log(previewImage.src, previewImage.width, previewImage.height)
  console.log(logo_src.value)
  for (let i=0; i<2; i++) {
    let arr ={
      varstr: i==0 ? '_host_title' : '_webpage_title',
      flag:'y',
      db_name: dp.db_name,
      format: 'json'
    };
    arr[locale.value] = i==0 ? host_title.value : webpage_title.value;
    // console.log(arr);

    axios({
      method: 'post',
      url : '/api/update',
      params: {
        data: 'language'
      },
      data : arr,
      header:{"Context-Type": "multipart/form-data"}

    }).then((res) => {
      // console.log(res);
      document.getElementById('__host_title').innerHTML = host_title.value;
      document.title = webpage_title.value;
    }).catch((error) => {
      console.error(error);
    });
  }

  if (logo_src.value != previewImage.src) {
    console.log('need upate');
    if (previewImage.width > 300) {
      alert(t('too_large_image'));
      return false;
    }
    axios({
      method: 'post',
      url : '/api/update',
      params: {
        db_name: dp.db_name,
        data: 'webconfig',
        page: 'logo',
        fmt: 'json'
      },
      data: {data:previewImage.src},
      header:{"Context-Type": "multipart/form-data"}

    }).then((res) => {
      console.log(res);
      document.getElementById('__logo').src = previewImage.src;
    }).catch((error) => {
      console.error(error);
    });
  }
});



onMounted(()=>{
  const image = document.getElementById('__logo');
  image.onload = function () {
    logo_src.value = document.getElementById('__logo').src;
  }
  logo_src.value = document.getElementById('__logo').src;
})
</script>



<style></style>