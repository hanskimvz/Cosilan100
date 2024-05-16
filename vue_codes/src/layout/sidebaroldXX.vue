<template>
  <nav class="sidebar sidebar-sticky">
    <div class="sidebar-content ">
      <a class="sidebar-brand text-center mb-0 mr-4" href="/">
        <img :src ="_logo_image" width="60px"/><br />
        <span class="align-middle ml-2" >{{ $t('_webpage_title')}}</span>
      </a> 
      <ul class="sidebar-nav">
        <li class="sidebar-header">Main</li>
        <li class="sidebar-item" :class="['/', '/dashboard'].includes($route.path) ? 'active': ''">
          <RouterLink class="sidebar-link"  to="/"><i class="align-middle me-2 fas fa-fw fa-laptop"></i>{{$t('dashboard')}}</RouterLink>
        </li>
        <li class="sidebar-item" :class="['/dataglunt', '/recentdata', '/trendanalysis', '/advancedanalysis'].includes($route.path) ? 'active': ''">
          <a href="#footfall" data-toggle="collapse" class="sidebar-link collapsed">
            <i class="align-middle me-2 fas fa-fw fa-user-friends"></i>{{$t('footfall')}}
          </a>
          <ul id="footfall" class="sidebar-dropdown list-unstyled collapse" :class="['/dataglunt', '/recentdata', '/trendanalysis', '/advancedanalysis'].includes($route.path) ? 'show': ''">
            <li class="sidebar-item" :class="$route.path=='/dataglunt' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/dataglunt">{{$t('data_glunt')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/recentdata' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/recentdata">{{$t('recent_data')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/trendanalysis' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/trendanalysis">{{$t('trend_analysis')}}</RouterLink>
            </li>  
            <li class="sidebar-item" :class="$route.path=='/advancedanalysis' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/advancedanalysis">{{$t('advanced_analysis')}}</RouterLink>
            </li>
          </ul>
        </li>
        <li class="sidebar-item" :class="['/comparebytime', '/comparebyplace', '/trafficdistribution', '/comparebylabel'].includes($route.path) ? 'active': ''">
          <a href="#dataCompare" data-toggle="collapse" class="sidebar-link collapsed"><i class="align-middle me-2 fas fa-fw fa-sliders-h"></i>{{$t('data_compare')}}</a>
          <ul id="dataCompare" class="sidebar-dropdown list-unstyled collapse" :class="['/comparebytime', '/comparebyplace', '/trafficdistribution', '/comparebylabel'].includes($route.path) ? 'show': ''">
            <li class="sidebar-item" :class="$route.path=='/comparebytime' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/comparebytime">{{$t('compare_by_time')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/comparebyplace' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/comparebyplace">{{$t('compare_by_place')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/trafficdistribution' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/trafficdistribution">{{$t('traffic_distribution')}}</RouterLink>
            </li>            
            <li class="sidebar-item" :class="$route.path=='/comparebylabel' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/comparebylabel">{{$t('compare_by_label')}}</RouterLink>
            </li>     
          </ul>
        </li>
        <!-- <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/heatmap"><i class="align-middle" data-feather="map-pin"></i>Heatmap</RouterLink>
        </li>         -->
        <!-- <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/agegender"><i class="align-middle" data-feather="slack"></i>Age & Gender</RouterLink>
        </li>                  -->
        <li class="sidebar-item" :class="['/reportsummary', '/reportstandard', '/reportpremium', '/reportexport'].includes($route.path) ? 'active': ''">
          <a href="#report" data-toggle="collapse" class="sidebar-link collapsed"><i class="align-middle me-2 fas fa-fw fa-file"></i><span class="align-middle">{{$t('report')}}</span></a>
          <ul id="report" class="sidebar-dropdown list-unstyled collapse" :class="['/reportsummary', '/reportstandard', '/reportpremium', '/reportexport'].includes($route.path) ? 'show': ''">
            <li class="sidebar-item" :class="$route.path=='/reportsummary' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/reportsummary">{{$t('summary')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/reportstandard' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/reportstandard">{{$t('standard')}}</RouterLink>
            </li>        
            <li class="sidebar-item" :class="$route.path=='/reportpremium' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/reportpremium">{{$t('premium')}}</RouterLink>
            </li>        
            <li class="sidebar-item" :class="$route.path=='/reportexport' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/reportexport">{{$t('export_db')}}</RouterLink>
            </li>
          </ul>
        </li>
        <li class="sidebar-header">{{$t('setting')}}</li>
        <li class="sidebar-item" :class="$route.path=='/sensors' ? 'active': ''">
          <RouterLink class="sidebar-link" to="/sensors"><i class="align-middle me-2 fas fa-fw fa-camera"></i>{{$t('sensors')}}</RouterLink>
        </li>
        <li class="sidebar-item" :class="$route.path=='/sitemap' ? 'active': ''">
          <RouterLink class="sidebar-link" to="/sitemap"><i class="align-middle me-2 fas fa-fw fa-grip-vertical"></i>{{$t('sitemap')}}</RouterLink>
        </li>
        <li class="sidebar-header">{{$t('about')}}</li>
        <li class="sidebar-item" :class="$route.path=='/about' ? 'active': ''">
          <RouterLink class="sidebar-link active"  to="/about"><i class="align-middle me-2 fas fa-fw fa-eye"></i>{{$t('about')}}</RouterLink>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
// import { useI18n } from 'vue-i18n';
// const { t } = useI18n();

// console.log('logo_iamge', t('_logo_image'));

// const fname = ref("Vue");
// fname.value = t('_logo_image');

// function getImageUrl(name) {
//   return new URL(`/src/assets/${name}`, import.meta.url).href;
// }

const _logo_image = ref();
_logo_image.value = "data:image/png;base64,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",
  


onMounted(()=>{
  const url ='/api/query?data=webconfig&fmt=json&page=main';
  console.log(url);
  axios.get(url)
  .then(result => {
    console.log(result);
  //   // chart.updateSeries(result.data['series']);
  })
  .catch(error => {
      console.log(error);
  });
  // const li_tags = $('li');
  // Object.entries(li_tags).forEach(element => {
  //   // console.log(element[1]);
  //   let tags_a = $(element[1]).children('a');
  //   console.log(tags_a[0]);
  // });
// console.log(li_tags)


});

</script>