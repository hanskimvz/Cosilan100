<template>
  <div class="row">
    <div class="col-12">
      <div class="float-right mr-3" >TOTAL: {{ TOTAL_RECORD }}</div>
      <div class="col-12 col-lg-5 d-flex" >
        <nav>
          <ul class="pagination pagination-sm">
            <li class="page-item"  v-for=" p in pages" :key="p" :class="p==page_no ? 'active' : ''"><span class="page-link" @click="movePage(p)" style="cursor:pointer;">{{ p }}</span></li>
          </ul>
        </nav>
      </div>
      <table class="table table-striped table-sm table-bordered table-hover" >
        <thead>
          <tr>
            <th v-for="(col,i) in table_head" :key="i">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in table_body" :key="i">
            <td v-for="(col, j) in table_body[i]" :key="j" >{{ col }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUpdated } from 'vue';
import axios from 'axios';
import { _tz_offset } from '@/store/nav_store.js'
import { useRoute } from 'vue-router'

const route = useRoute();
const CUSTOM_DB = 'cnt_demo'; // get From cookie
// console.log (route.path, route.params.table);


let db_name;
let table_name;
let fields = '';
let search = '';
let page_no = 1;
let page_max = 20;
let orderby = '';
let reload_flag = false;

let ts;
watch([route], (o,n)=> {
  // console.log (route.path, route.params.table)
  page_no = 1;
  if (ts) {
    clearTimeout(ts);
  }
  ts =  setTimeout(() => {
    getDBData()
  }, 500);  
});


const table_head = ref();
const table_body = ref();
const TOTAL_RECORD = ref(0);
const pages = ref();


const massageTable= (()=>{
  console.log(db_name, table_name);
  const tags = $('tr:has(td)');
  for (let i=0; i<tags.length; i++){
    let tags_td = $(tags[i]).children('td');
    if (db_name == 'common' && table_name == 'params'){
      // console.log(tags_td[12])
      tags_td[1].innerHTML = '<a href="./devicedetail?'+tags_td[1].innerText+'">' + tags_td[1].innerText + '</a>';
      for (let k=4; k<11; k++) {
        tags_td[k].innerHTML = tags_td[k].innerHTML == 'n' ? '<font color=#AAAAAA>n</font>' : 'y';
      }
      
      let diffMSec = (tags_td[13].innerText - _tz_offset) * 1000;
      // let dispTime = ('0' + new Date(diffMSec).getHours()).slice(-2) + ":" + ('0' + new Date(diffMSec).getMinutes()).slice(-2) + ":" + ('0' + new Date(diffMSec).getSeconds()).slice(-2);
      let dispTime = ('0' + Math.floor(tags_td[13].innerText/3600)).slice(-2) + ":" +  ('0' +Math.ceil(tags_td[13].innerText/60)).slice(-2) + ":" + ('0' + Math.ceil(tags_td[13].innerText%60)).slice(-2)

      if (tags_td[13].innerText < 3600) {
        tags_td[13].innerHTML = dispTime; 
        // tags_td[13].align = "center"; 
        tags_td[13].className = 'badge badge-success';
      }
      else if (tags_td[13].innerText < 3600 * 24) {
        tags_td[13].innerHTML = dispTime;  
        tags_td[13].className = 'badge badge-warning';
      }
      else {
        tags_td[13].innerHTML = Math.floor(diffMSec/3600000/24, 0) + "D "+ dispTime;  
        tags_td[13].className = 'badge badge-danger';
      }
    }
    else if (db_name == 'common' && table_name == 'face_thumbnail') {
      tags_td[4].innerHTML = '<img src="'+ tags_td[4].innerHTML +'" height="100" />';
    }
    else if (db_name == 'common' && table_name== 'snapshot') {
      tags_td[2].innerHTML = '<img src="'+ tags_td[2].innerHTML +'" width="200" />';
    }
    else if (db_name == 'common' && table_name== 'heatmap') {
      tags_td[4].innerHTML = 'draw_heatmap';
    }
    else if (db_name == CUSTOM_DB && table_name == 'heatmap'){
      tags_td[4].innerHTML = 'draw heatmap';
    }

  }
});

const movePage = ((p) =>{
  console.log(p);
  page_no = p;
  getDBData();
})

const getDBData=(()=>{
  reload_flag = false;
  table_head.value = "";
  table_body.value = ""; 

  let filename = './bin/log/bi.log';
  const url ='/api/query?data=jsonfromfile&fmt=json&filename='+filename+'&cat=systemlog';
  axios.get(url)
  .then((res) => {
    console.log(res);
    table_head.value = res.data.fields;
    table_body.value = res.data.data;
    TOTAL_RECORD.value = res.data.total_records;
    reload_flag = true;
    
    // const total_page_num = Math.ceil(res.data.total_records/page_max);
    // console.log('total page', total_page_num);
    // let arr = [];
    // for ( let p = 1; p <= total_page_num; p++) {
    //   if (p > total_page_num) {
    //     break;
    //   }
    //   if (p - page_no < -10) {
    //     continue;
    //   }
    //   if (p - page_no > 19) {
    //     break;
    //   }
    //   arr.push(p);
    // }
    // pages.value =  arr;
  })
  .catch((error) => {
    console.error(error);
  });
});

onUpdated(()=>{
  if (reload_flag == true) {
    // console.log(1);
    // massageTable();
  }
  reload_flag = false;
})

onMounted(()=>{
  getDBData();
})

</script>

<style></style>