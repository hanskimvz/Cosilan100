import { ref, reactive } from 'vue';
// import { ko, enUS, zhCN } from 'date-fns/locale';

const square_code = ref(0);
const store_code = ref(0);
const date_from = ref('');
const date_to = ref('');
const view_by = ref('hourly');
const load_time = ref(Date.now());
const _tz_offset = 9;

// const locale = reactive(ko);
// const dateFormat = ref('yyyy-MM-dd');

// const locale = reactive(zhCN);
// const dateFormat = ref('yyyy-MM-dd');

// const locale = reactive(enUS);
// const dateFormat = ref('MMM dd yyyy');

export {load_time, square_code , store_code, date_from, date_to, view_by, _tz_offset};