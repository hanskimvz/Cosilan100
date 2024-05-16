import { defineStore } from 'pinia';

const useDatetime = defineStore({
  id: 'place',
  state : () =>({
    date_from : '2024-04-01',
    date_to : '2024-04-19',
    view_by : 'hourly'
  }),
  getters:{
  },
  actions:{
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


export  { useDatetime}