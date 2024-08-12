<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="navbar-collapse ">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
      </ul>
      <navLanguage /><navDropdown />
    </div>
  </nav>
  
  <div class="main">
    <main class="content">
      <div class="container-fluid mt-2">
        <div class="row">
          <div class="col-12">
            <div class="clearfix">
              <div class="float-start">
                <div class="navbar-collapse col-lg-5 d-flex" >
                  <ul class="pagination pagination-sm">
                    <li class="page-item"  v-for="p in pages" :key="p" :class="p == page_no ? 'active' : ''">
                      <span class="page-link" @click="movePage(p)" style="cursor:pointer;">{{ p }}</span>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="float-end">TOTAL: {{ TOTAL_RECORD }}</div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-12">
            <table class="table table-striped table-sm table-bordered table-hover" >
              <thead>
                <tr>
                  <th v-for="(col,i) in table_head" :key="i">{{ col }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in table_body" :key="index">
                  <td v-for="(cell, cellKey) in row" :key="cellKey" 
                    :class="getCellClass(cellKey, cell, row)" 
                    v-html="getCellContent(cellKey, cell, row)">
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUpdated, computed } from 'vue';
import axios from 'axios';
import { _tz_offset } from '@/store/nav_store.js'
import { useRoute, useRouter } from 'vue-router'

import navLanguage from '@/layout/NavLanguage.vue';
import navDropdown from '@/layout/NavDropdown.vue';


const route = useRoute();
const router = useRouter();
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
const class_ref = ref([]);

const processedData = ref([]);

const massageTable = () => {
  table_body.value.forEach((row, idx) =>{
    console.log(row);
    // processedData[idx][]
  })
} 

// const massageTable = () => {
// processedData = computed(() => {
//   return table_body.value.map(row => {
//     if (db_name === 'common' && table_name === 'params') {
//       return row.map((cell, index) => {
//         if (index === 1) {
//           return `<a href="./devicedetail?${cell}">${cell}</a>`;
//         }
//         if (index >= 4 && index <= 10) {
//           return cell === 'n' ? '<font color=#AAAAAA>n</font>' : 'y';
//         }
//         return cell;
//       });
//     } else if (db_name === 'common' && table_name === 'face_thumbnail') {
//       return row.map((cell, index) => index === 4 ? `<img src="${cell}" height="100" />` : cell);
//     } else if (db_name.value === 'common' && table_name.value === 'snapshot') {
//       return row.map((cell, index) => index === 2 ? `<img src="${cell}" width="200" />` : cell);
//     } else if (db_name.value === 'common' && table_name.value === 'heatmap') {
//       return row.map((cell, index) => index === 4 ? 'draw_heatmap' : cell);
//     } else if (db_name.value === CUSTOM_DB && table_name.value === 'heatmap') {
//       return row.map((cell, index) => index === 4 ? 'draw heatmap' : cell);
//     }
//     return row;
//   });
// });
// }

function getCellClass(cellKey, cell, row) {
  if (db_name === 'common' && table_name === 'params') {
    if (['PRO', 'SURV', 'CNT', 'face', 'hm', 'crpt', 'mac'].includes(cellKey)) {
      return 'text-center';
    }
    if (cellKey === 'status') {
      if (cell) {
        if (cell.includes('days,')) {
          return 'badge text-bg-danger';
        }
        const [hours, minutes] = cell.split(':').map(Number);
        if (hours > 0 || minutes > 0) {
          return 'badge text-bg-warning';
        }
        return 'badge text-bg-success';
      }
    }
  }
  return '';
}

function getCellContent(cellKey, cell, row) {
  if (db_name === 'common' && table_name === 'params' ) {
    if(cellKey=='device_info') {
      return `<a href="./devicedetail?${cell}" target="_device_info">${cell}</a>`;
    }
    else if (['PRO', 'SURV', 'CNT', 'face', 'hm', 'crpt', 'mac'].includes(cellKey)) {
      return cell == 'n' ? '<font color=#AAAAAA>n</font>' : 'y';
    }
    else if (cellKey === 'status' && cell && cell.includes('days,')) {
      return cell.replace(' days,', 'D');
    }
  }
  else if (db_name === 'common' && table_name === 'snapshot') {
    if(cellKey == 'body') {
      return `<img src="${cell}" width="200" />`;
    }
  }
  else if (db_name === 'common' && table_name === 'face_thumbnail') {
    if(cellKey == 'thumbnail') {
      return `<img src="${cell}" height="100" />`;
    }
  }
  return cell;
}


const massageTableX= (()=>{
  console.log(db_name, table_name);
  const tags = $('tr:has(td)');
  for (let i=0; i<tags.length; i++){
    let tags_td = $(tags[i]).children('td');
    if (db_name == 'common' && table_name == 'params'){
      // console.log(tags_td[12])
      tags_td[1].innerHTML = '<a href="./devicedetail?'+tags_td[1].innerText+'">' + tags_td[1].innerText + '</a>';
      for (let k=4; k<11; k++) {
        tags_td[k].innerHTML = tags_td[k].innerHTML == 'n' ? '<font color=#AAAAAA>n</font>' : 'y';
        tags_td[k].className = "text-center";
      }
      
      if (tags_td[13].innerText.indexOf('days,')>0){
        tags_td[13].className = 'badge badge-danger';
        tags_td[13].innerHTML = tags_td[13].innerHTML.replace(' days,', 'D');
      }
      else {
        let time_delta = tags_td[13].innerHTML.split(":");
        if (time_delta >0) {
          tags_td[13].className = 'badge badge-warning';
        }
        else {
          tags_td[13].className = 'badge badge-success';
        }
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
  let dbs = route.params.table.split(".");
  db_name = dbs[0];
  table_name = dbs[1];
  if (db_name == 'custom') {
    db_name = CUSTOM_DB;
  }

  reload_flag = false;
  table_head.value = "";
  table_body.value = ""; 
  console.log(db_name, table_name) 
  if (db_name == 'common') {
    if (table_name == 'params') {
      fields = ['pk',	'device_info',	'usn', 'product_id as P_id', 'lic_pro as PRO',	'lic_surv as SURV',	'lic_count as CNT', 'face_det as face', 'heatmap as hm', 'countrpt as crpt', 'macsniff as mac', 'initial_access',	'last_access', 'timediff(now(), last_access) as status','db_name', 'url as local_ip', 'method'];
      orderby = "last_access desc";
    }
    else if (table_name == 'counting_report_10min') {
      fields = [];
      orderby = "regdate desc";
    }  
    else if (table_name == 'counting_event') {
      fields = ['pk',	'regdate', 'device_info',	'device_ip', 'timestamp', 'counter_name as ct_name',	'counter_val as ct_val',	'substring(message, 1, 80) as message', 'flag', 'status'];
      orderby = "regdate desc";
    }
    else if (table_name == 'face_thumbnail') {
      fields = ['pk','regdate', 'timestamp', 'datetime','thumbnail','age', 'gender', 'face_token', 'flag', 'flag_fd', 'flag_ud', 'flag_fs'	];
      orderby = "regdate desc";
    }
    else if (table_name == 'heatmap') {
      fields = [];
      orderby = "regdate desc";
    }  
    else if (table_name == 'snapshot') {
      fields = [];
      orderby = "regdate desc";
    }
    else if (table_name == 'access_log') {
      fields = [];
      orderby = "regdate desc";
    }
    else {
      fields = [];
      orderby = "datetime desc";
    }    
  }  
  else if (db_name == CUSTOM_DB) {
    if(table_name == 'count_tenmin_p') {
      fields = ['pk', 'device_info', 'timestamp', 'cast(concat(year,"-",month,"-",day," ",hour,":",min) as datetime) as datetime', 'counter_name as cnt_name', 'counter_val as cnt_val', 'counter_label as cnt_label', 'camera_code', 'store_code', 'square_code', 'flag'];
      orderby = "timestamp desc";
    } 
    else if (table_name == 'age_gender') {
      fields = ['pk', 'device_info', 'timestamp', 'cast(concat(year,"-",month,"-",day," ",hour,":",min) as datetime) as datetime', 'gender', 'age', 'camera_code', 'store_code', 'square_code'];
      orderby = "timestamp desc";
    }
    else if (table_name == 'heatmap') {
      fields = ['pk', 'device_info', 'timestamp', 'cast(concat(year,"-",month,"-",day," ",hour,":00") as datetime) as datetime', 'body_csv','camera_code', 'store_code', 'square_code'];
      orderby = "timestamp desc";
    }   
    else if (table_name == 'weather') {
      fields = [];
      orderby = "datetime desc";
    }
    else {
      fields = [];
      orderby = "datetime desc";
    }
  }  
  else {
    console.log("db wrong", db_name)
    return false;
  }
  
  const url ='/api/query?data=querydb&fmt=json&db='+db_name+'&table='+table_name;
  axios.post(url, 
    { 
      db: db_name,
      table: table_name,
      fields: fields,
      search: search,
      orderby: orderby,
      page_no: page_no,
      page_max: page_max,
      format : 'json'
    }, 
    { header: {"Context-Type": "multipart/form-data",},}
  )
  .then((res) => {
    console.log(res);
    if (res.data.code == 403) {
      router.push({ path: '/login'});
      return 0;
    }
    table_head.value = res.data.fields;
    table_body.value = res.data.data;
    TOTAL_RECORD.value = res.data.total_records;
    reload_flag = true;
    
    const total_page_num = Math.ceil(res.data.total_records/page_max);
    console.log('total page', total_page_num);
    let arr = [];
    for ( let p = 1; p <= total_page_num; p++) {
      if (p > total_page_num) {
        break;
      }
      if (p - page_no < -10) {
        continue;
      }
      if (p - page_no > 19) {
        break;
      }
      arr.push(p);
    }
    pages.value =  arr;
  })
  .catch((error) => {
    console.error(error);
  });
});

onUpdated(()=>{
  if (reload_flag == true) {
    // console.log(1);
    massageTable();
  }
  reload_flag = false;
})

onMounted(()=>{
  getDBData();
})

</script>

<style></style>