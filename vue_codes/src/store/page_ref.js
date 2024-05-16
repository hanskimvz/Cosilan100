import { defineStore } from 'pinia';

const useDataGlunt = defineStore({
  id: 'dataglunt',
  state : () =>({
    date_from: new Date(),
    date_to: new Date(),
    view_by: 'hourly',
    sq_code: 0,
    st_code: 0,
    cam_code: 0,
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

const useRecentData = defineStore({
  id: 'recentdata',
  state : () =>({
    date_from: new Date(),
    date_to: new Date(),
    view_by: 'daily',
    view_on: '7days',
    sq_code: 0,
    st_code: 0,
    cam_code: 0,
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
// const usePlaceStore = defineStore({
//   id: 'store',
//   state : () =>({
//     code : 0,
//     name : 'All Store'
//   }),
//   getters:{
    
//   },
//   actions:{
//     clear() {
//       this.code = 0;
//     }
//   }
// });


const getDateString = ( (date)=> {
  let y = date.getFullYear();
  let m = date.getMonth() + 1;
  if (m<10) {
    m = '0'+ m
  }
  let d = date.getDate();
  if (d<10) {
    d = '0'+ d
  }  
  return (y+"-"+m+"-"+d)
});

function Utc2Local(date, offset) {
  let dt = new Date(date);
  let ts = dt.getTime() + offset * 1000;
  let new_d = new Date(ts);
  let y = new_d.getFullYear();
  let m = new_d.getMonth() + 1;
  let d = new_d.getDate();
  let h = new_d.getHours();
  let mm = new_d.getMinutes()

  if (m<10) {
    m = '0'+ m;
  }
  if (d<10) {
    d = '0'+ d;
  }
  if (h<10) {
    h = '0' + h;
  }
  if (mm<10){
    mm = '0' + mm;
  }
  return (y + "-" + m + "-" + d + " " + h + ":" + mm)
}

export  { useDataGlunt, useRecentData, getDateString, Utc2Local }