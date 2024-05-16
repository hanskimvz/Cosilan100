import { defineStore } from 'pinia';

// const _tz_offset = 3600*9;
const _tz_offset = new Date().getTimezoneOffset()*60 *-1;

const navStore = defineStore({
  id: 'navstore',
  state : () =>({
    date_from: new Date(),
    date_to: new Date(),
    date_to1: new Date(),
    date_to2: new Date(),
    view_by: 'hourly',
    view_on: '7days',
    db_name: 'cnt_demo',
    sq_code: 0,
    st_code: 0,
    cam_code: 0,
    sq_code1: 0,
    st_code1: 0,
    cam_code1: 0,
    sq_code2: 0,
    st_code2: 0,
    cam_code2: 0,
    place_data: new Array(),
    ts : Date.now()
  }),
  getters:{
  },
  actions:{
    clear_square() {
      this.sq_code = 0;
    },
    clear_store() {
      this.st_code = 0;
    },
  }
});

const charts = defineStore({
  id: 'charts',
  state : () =>({
    chart_bar: null,
    chart_line: null,
  }),
  getters:{
  },
  actions:{
  }
});

const getDateString = ( (date)=> {
  let y = date.getFullYear();
  let m = date.getMonth() + 1;
  let d = date.getDate();
  // if (m<10) {
  //   m = '0'+ m
  // }
  
  // if (d<10) {
  //   d = '0'+ d
  // }  
  return ( y + "-" + ('0' + m).slice(-2) + "-" + ('0' + d).slice(-2));
});

function Utc2Local(date, offset) {
  
  let dt = new Date(date);
  let ts = dt.getTime() + offset * 1000;
  let new_d = new Date(ts);
  let y = new_d.getFullYear();
  let m = new_d.getMonth() + 1;
  let d = new_d.getDate();
  let h = new_d.getHours();
  let mm = new_d.getMinutes();

  // if (m<10) {
  //   m = '0'+ m;
  // }
  // if (d<10) {
  //   d = '0'+ d;
  // }
  // if (h<10) {
  //   h = '0' + h;
  // }
  // if (mm<10){
  //   mm = '0' + mm;
  // }
  return (y + "-" + ('0' + m).slice(-2) + "-" + ('0' + d).slice(-2) + " " + ('0' + h).slice(-2) + ":" + ('0' + mm).slice(-2));
}

function addDays(date, days) {
  const clone = new Date(date);
  clone.setDate(date.getDate() + days);
  return clone;
}
const db_name = 'cnt_demo';

export  {_tz_offset, navStore, charts, getDateString, Utc2Local, addDays, db_name }