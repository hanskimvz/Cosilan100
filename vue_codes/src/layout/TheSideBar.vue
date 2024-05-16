<template>
  <nav class="sidebar sidebar-sticky">
    <div class="sidebar-content ">
      <a class="sidebar-brand text-center mb-0 mr-4" href="/">
        <img id = "__logo" :src ="_logo_image" width="60px"/><br />
        <span id = "__host_title" class="align-middle ml-2" >{{ $t('_host_title')}}</span>
      </a> 
      <ul class="sidebar-nav">
        <li v-for=" (m, i) in menus":key="i" :class="m.page=='split_line' ? 'sidebar-header' : (m.to == $route.path ? 'sidebar-item active':'sidebar-item')" >
          <span v-if="m.page == 'split_line'">{{ $t(m.i18n_t) }}</span>
          <RouterLink v-if="(m.page != 'split_line' && !m.children &&m.use)" class="sidebar-link" :to="m.to">
              <i class="align-middle me-2 fas fa-fw" :class="m.icon"></i>{{ $t(m.i18n_t) }}
          </RouterLink>
          <a v-if="m.children" :href="m.to" data-toggle="collapse" class="sidebar-link collapsed">
            <i class="align-middle me-2 fas fa-fw" :class="m.icon"></i>{{ $t(m.i18n_t)}}
          </a>
          <ul v-if="m.children" :id="m.to.slice(1)" class="sidebar-dropdown list-unstyled collapse"  :class="m.ref_paths.includes($route.path) ?'show':''">
            <li v-for = "(mx, j) in m.children" :key = "j" class="sidebar-item" :class="mx.to == $route.path ? 'active': ''">
              <RouterLink v-if="mx.use" class="sidebar-link" :to="mx.to">{{ $t(mx.i18n_t)}}</RouterLink>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const menus = ref({});
// console.log(route.meta.page)

// console.log('logo_iamge', t('_logo_image'));

// const fname = ref("Vue");
// fname.value = t('_logo_image');

// function getImageUrl(name) {
//   return new URL(`/src/assets/${name}`, import.meta.url).href;
// }

const _logo_image = ref();
let ref_to = {};
onMounted( async ()=>{
  await router.isReady();
  console.log(route.meta.page)
  let url;
  // if (route.path.indexOf('/admin') >=0   || route.path.indexOf('/system') >=0) {
  if (route.meta.page == 'admin'){
    url ='/api/query?data=webconfig&fmt=json&page=admin';
  }
  // else {
  else if (route.meta.page == 'main') {
    url ='/api/query?data=webconfig&fmt=json&page=main';
  }

  // console.log(url);
  axios.get(url)
  .then(result => {
    // console.log(result);
    // if (!result.data) {
    //   result.data = default_body;
    // }
    menus.value = result.data.body;
    _logo_image.value = result.data.logo;

    menus.value.forEach((menu) => {
      menu['ref_paths'] = [];
      if (menu.children) {
        menu.children.forEach((ch) => {
          menu['ref_paths'].push(ch.to)
        });
      }

    });
    // console.log(main_menus.value);
  })
  .catch(error => {
      console.log(error);
      router.push("/login")
  });
  // const li_tags = $('li');
  // Object.entries(li_tags).forEach(element => {
  //   // console.log(element[1]);
  //   let tags_a = $(element[1]).children('a');
  //   console.log(tags_a[0]);
  // });
// console.log(li_tags)
});

const default_body = {
  "logo": "data:image/png;base64,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",
  "body": [
    { "page": "split_line",   "parent": 0,    "depth": 0,        "i18n_t": "main",        "icon": "",                "to": "",              "use": true    },
    { "page": "dashboard",    "parent": 0,    "depth": 0,        "i18n_t": "dashboard",   "icon": "fa-laptop",       "to": "/dashboard",    "use": true    },
    { "page": "footfall",     "parent": 0,    "depth": 0,        "i18n_t": "footfall",    "icon": "fa-user-friends", "to": "#footfall",     "use": true,
      "children": [
        { "page": "dataglunt",           "parent": 0, "depth": 0,  "i18n_t": "data_glunt",         "icon": "",      "to": "/dataglunt",         "use": true    },
        { "page": "latestflow",          "parent": 0, "depth": 0,  "i18n_t": "recent_data",        "icon": "",      "to": "/recentdata",        "use": true    },
        { "page": "trendanalysis",       "parent": 0, "depth": 0,  "i18n_t": "trend_analysis",     "icon": "",      "to": "/trendanalysis",     "use": true    },
        { "page": "advancedanalysis",    "parent": 0, "depth": 0,  "i18n_t": "advanced_analysis",  "icon": "",      "to": "/advancedanalysis",  "use": true    },
        { "page": "promotionanalysis",   "parent": 0, "depth": 0,  "i18n_t": "promotion_analysis", "icon": "",      "to": "/promotionanalysis", "use": false    },
        { "page": "brandoverview",       "parent": 0, "depth": 0,  "i18n_t": "brand_overview",     "icon": "",      "to": "/brandoverview",     "use": false    },
        { "page": "weatheranalysis",     "parent": 0, "depth": 0,  "i18n_t": "weather_analysis",   "icon": "",      "to": "/weatheranalysis",   "use": false    },
        { "page": "kpi",                 "parent": 0, "depth": 0,  "i18n_t": "kpi_overview",       "icon": "",      "to": "/kpi",               "use": false   }
      ]
    },
    { "page": "datacompare",      "parent": 0, "depth": 0, "i18n_t": "data_compare",        "icon": "fa-sliders-h",        "to": "#dataCompare",        "use": true,
      "children": [
        {  "page": "comparebytime",       "parent": 0,  "depth": 0,  "i18n_t": "compare_by_time",      "icon": "",    "to": "/comparebytime",        "use": true  },
        {  "page": "comparebyplace",      "parent": 0,  "depth": 0,  "i18n_t": "compare_by_place",      "icon": "",   "to": "/comparebyplace",       "use": true   },
        {  "page": "trafficdistribution", "parent": 0, "depth": 0,   "i18n_t": "traffic_distribution",  "icon": "",   "to": "/trafficdistribution",  "use": true   },
        {  "page": "comparebylabel",      "parent": 0,   "depth": 0, "i18n_t": "compare_by_label",      "icon": "",    "to": "/comparebylabel",      "use": true   }
      ]
    },
    { "page": "heatmap",     "parent": 0,  "depth": 0,      "i18n_t": "heatmap",      "icon": "map-pin",     "to": "/heatmap",        "use": false    },
    { "page": "agegender",   "parent": 0,  "depth": 0,      "i18n_t": "age_gender",   "icon": "slack",       "to": "/agegender",      "use": false    },
    { "page": "macsniff",    "parent": 0,  "depth": 0,      "i18n_t": "macsniff",     "icon": "wifi",        "to": "/macsniff",       "use": false    },
    { "page": "report",      "parent": 0,  "depth": 0,      "i18n_t": "report",       "icon": "fa-file",     "to": "#report",         "use": true,
      "children": [
        { "page": "summary",   "parent": 0,  "depth": 0,    "i18n_t": "summary",      "icon": "",            "to": "/reportsummary",  "use": true     },
        { "page": "standard",  "parent": 0,  "depth": 0,    "i18n_t": "standard",     "icon": "",            "to": "/reportstandard", "use": true     },
        { "page": "premium",   "parent": 0,  "depth": 0,    "i18n_t": "premium",      "icon": "",            "to": "/reportpremium",  "use": true     },
        { "page": "export",    "parent": 0,  "depth": 0,    "i18n_t": "export_db",    "icon": "",            "to": "/reportexport",   "use": true     }
      ]
    },
    { "page": "split_line",    "parent": 0,  "depth": 0,    "i18n_t": "setting",      "icon": "",                  "to": "",           "use": true     },
    { "page": "sensors",       "parent": 0,  "depth": 0,    "i18n_t": "sensors",      "icon": "fa-camera",         "to": "/sensors",   "use": true     },
    { "page": "sitemap",       "parent": 0,  "depth": 0,    "i18n_t": "sitemap",      "icon": "fa-grip-vertical",  "to": "/sitemap",   "use": true     },
    { "page": "split_line",    "parent": 0,  "depth": 0,    "i18n_t": "about",        "icon": "",                  "to": "",           "use": false    },
    { "page": "aboout",        "parent": 0,  "depth": 0,    "i18n_t": "about",        "icon": "fa-eye",            "to": "/about",     "use": false    },
    { "page": "feedback",      "parent": 0,  "depth": 0,    "i18n_t": "feedback",     "icon": "pen-tool",          "to": "/feedback",  "use": false    }
  ]
};
</script>