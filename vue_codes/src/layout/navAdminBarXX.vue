<template>
  <nav class="navbar sidebar-sticky navbar-expand navbar-light bg-white">
    <a class="sidebar-toggle d-flex mr-2"><i class="hamburger align-self-center"></i></a>
    <form v-if="$route.path != '/admin/db:common.systemlog'" method="GET" class="form-inline d-none d-sm-inline-block" ENCTYPE="multipart/form-data">
      <input type="text" class="form-control form-control-no-border"  placeholder="Search" name="search" value="" size="100">
      <button type="submit" class="btn btn-warning" >Search</button>
    </form>

    <div class="navbar-collapse collapse">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item dropdown">
          <a class="nav-flag dropdown-toggle" href="#" id="languageDropdown" data-toggle="dropdown">
            <img :src="img_cur" />
          </a>
          <div class="dropdown-menu dropdown-menu-right" aria-labelledby="languageDropdown">
            <span class="dropdown-item" @click="changeLocale('eng')" style="cursor:pointer;">
              <img :src="img['eng']" alt="English" width="20" class="align-middle mr-1" />
              <span class="align-middle">{{$t('english')}}</span>
            </span>
            <span class="dropdown-item" @click="changeLocale('kor')" style="cursor:pointer;">
              <img :src="img['kor']" alt="Korean" width="20" class="align-middle mr-1" />
              <span class="align-middle">{{$t('korean')}}</span>
            </span>
            <span class="dropdown-item" @click="changeLocale('chi')" style="cursor:pointer;">
              <img :src="img['chi']" alt="Chinese" width="20" class="align-middle mr-1" />
              <span class="align-middle">{{$t('chinese')}}</span>
            </span>
          </div>
        </li>
        <li class="nav-item dropdown">
          
          <a class="nav-link dropdown-toggle d-none d-sm-inline-block" href="#" data-toggle="dropdown"><i class="align-middle" data-feather="user"></i> <span class="text-dark">User Name</span></a>
          <div class="dropdown-menu dropdown-menu-right">
            <RouterLink class="dropdown-item" to="/profile">{{$t('profile')}}</RouterLink>
            <a class="dropdown-item" href="/admin/" target = "admin_page">{{$t('admin_page')}}</a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="/help/">{{$t('help')}}</a>
            <a class="dropdown-item" href="/logout">{{$t('logout')}}</a>
          </div>
        </li>
      </ul>
    </div>
  </nav>
  
</template>
<script setup>
import {ref, onMounted} from 'vue';
import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();

let img_cur = ref();
defineProps({
  img_eng: {
    type: String,
  }
});

const img = {
  'eng': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAAA1CAMAAACA7r40AAAA/FBMVEWyIjNPN2Y8O249PG8+PW8+PXA/PnBBQHFCQXNDQnNFRHVHR3dIR3dJSHhLSnlMS3pOTXtOTXxPTnxRUH1RUX5SUX5TUn9WVYFYV4JYV4NaWYReXohgX4lhYYpiYYplZIxra5FvbpRwb5VycZZycpZ0c5h7e518fJ6CgqKDgqOGYoCIh6aIiKeJiaeUk6+VlbGXlrKYl7Kiobqiorqjo7ukpLurqsCsq8GyIjS0tMe1tMi2tci4uMq6usy7u8zExNPFxdTGxdTGxtXHYG3Hx9XPdYDXi5Teoajg3+jg4Ojltbvn5u3n5+3r6/Dty8/w8PTx8fX09Pf19fj///+ShAP7AAAAAnRSTlPQ9qN1Xw4AAAG4SURBVFjD7ZVbU9NgFEXjCj1Ik1ZSQsutFmuo1BZBuYgS5SYiIKic//9ffMgMA/0yQzunk4dO11vWy575cvZs78WQeBaAOgBBAA8frjs04CEf9Q0QX/2KgbbuCHnOFsK2hgC/bwAq+gHynDEkKJVpZk/TpFwKqNVcx50BD4BEDwTks74FYtV40IEayEJe/e0B9P9UAU6OXWcO2UAQlpcRhA0QcZ0xRL5r8viRvgl57tyAB500wof9PfCJ0g6+7zrrdQH0fAC/B8DrpuvGEJLoiYCcPn2kR84eMkvUbSMl2t2IWehuuo5rAx6yksZAZatfARbTFSHP2a7LP9JVoKxaBlb1i0+eM/aktTZPCOvrEDK/1mLupevG0PjWbUdA3t22gIWjrwuDDi4MZCE1/QSwqxEwozoz6OzXVacaNggCGmGVOjQarpug0bo0MPRo2a/rYaCSnNFKxjVa932ArX9VgB9nrjOHJAjC0hKCkGSjNej4aWDo0TJeVyeNIBsosoHKc2MYrecxhbwfEtM/0QKYoJDLAvAOC2CCQi4KYNqT0UKuC2Dak9FCzgtg2pPRQu4KYNqT0UKK4D/1FIf2XdvrFwAAAABJRU5ErkJggg==",
  'kor': "data:image/png;base64,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",
  'chi': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABDCAMAAABdlVDoAAABR1BMVEXfKRDeKRDeKhDeKxDeLBDfKxDfLRDfLw/fMA/fMQ/gMg/gNA/gNQ/gNw/hOA/hOg7hPA7hPQ7iPA7iPQ7iPg7iPw7iQA7iQQ7iQg7jQQ7jQg7kRw3kSQ3kSg3kSw3kTA3lTg3lUA3lUQzlUgzmUwzmVQzmVwzmWAznVwznWgznWwznXQvoYAvoYQvoYgvpZAvpZQvqagrqawrqbArrbgrrcArsdAnsdgnseAnseQntegntewntfAntfgnufgjugQjuggjuhAjvgwjvhQjvhgjviQjwiwfwjAfxjgfxkQfylAfymAbzmQbzmwbznAbznwb0oAX0ogX0owX1pgX1qAX1qgX2rAT2sAT3rwT3sgT3swT3tAT4twP4uAP5uwP6wwL6xQL7xQL7yAL7ygL8ygL8zQL90QH90wH+2AH+2QD+2wD/3AD/3gCZgVGdAAAAAXRSTlPUwVjOqwAAAXpJREFUWMPt2ddTwjAcB3CSynQgVMGFgiOCG7UKLsSBe+IeiIr7+/8/+8CwLTxJ0vO85Knpfe8+98to06vNZkUjFrS/gjhEIw4vUZeFV3J0hlX+SIOx2wlgxskbSSr6Ht0HXjWVM0KfIvpucNz/0M99uMLImO6MBLkjm3ik5uIIIT7KEaF5oLdGbHLNofl4ISEAGzViESBbfyXdjDHG2DUAFC+Hfhazc/4N2Ksf8V7A2ApMN4j+USA3W/9wKYufeiPbbMxdBszb9HdzEs5XiI8582oK81pdnoOy0SPwUd9RQtIi3ydLJeReJHJXnpO2qlzIzQlRga+0PfYCJKty63FOSALPg4SQlnPcGkN2LQXsJhQeyM1pU3HvJd+9xpSaA65cPCpp1Cqboy9qik0DK8KPRJmBwA4VjbgIUUQirjHRRyL31vDxgvBz1xRQaBeNxAAcdolFWk+2MWHBgTsetQChnn/zfSIRiUhEIhKRiEQkIhGJSEQilvwI+gbiNmMZjsKSWAAAAABJRU5ErkJggg=="
}

const changeLocale= ((lang) =>{
  console.log(lang);
  // set cookie __locale 
  locale.value = lang;
  img_cur.value = img[lang];
});

onMounted(()=>{
  img_cur.value = img[locale.value];
})
// const img_cur = img_eng

</script>   

