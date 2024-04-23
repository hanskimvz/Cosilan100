<template>
  <nav v-if="flag==0" class="sidebar sidebar-sticky">
    <div class="sidebar-content ">
      <a class="sidebar-brand" href="/"><img src = "" height="26px"><span class="align-middle ml-2">Business Inteligence</span></a> 
      <ul class="sidebar-nav">
        <li class="sidebar-header">Main</li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" active-class="color-red" to="/"><i class="align-middle me-2 fas fa-fw fa-code"></i>Dashboard</RouterLink>
        </li>
        <li class="sidebar-item">
          <a href="#footfall" data-toggle="collapse" class="sidebar-link collapsed">
            <i class="align-middle" data-feather="users"></i>Footfall
          </a>
          <ul id="footfall" class="sidebar-dropdown list-unstyled collapse">
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/dataglunt">Data Glunt</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/recentdata">Recent Data</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/trendAnalysis">Trend Analysis</RouterLink>
            </li>  
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/advancedAnalysis">Advanced Analysis</RouterLink>
            </li>
          </ul>
        </li>
        <li class="sidebar-item">
          <a href="#dataCompare" data-toggle="collapse" class="sidebar-link collapsed">
            <i class="align-middle" data-feather="sliders"></i>Data Compare
          </a>
          <ul id="dataCompare" class="sidebar-dropdown list-unstyled collapse">
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/comparebytime">Compare By Time</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/comparebyplace">Compare By Place</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/trafficdistribution">Traffic Distribution</RouterLink>
            </li>            
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/comparebylabel">Compare By Label</RouterLink>
            </li>     
          </ul>
        </li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/heatmap"><i class="align-middle" data-feather="map-pin"></i>Heatmap</RouterLink>
        </li>        
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/agegender"><i class="align-middle" data-feather="slack"></i>Age & Gender</RouterLink>
        </li>                 
        <li class="sidebar-item">
          <a href="#report" data-toggle="collapse" class="sidebar-link collapsed">
            <i class="align-middle" data-feather="book-open"></i><span class="align-middle">Report</span>
          </a>
          <ul id="report" class="sidebar-dropdown list-unstyled collapse">
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/reportsummary">Summary</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/reportstandard">Standard</RouterLink>
            </li>        
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/reportpremium">Premium</RouterLink>
            </li>        
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/reportexport">Query Database</RouterLink>
            </li>
          </ul>
        </li>
        <li class="sidebar-header">setting</li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/sensors"><i class="align-middle" data-feather="camera"></i>Sensors</RouterLink>
        </li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/sitemap"><i class="align-middle" data-feather="map"></i>Sitemap</RouterLink>
        </li>
        <li class="sidebar-header">about</li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/about"><i class="align-middle" data-feather="map"></i>About</RouterLink>
        </li>
      </ul>
    </div>
  </nav>

  <nav v-else class="sidebar sidebar-sticky">
    <div class="sidebar-content ">
      <a class="sidebar-brand" href="/"><img src = "" height="26px"><span class="align-middle ml-2">Business Inteligence</span></a> 
      <ul class="sidebar-nav">
        <li class="sidebar-header">Main</li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/admin/account"><i class="align-middle" data-feather="monitor"></i>Account</RouterLink>
        </li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/admin/devicetree"><i class="align-middle" data-feather="monitor"></i>Device Tree</RouterLink>
        </li>        
        <li class="sidebar-item">
          <a href="#footfall" data-toggle="collapse" class="sidebar-link collapsed">
            <i class="align-middle" data-feather="users"></i>Footfall
          </a>
          <ul id="footfall" class="sidebar-dropdown list-unstyled collapse">
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/dataglunt">Data Glunt</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/recentdata">Recent Data</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/trendAnalysis">Trend Analysis</RouterLink>
            </li>  
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/advancedAnalysis">Advanced Analysis</RouterLink>
            </li>
          </ul>
        </li>
        <li class="sidebar-item">
          <a href="#dataCompare" data-toggle="collapse" class="sidebar-link collapsed">
            <i class="align-middle" data-feather="sliders"></i>Data Compare
          </a>
          <ul id="dataCompare" class="sidebar-dropdown list-unstyled collapse">
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/comparebytime">Compare By Time</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/comparebyplace">Compare By Place</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/trafficdistribution">Traffic Distribution</RouterLink>
            </li>            
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/comparebylabel">Compare By Label</RouterLink>
            </li>     
          </ul>
        </li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/heatmap"><i class="align-middle" data-feather="map-pin"></i>Heatmap</RouterLink>
        </li>        
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/agegender"><i class="align-middle" data-feather="slack"></i>Age & Gender</RouterLink>
        </li>                 
        <li class="sidebar-item">
          <a href="#report" data-toggle="collapse" class="sidebar-link collapsed">
            <i class="align-middle" data-feather="book-open"></i><span class="align-middle">Report</span>
          </a>
          <ul id="report" class="sidebar-dropdown list-unstyled collapse">
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/reportsummary">Summary</RouterLink>
            </li>
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/reportstandard">Standard</RouterLink>
            </li>        
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/reportpremium">Premium</RouterLink>
            </li>        
            <li class="sidebar-item">
              <RouterLink class="sidebar-link" to="/reportexport">Query Database</RouterLink>
            </li>
          </ul>
        </li>
        <li class="sidebar-header">setting</li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/sensors"><i class="align-middle" data-feather="camera"></i>Sensors</RouterLink>
        </li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/sitemap"><i class="align-middle" data-feather="map"></i>Sitemap</RouterLink>
        </li>
        <li class="sidebar-header">about</li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/about"><i class="align-middle" data-feather="map"></i>About</RouterLink>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
let flag = 0
// import { useRoute } from 'vue-router'
// let route = useRoute();

// console.log(route, route.path.split('/'))


// if (route.path.indexOf('admin')>0){
//    flag = 1;
// }

// const userData = ref()
// watch(
//   () => route.path,
//   async newPath => {
//     userData.value = await console.log(newPath)
//   }
// )

</script>