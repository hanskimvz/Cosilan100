
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

export  { _tz_offset, getDateString, Utc2Local, addDays, arraySum }