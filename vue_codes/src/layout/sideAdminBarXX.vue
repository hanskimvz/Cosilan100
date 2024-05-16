<template>
  <nav class="sidebar sidebar-sticky">
    <div class="sidebar-content ">
      <a class="sidebar-brand" href="/"><img src = "" height="26px"><span class="align-middle ml-2">Business Inteligence</span></a> 
      <ul class="sidebar-nav">
        <li class="sidebar-item" :class="$route.path.indexOf('/admin/account')>=0 ? 'active': ''">
          <RouterLink class="sidebar-link" to="/admin/account"><i class="align-middle" data-feather="monitor"></i>{{$t('account')}}</RouterLink>
        </li>
        <li class="sidebar-item" :class="$route.path.indexOf('/admin/devicetree')>=0 ? 'active': ''">
          <RouterLink class="sidebar-link" to="/admin/devicetree"><i class="align-middle" data-feather="monitor"></i>{{$t('device_tree')}}</RouterLink>
        </li>
        <li class="sidebar-item" :class="$route.path.indexOf('/admin/counterlabel')>=0 ? 'active': ''">
          <RouterLink class="sidebar-link" to="/admin/counterlabel"><i class="align-middle" data-feather="monitor"></i>{{$t('counter_label')}}</RouterLink>
        </li>
        <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:custom')>=0 ? 'active': ''">
          <a href="#customDatabase" data-toggle="collapse" class="sidebar-link collapsed"><i class="align-middle" data-feather="users"></i>{{$t('custom_database')}}</a>
          <ul id="customDatabase" class="sidebar-dropdown list-unstyled collapse" :class="$route.path.indexOf('/admin/db:custom')>=0 ? 'show': ''">
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:custom.count_tenmin_p')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:custom.count_tenmin_p">{{$t('counting')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:custom.age_gender')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:custom.age_gender">{{$t('age_gender')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:custom.heatmap')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:custom.heatmap">{{$t('heatmap')}}</RouterLink>
            </li>  
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:custom.weather')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:custom.weather">{{$t('weather')}}</RouterLink>
            </li>
          </ul>
        </li>
        <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common')>=0 ? 'active': ''">
          <a href="#commonDatabase" data-toggle="collapse" class="sidebar-link collapsed">
            <i class="align-middle" data-feather="sliders"></i>{{$t('common_database')}}
          </a>
          <ul id="commonDatabase" class="sidebar-dropdown list-unstyled collapse" :class="$route.path.indexOf('/admin/db:common')>=0 ? 'show': ''">
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common.params')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:common.params">{{$t('param')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common.counting_report_10min')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:common.counting_report_10min">{{$t('counting')}}</RouterLink>
            </li>

            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common.counting_event')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:common.counting_event">{{$t('event_counting')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common.face_thumbnail')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:common.face_thumbnail">{{$t('face')}}</RouterLink>
            </li>            
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common.heatmap')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:common.heatmap">{{$t('heatmap')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common.snapshot')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:common.snapshot">{{$t('snapshot')}}</RouterLink>
            </li>                    
            <!-- <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common.macsniff')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:common.macsniff">{{$t('mac_sniff')}}</RouterLink>
            </li> -->
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common.accesslog')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/db:common.access_log">{{$t('access_log')}}</RouterLink>
            </li>
          </ul>
        </li>
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/admin/language"><i class="align-middle" data-feather="map-pin"></i>{{$t('language')}}</RouterLink>
        </li>        
        <li class="sidebar-item">
          <RouterLink class="sidebar-link" to="/admin/information"><i class="align-middle" data-feather="slack"></i>{{$t('information')}}</RouterLink>
        </li>
        <li class="sidebar-item" :class="$route.path.indexOf('/system/')>=0 ? 'active': ''">
          <a href="#system" data-toggle="collapse" class="sidebar-link collapsed"><i class="align-middle" data-feather="sliders"></i>{{$t('system')}}</a>
          <ul id="system" class="sidebar-dropdown list-unstyled collapse" :class="$route.path.indexOf('/system/')>=0 ? 'show': ''">        
            <li class="sidebar-item" :class="$route.path=='/system/software' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/system/software"><i class="align-middle" data-feather="camera"></i>{{$t('software')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/system/database' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/system/database"><i class="align-middle" data-feather="camera"></i>{{$t('database')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/system/license' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/system/license"><i class="align-middle" data-feather="camera"></i>{{$t('license')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/system/tool' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/system/tool"><i class="align-middle" data-feather="camera"></i>{{$t('tool')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path.indexOf('/admin/db:common.systemlog')>=0 ? 'active': ''">
              <RouterLink class="sidebar-link" to="/system/log">{{$t('system_log')}}</RouterLink>
            </li>
          </ul>
        </li>
        <li class="sidebar-item" :class="$route.path.indexOf('/admin/webconfig')>=0 ? 'active': ''">
          <a href="#webpageconfig" data-toggle="collapse" class="sidebar-link collapsed"><i class="align-middle" data-feather="sliders"></i>{{$t('webpage_config')}}</a>
          <ul id="webpageconfig" class="sidebar-dropdown list-unstyled collapse" :class="$route.path.indexOf('/admin/webconfig')>=0 ? 'show': ''">
            <li class="sidebar-item" :class="$route.path=='/admin/webconfigbasic' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/webconfigbasic"><i class="align-middle" data-feather="map"></i>{{$t('basic')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/admin/webconfigmenus' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/webconfigmenus"><i class="align-middle" data-feather="map"></i>{{$t('display_menu')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/admin/webconfigdashboard' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/webconfigdashboard"><i class="align-middle" data-feather="map"></i>{{$t('dashboard')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/admin/webconfiganalysis' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/webconfiganalysis"><i class="align-middle" data-feather="map"></i>{{$t('analysis')}}</RouterLink>
            </li>
            <li class="sidebar-item" :class="$route.path=='/admin/webconfigreport' ? 'active': ''">
              <RouterLink class="sidebar-link" to="/admin/webconfigreport" ><i class="align-middle" data-feather="map"></i>{{$t('report')}}</RouterLink>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>
    
</template>
  
<script setup>
</script>