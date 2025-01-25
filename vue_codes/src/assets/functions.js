
const _tz_offset = new Date().getTimezoneOffset()*60 *-1;

const getDateString = ( (date)=> {
  let y = date.getFullYear();
  let m = date.getMonth() + 1;
  let d = date.getDate();
  return ( y + "-" + ('0' + m).slice(-2) + "-" + ('0' + d).slice(-2));
});


function addDays(date, days) {
  const clone = new Date(date);
  clone.setDate(date.getDate() + days);
  return clone;
}


function Utc2Local(date, offset) {
  let dt = new Date(date);
  let ts = dt.getTime() + offset * 1000;
  let new_d = new Date(ts);
  let y = new_d.getFullYear();
  let m = new_d.getMonth() + 1;
  let d = new_d.getDate();
  let h = new_d.getHours();
  let mm = new_d.getMinutes();
  return (y + "-" + ('0' + m).slice(-2) + "-" + ('0' + d).slice(-2) + " " + ('0' + h).slice(-2) + ":" + ('0' + mm).slice(-2));
}

const arraySum = ((arr) => {
	let sum = 0;
	arr.forEach(function(item){
		sum += Number(item);
	});
	return sum;
});

const makeXaxis = (date_from, date_to, view_by)=> {
  let ts_from = (new Date(date_from).getTime())/1000;
  let ts_to = (new Date(date_to).getTime())/1000 + 3600*24 -1;
  let step = 3600;  

  let xaxis = [];
  if (view_by == 'tenmin') {
      step = 600;
  }
  else if (view_by == 'hourly') {
    step = 3600;
  }
  else if (view_by == 'daily') {
    step = 3600*24;
  }
  else if (view_by == 'weekly') {
    step = 3600*24*7;
  }
  // 1704067200
  // 1704002400
  if (view_by == 'monthly') {
    let d_from = new Date(date_from);
    d_from.setDate(1); // 1일로 설정
    d_from.setHours(0, 0, 0, 0); // 0시 0분 0초로 설정
    ts_from = d_from.getTime()/1000;

    let d_to = new Date(date_to);
    d_to.setDate(1); // 1일로 설정
    d_to.setHours(0, 0, 0, 0); // 0시 0분 0초로 설정
    d_to.setMonth(d_to.getMonth() + 1); // 다음달로 이동
    d_to.setDate(0); // 이전달의 마지막날로 설정
    ts_to = d_to.getTime()/1000;

    let d = new Date(ts_from * 1000);
    while (d.getTime()/1000 <= ts_to) {
      d.setDate(1); // 매월 1일로 설정 
      d.setHours(0, 0, 0, 0); // 0시 0분 0초로 설정
      xaxis.push(d.getTime());
      console.log('xaxis', new Date(d.getTime()).toISOString());
      d.setMonth(d.getMonth() + 1); // 다음달로 이동
    }
  }
  else {
    for (let i=ts_from; i<=ts_to; i+=step) {
      xaxis.push(i*1000 - _tz_offset*1000);
    }
  }
  console.log('xaxis',view_by, xaxis);
  return xaxis;
}

const makeSeries = (data, xaxis, t)=> {
  let series = [];
  let ct_labels = [];
  let arr_cnt = {};
  let now = new Date().getTime()/1000 + _tz_offset;
  data.forEach( (item, idx)=> {
    if (!ct_labels.includes(item.ct_label)) {
      ct_labels.push(item.ct_label);
      series.push({
        name: item.ct_label,
        data: []
      });
    }
    if (!arr_cnt[item.ct_label]) {
      arr_cnt[item.ct_label] = {};
    }
    if (!arr_cnt[item.ct_label][item.timestamp]) {
      arr_cnt[item.ct_label][item.timestamp] = 0;
    }
    arr_cnt[item.ct_label][item.timestamp] += item.ct_value;
  });

  // console.log('arr_cnt', Object.keys(arr_cnt).length, arr_cnt);

  for (let i=0; i<ct_labels.length; i++) {
    for (let j=0; j<xaxis.length; j++) {
      if (arr_cnt[ct_labels[i]][xaxis[j]/1000 + _tz_offset]) {
        series[i].data.push(arr_cnt[ct_labels[i]][xaxis[j]/1000 + _tz_offset]);
      }
      else if (xaxis[j]/1000 + _tz_offset > now) {
        series[i].data.push(null);
      }
      else {
        series[i].data.push(0);
      }
    }
  }
  for (let i=0; i<series.length; i++) {
    series[i].name = t(series[i].name);
  }
  // console.log('ct_labels', ct_labels);
  console.log('series', series);
  return series;
}

export  { _tz_offset, getDateString, Utc2Local, addDays, arraySum, makeXaxis, makeSeries }